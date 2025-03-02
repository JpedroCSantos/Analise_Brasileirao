import os  # biblioteca para manipular arquivos e pastas
import json
import pandas as pd

from typing import List

def read_file(path: str, file_name: str, encoding: bool =False) -> pd.DataFrame:
    """
    function para ler um arquivo e retornar uma dataframe

    args: path (srt): caminho arquivo
          delimiter(srt): Delimitador do arquivo csv (Default: ',')
          encoding(srt): Encode do arquivo csv (Default: 'utf-8')

    return: dataframe
    """
    print("Loading File")
    if (os.path.exists(f"{path}/{file_name}")):
        with open(f"{path}/{file_name}", "r") as file:
            content = json.load(file)
            
    return  content if 'content' in locals() else None

def json_to_dataFrame(json_content: json, encoding: bool =False) -> pd.DataFrame:
    """
    function para ler um json e retornar uma dataframe

    args: path (srt): caminho arquivo
          delimiter(srt): Delimitador do arquivo csv (Default: ',')
          encoding(srt): Encode do arquivo csv (Default: 'utf-8')

    return: dataframe
    """
    content = json_content
    if isinstance(content, list):
        df = pd.json_normalize(content)  # Normaliza toda a lista de objetos JSON
    else:
        df = pd.json_normalize([content])

    if encoding and 'df' in locals():
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].apply(fix_encoding_issues)

    return  df if 'df' in locals() else None

def fix_encoding_issues(text):
    if isinstance(text, str):
        replacements = {
            'Ã£': 'ã', 'Ã¡': 'á', 'Ã¢': 'â', 'Ãª': 'ê', 'Ã³': 'ó', 'Ãº': 'ú',
            'Ã©': 'é', 'Ã§': 'ç', 'Ã‘': 'Ñ', 'Ã¬': 'ì', 'Ã¹': 'ù',
            'Ã³': 'ó', 'Ã•': 'Õ', 'Ãµ': 'õ', 'Ã‰': 'É', 'Ã‡': 'Ç',
            'Ã€': 'À', 'Ã£': 'ã', 'Ãƒ': 'Â', 'Ãº': 'ú'
        }
        for corrupted, correct in replacements.items():
            text = text.replace(corrupted, correct)
    return text

def parquet_to_dataFrame(path: str, file_name: str):
    print("Loading Dataframe")
    if (os.path.exists(f"{path}/{file_name}.parquet")):
        print("Lendo arquivo PARQUET")
        df = pd.read_parquet(f"{path}/{file_name}.parquet")
    
    return df

def csv_to_dataFrame(path: str, file_name: str):
    if(os.path.exists(f"{path}/{file_name}.csv")):
        print("Lendo arquivo CSV")
        df = pd.read_csv(f"{path}/{file_name}.csv", delimiter=";", encoding="utf-8")

    return df

if __name__ == "__main__":
    content = read_file(path="data/input", file_name = "season_2021.json", encoding=True)
    print(content)