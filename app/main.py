import os
import sys
import json

from dotenv import load_dotenv
from api.consult import FootballAPI

load_dotenv(dotenv_path="env/.env")
INPUT_DATA_PATH     = "data/input/bilheteria-diaria-obras-por-exibidoras-csv"
DATA_PATH           = "data/output"
FINAL_PATH          = f"{DATA_PATH}/DATAS/FINAL_DATABASE"
TEMP_PARQUET_FILE   = f"{DATA_PATH}/Backup/TEMP_DATAFRAME.parquet"
FINAL_FILE_NAME     = "MOVIES"

PARAMS = {
    "CONSULT_API": False,
}

if PARAMS['CONSULT_API']:
    football_api = FootballAPI(os.getenv("api_football_key"))
    STATUS = football_api.getStatus()
    if not STATUS['requests_avaible']:
        print(STATUS)
        raise('Api não disponivel para consulta!')

    BRASILEIRAO_LIGA_ID = 71
    SEASONS = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
            '2020', '2021', '2022', '2023', '2024']
    end_point = "fixtures"

    for season in SEASONS:
        params = {
            'league': BRASILEIRAO_LIGA_ID,
            'season': season
        }

        football_api.search(params = params, endpoint = end_point)


if os.path.exists("data/input/season_2021.json"):
    with open("data/input/season_2021.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

print(len(data['response']['response']))