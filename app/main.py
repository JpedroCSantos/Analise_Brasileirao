import os
import pandas as pd
import glob

from pathlib import Path
from dotenv import load_dotenv
from api.consult import FootballAPI
from pipeline.extract import read_file
from pipeline.transform import build_dataframe, create_compiled_dataframe
from pipeline.load import load_files


load_dotenv(dotenv_path="env/.env")
INPUT_DATA_PATH     = "data/input/"
DATA_PATH           = "data/output"
FINAL_PATH          = f"{DATA_PATH}"
TEMP_PARQUET_FILE   = f"{DATA_PATH}/TEMP_DATAFRAME.parquet"
FINAL_FILE_NAME     = "SEASON_RESULTS"

PARAMS = {
    "CONSULT_API": True,
    "READ_FILE": False,
    "BUILD_VIZUALISATION": True
}
if any(PARAMS.values()):
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
            result = football_api.search(params = params, endpoint = end_point)
            if not result or not result["response"]:
                continue
            df_season = build_dataframe(result["response"])
            load_files(df_season, FINAL_PATH, f"{season}_SEASON_RESULTS")
            data_frames.append(df_season)

    elif PARAMS['READ_FILE']:
        seasons = ['2021', '2022', '2023']
        data_frames = []

        for season in seasons:
            json_content = read_file(
                path="data/input", 
                file_name = f"season_{season}.json", 
                encoding=True
            )
            df_season = build_dataframe(json_content["response"])
            data_frames.append(df_season)
            load_files(df_season, FINAL_PATH, f"{season}_SEASON_RESULTS")

    compiled_df = create_compiled_dataframe(data_frames)
    load_files(compiled_df, FINAL_PATH, "COMPILED_TEAMS_RESULTS")