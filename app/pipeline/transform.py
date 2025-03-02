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

def create_compiled_dataframe(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    columns= ["Team_ID", "Team_Name", "Team_Logo", "Victories", "Defeats",
                "Draws_With_Goals", "Draws_Without_Goals"]
    compiled_dataframe = pd.DataFrame(columns = columns)

    for df in dfs:
        for index, row in df.iterrows():
            TEAM_ID = row["Team_ID"]
            if TEAM_ID not in compiled_dataframe['Team_ID'].values:
                new_entry = {col: row[col] if col in row else 0 for col in columns}
                compiled_dataframe = pd.concat([compiled_dataframe, pd.DataFrame([new_entry])], ignore_index=True)
            else:
                columns_to_update = ["Victories", "Defeats", "Draws_With_Goals", "Draws_Without_Goals"]
                compiled_dataframe.loc[compiled_dataframe["Team_ID"] == TEAM_ID, columns_to_update] += row[columns_to_update]
        
    return compiled_dataframe
    

if __name__ == "__main__":
    path="data/input"
    file_name = "season_2021.json"

    from pipeline.extract import json_to_dataFrame

    with open(f"{path}/{file_name}", "r") as file:
            json_content = json.load(file)

    df = json_to_dataFrame(json_content["response"], encoding=True)
    # print(df)
    filter_df(df)