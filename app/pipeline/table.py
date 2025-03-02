# import os
# import sys
import pandas as pd

from typing import Dict
from pipeline.classes.table_class import Table
from pipeline.schemas.table_schema import ChampionshipSchema


class Championship_Table(Table):
    def __init__(self):
        self.table = self.build_table()

    def build_table(self) -> pd.DataFrame:
        columns = list(ChampionshipSchema.__annotations__.keys())
        
        return pd.DataFrame(columns= columns)
    
    def get_teams(self, row: Dict) -> Dict:
        """
        Função para buscar os times participantes de
        query (EX: Titulo do filme)

        args: Row: Linha do dataframe com as informações para serem utilizadas
              na busca

        return: json
        """

        TEAMS_KEY = ["home", "away"]
        TEAMS_ID = {}
        for key in TEAMS_KEY:
            TEAM_KEY = f"teams.{key}"
            TEAM_ID = row[f"{TEAM_KEY}.id"]

            if TEAM_ID not in self.table['Team_ID'].values:
                columns = self.table.columns
                data = {col: 0 if ChampionshipSchema.__annotations__[col] in [int, float] else None for col in columns}
                data["Team_ID"]= row[f"{TEAM_KEY}.id"]
                data["Team_Name"]= row[f"{TEAM_KEY}.name"]
                data["Team_Logo"]= row[f"{TEAM_KEY}.logo"]
                
                self.table.loc[len(self.table)] = data
            TEAMS_ID[key] = TEAM_ID
        
        return TEAMS_ID
    
    def get_results(self, row: Dict, teams_id: Dict) -> Dict:
        TEAMS_KEY = ["home", "away"]
        HOME_GOALS = row['goals.home']
        AWAY_GOALS = row['goals.away']


        for key in TEAMS_KEY:
            TEAM_ID = teams_id[key]
            team_index = self.table.index[self.table["Team_ID"] == TEAM_ID].tolist()
            if len(team_index) == 0:
                raise ("Time não encontrado na Tabela")
            team_index = team_index[0]

            if row[f"teams.{key}.winner"] and row[f"teams.{key}.winner"] is not None:
                self.table.loc[team_index, 'Victories'] += 1
            elif not row[f"teams.{key}.winner"] and row[f"teams.{key}.winner"] is not None:
                self.table.loc[team_index, 'Defeats'] += 1
            elif HOME_GOALS > 0 and AWAY_GOALS == HOME_GOALS:
                self.table.loc[team_index, 'Draws_With_Goals'] += 1
            elif HOME_GOALS == 0 and AWAY_GOALS == HOME_GOALS:
                self.table.loc[team_index, 'Draws_Without_Goals'] += 1
            else:
                raise ValueError("Não foi possível obter o resultado.")
    
    def show_table(self):
        print(self.table)