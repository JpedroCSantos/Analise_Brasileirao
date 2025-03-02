import os
import sys
import json
import pandas as pd

from dotenv import load_dotenv
from api.consult import FootballAPI
from pipeline.extract import read_file, json_to_dataFrame
from pipeline.transform import filter_df
from pipeline.load import load_files


load_dotenv(dotenv_path="env/.env")
INPUT_DATA_PATH     = "data/input/"
DATA_PATH           = "data/output"
FINAL_PATH          = f"{DATA_PATH}"
TEMP_PARQUET_FILE   = f"{DATA_PATH}/TEMP_DATAFRAME.parquet"
FINAL_FILE_NAME     = "SEASON_RESULTS"

PARAMS = {
    "CONSULT_API": False,
    "READ_FILE": True,
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
    data_frames= []

    for season in SEASONS:
        params = {
            'league': BRASILEIRAO_LIGA_ID,
            'season': season
        }

        data_frames.append(
            json_to_dataFrame(football_api.search(params = params, endpoint = end_point))
        )

elif PARAMS['READ_FILE']:
    seasons = ['2021', '2022', '2023']
    for season in seasons:
        json_content = read_file(
            path="data/input", 
            file_name = f"season_{season}.json", 
            encoding=True
        )
        df = json_to_dataFrame(json_content["response"], encoding=True)
        df = filter_df(df)
        load_files(df, FINAL_PATH, f"{season}_SEASON_RESULTS")