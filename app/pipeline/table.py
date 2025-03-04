import os
import sys
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict


try:
    from pipeline.classes.table_class import Table
    from pipeline.schemas.table_schema import ChampionshipSchema
except ModuleNotFoundError:
    from classes.table_class import Table
    from schemas.table_schema import ChampionshipSchema


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

        goals_map = {
            "home": (HOME_GOALS, AWAY_GOALS),
            "away": (AWAY_GOALS, HOME_GOALS)
        }

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
            
            pro_goals, own_goals = goals_map[key]
            self.table.loc[team_index, 'Pro_goals'] += pro_goals
            self.table.loc[team_index, 'Own_goals'] += own_goals

    def build_classification(self) -> pd.DataFrame:
        MODELS = self.build_models()
        
        for index, team in self.table.iterrows():
            self.table.loc[index, 'Score_Normal'] = self.get_scores(team, MODELS["MODEL_DEFAULT"])
            self.table.loc[index, 'Score_Type1'] = self.get_scores(team, MODELS["MODEL_1"])
            self.table.loc[index, 'Score_Type2'] = self.get_scores(team, MODELS["MODEL_2"])
            self.table.loc[index, 'Goals_difference'] = team['Pro_goals'] - team['Own_goals']
        self.calculate_positions()
        self.calculate_variations()

    def get_scores(self, row: Dict, rules: Dict) -> pd.DataFrame:
        SCORE_KEYS = ['Victories', 'Defeats', 'Draws_With_Goals', 'Draws_Without_Goals']
        SCORE = 0
        for key in SCORE_KEYS:
            SCORE += row[key] * rules[key]

        return SCORE
    
    def build_models(self) -> dict:
        return {
            "MODEL_DEFAULT": {
                'Victories': 3,
                'Defeats': 0,
                'Draws_With_Goals': 1,
                'Draws_Without_Goals': 1
            },
            "MODEL_1": {
                'Victories': 3,
                'Defeats': 0,
                'Draws_With_Goals': 1,
                'Draws_Without_Goals': 0
            },
            "MODEL_2": {
                'Victories': 3,
                'Defeats': 0,
                'Draws_With_Goals': 2,
                'Draws_Without_Goals': 1
            },
            "MODEL_3": {
                'Victories': 4,
                'Defeats': 0,
                'Draws_With_Goals': 2,
                'Draws_Without_Goals': 1
            },
        }
    
    def calculate_positions(self):
        MODELS = {
            "Position": "Score_Normal",
            "Position_1": "Score_Type1",
            "Position_2": "Score_Type2"
        }
        
        for position_column, score_column in MODELS.items():
            self.table.sort_values(by=[score_column, 'Victories', 'Goals_difference', 'Team_Name'], 
                                  ascending=[False, False, False, True], inplace=True)
            self.table.reset_index(drop=True, inplace=True)
            self.table[position_column] = range(1, len(self.table) + 1)

    def calculate_variations(self):
        """
        Calcula as variações dos modelos alternativos em relação ao modelo de referência (MODEL_DEFAULT).
        - Variation_1: Percentual de diferença entre Score_Normal e Score_Type1.
        - Position_Variation_1: Diferença de posição entre Position e Position_1.
        - Variation_2: Percentual de diferença entre Score_Normal e Score_Type2.
        - Position_Variation_2: Diferença de posição entre Position e Position_2.
        """
        self.table["Variation_1"] = ((self.table["Score_Type1"] - self.table["Score_Normal"]) / self.table["Score_Normal"]).fillna(0)
        self.table["Position_Variation_1"] = self.table["Position"] - self.table["Position_1"]

        self.table["Variation_2"] = ((self.table["Score_Type2"] - self.table["Score_Normal"]) / self.table["Score_Normal"]).fillna(0)
        self.table["Position_Variation_2"] = self.table["Position"] - self.table["Position_2"]


    def show_table(self):
        print(self.table)


if __name__ == "__main__":
    path="data/input"
    file_name = "season_2021.json"

    from pipeline.extract import parquet_to_dataFrame
    from pipeline.load import load_files

    table = Championship_Table()
    df = parquet_to_dataFrame(
        path = "data/output", 
        file_name = "SEASON_RESULTS"
    )

    table.table = df
    table.build_classification()
    load_files(table.table, "data/output", "2021_season_test")