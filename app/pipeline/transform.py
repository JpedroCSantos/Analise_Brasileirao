import json
import os
import sys
import glob
import requests
import pandas as pd

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "pipeline")))

from typing import List, Dict
from PIL import Image
from pipeline.table import Championship_Table
from pipeline.extract import json_to_dataFrame

def build_dataframe(json_content: json):
    df = json_to_dataFrame(json_content, encoding=True)
    df = filter_df(df)
    
    return df

def remove_coluns(df: pd.DataFrame, columns_to_remove: List[str]):
    """
    Remove coluna(s) de um dataframe, baseados no nome da coluna(s).

    args: df(pd.dataframe): Dataframe
          columns_to_remove (str or List): Coluna a ser removida

    return: dataframe
    """
    print("Removendo Colunas")
    return df.drop(columns_to_remove, axis=1)

def filter_df(df: pd.DataFrame):
    columns_to_remove: list = ["score.halftime.home", "score.halftime.away", "score.fulltime.home",
                        "score.fulltime.away", "score.extratime.home", "score.extratime.away",
                        "score.penalty.home", "score.penalty.away", "fixture.referee",
                        "fixture.timezone", "fixture.date", "fixture.timestamp",
                        "fixture.periods.first", "fixture.periods.second", "fixture.venue.id",
                        "fixture.venue.name", "fixture.venue.city", "fixture.status.long",
                        "fixture.status.short", "fixture.status.elapsed", "fixture.status.extra",
                        "league.country", "league.logo", "league.flag", "league.standings"]
    
    df = remove_coluns(df, columns_to_remove)
    table = Championship_Table()

    for index, row in df.iterrows():
        TEAMS = table.get_teams(row)
        table.get_results(row, TEAMS)
    
    table.build_classification()
    return table.table

def create_compiled_dataframe(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    columns= ["Team_ID", "Team_Name", "Team_Logo", "Victories", "Defeats",
                "Draws_With_Goals", "Draws_Without_Goals"]
    compiled_dataframe = pd.DataFrame(columns = columns)

    for df in dfs:
        for index, row in df.iterrows():
            TEAM_ID = row["Team_ID"]
            getLogo(row)
            if TEAM_ID not in compiled_dataframe['Team_ID'].values:
                new_entry = {col: row[col] if col in row else 0 for col in columns}
                compiled_dataframe = pd.concat([compiled_dataframe, pd.DataFrame([new_entry])], ignore_index=True)
            else:
                columns_to_update = ["Victories", "Defeats", "Draws_With_Goals", "Draws_Without_Goals"]
                compiled_dataframe.loc[compiled_dataframe["Team_ID"] == TEAM_ID, columns_to_update] += row[columns_to_update]
        
    return compiled_dataframe

def getLogo(row: Dict):
    """
    Faz o download de uma imagem a partir de uma URL e salva no caminho especificado.
    
    :param url: URL da imagem a ser baixada.
    :param save_path: Caminho onde a imagem será salva.
    """
    OUTPUT_PATH = "images"
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH, exist_ok=True)
    
        return
    
    TEAM_ID = str(row["Team_ID"]) + ".png"
    FILE_NAME = os.path.join(OUTPUT_PATH, os.path.basename(TEAM_ID))
    try:
        response = requests.get(row["Team_Logo"], stream=True)
        response.raise_for_status()  # Garante que a requisição foi bem-sucedida

        temp_path = FILE_NAME + "_temp"
        with open(temp_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        with Image.open(temp_path) as img:
            img = img.convert("RGBA")
            img.save(FILE_NAME, format="PNG")

        os.remove(temp_path)

        print(f"Imagem salva com sucesso em: {FILE_NAME}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem: {e}")
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")

def getLogoPath(df: pd.DataFrame) -> pd.DataFrame:
    ERROS = []
    for index, row in df.iterrows():
        TEAM_ID = row["Team_ID"]
        TEAM_NAME = row["Team_Name"]
        try:
            [LOGO] = glob.glob(f"images/{TEAM_ID}.png")  # Busca a logo na pasta 'images/'            
            if not LOGO:
                raise FileNotFoundError
            
            df.loc[index, 'Logo_File'] = LOGO
        except FileNotFoundError:
            ERROS.append(f"A logo do time {TEAM_NAME} com o ID: {TEAM_ID} não foi encontrada")
    
    if ERROS and len(ERROS):
        print(ERROS)

    return df

def getStatisticsData(df: pd.DataFrame) -> pd.DataFrame:
    for index, row in df.iterrows():
        TOTAL_GAMES = row['Victories'] + row['Defeats'] + row['Draws_With_Goals'] + row['Draws_Without_Goals']        

        df.loc[index, 'N_de_partidas'] = TOTAL_GAMES
        df.loc[index, 'Percent_Draws_Without_Goals'] = (row['Draws_Without_Goals'] / TOTAL_GAMES) * 100
    
    return df

if __name__ == "__main__":
    path="data/input"
    file_name = "season_2021.json"

    from pipeline.extract import json_to_dataFrame

    with open(f"{path}/{file_name}", "r") as file:
            json_content = json.load(file)

    df = json_to_dataFrame(json_content["response"], encoding=True)
    # print(df)
    filter_df(df)