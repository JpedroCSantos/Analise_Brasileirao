import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import json
import requests
from typing import Dict

from api.classes.consult_class import ConsultApi

class FootballAPI(ConsultApi):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.response_file = "response.json"
        
    def search(self, params: Dict, endpoint: str) -> json:
        """
        Realiza uma requisição à API de futebol e armazena a resposta no arquivo JSON.

        args: 
            params (Dict): Parâmetros da requisição.
            endpoint (str): Endpoint da API.

        return: json (resposta da API) ou None em caso de erro.
        """
        BASE_URL: str = f"https://v3.football.api-sports.io/{endpoint}"
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            if response.status_code != 200:
                return None
            
            data = response.json()
            if os.path.exists(self.response_file):
                with open(self.response_file, "r") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            existing_data.append({
                "endpoint": endpoint,
                "params": params,
                "response": data
            })
            with open(self.response_file, "w") as f:
                json.dump(existing_data, f, indent=4)

            return data
                        
        except Exception as e:
            print(f"Erro ao realizar a requisição: {e}")
            return None

    def getStatus(self) -> Dict:
        """
        Realiza uma requisição à API de futebol para consultar o status da API e da
        API_KEY fornecida.


        return: {
            'plan': response.plan,
            'requests_avaible': True or False
        }
        """
        BASE_URL: str = "https://v3.football.api-sports.io/status"
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        try:
            response = requests.get(BASE_URL, headers=headers)
            if response.status_code != 200:
                return None
            
            data = response.json()
            RESPONSE = data['response']
            if isinstance(data['errors'], list) and len(data['errors']):
                print(f"List ERRO: {data['errors']}")
                return {
                    'plan': data['subscription']['plan'] if RESPONSE else None,
                    'requests_avaible': False
                }
            elif isinstance(data['errors'], Dict) and data['errors']:
                print(f"Dict ERRO: {data['errors']}")
                return {
                    'plan': data['subscription']['plan'] if RESPONSE else None,
                    'requests_avaible': False
                }
            
            LIMIT_REQUEST = RESPONSE['requests']['limit_day']
            CURRENT_VALUE = RESPONSE['requests']['current']
            REQUEST_AVAIBLE = True if CURRENT_VALUE < LIMIT_REQUEST else False

            return {
                'plan': RESPONSE['subscription']['plan'],
                'requests_avaible': REQUEST_AVAIBLE
            }        
        except Exception as e:
            print(f"Erro ao realizar a requisição: {e}")
            return None
    
if __name__ == "__main__":
    import os
    import sys
    from dotenv import load_dotenv

    load_dotenv(dotenv_path="env/.env")
    api_key = os.getenv("api_football_key")
    football_api = FootballAPI(api_key)

    BRASILEIRAO_LIGA_ID = 71
    SEASONS = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
               '2020', '2021', '2022', '2023', '2024']
    end_point = "fixtures"

    football_api.getStatus()
    for season in SEASONS:
        params = {
            'league': BRASILEIRAO_LIGA_ID,
            'season': season
        }

        football_api.search(params = params, endpoint = end_point)