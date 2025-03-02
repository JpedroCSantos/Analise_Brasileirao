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


if __name__ == "__main__":
    content = read_file(path="data/input", file_name = "season_2021.json", encoding=True)
    print(content)