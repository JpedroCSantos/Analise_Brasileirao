import json
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "pipeline")))

from typing import List
from pipeline.table import Championship_Table

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

if __name__ == "__main__":
    path="data/input"
    file_name = "season_2021.json"

    from pipeline.extract import json_to_dataFrame

    with open(f"{path}/{file_name}", "r") as file:
            json_content = json.load(file)

    df = json_to_dataFrame(json_content["response"], encoding=True)
    # print(df)
    filter_df(df)