import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "pipeline")))

from schemas.schema import TableSchema
from typing import Optional


class ChampionshipSchema(TableSchema):
    Position: int
    Position_1: int
    Position_2: int
    Team_Name: str
    Team_ID: int
    Team_Logo: Optional[str]
    Victories: int
    Draws_With_Goals: int
    Draws_Without_Goals: int
    Defeats: int
    Score_Normal: int
    Score_Type1: int
    Score_Type2: int
    Pro_goals: int
    Own_goals: int
    Goals_difference: int
    Variation_1: float
    Variation_2: float
    Position_Variation_1: float
    Position_Variation_2: float