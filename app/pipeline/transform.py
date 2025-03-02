import json
import pandas as pd

from typing import List
from pipeline.table import Championship_Table


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

    return table.table

if __name__ == "__main__":
    path="data/input"
    file_name = "season_2021.json"

    with open(f"{path}/{file_name}", "r") as file:
            json_content = json.load(file)

    df = json_to_dataFrame(json_content["response"], encoding=True)
    # print(df)
    filter_df(df)