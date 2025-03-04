import requests
import os

from PIL import Image
from pipeline.extract import parquet_to_dataFrame


def download_image(row: dict):
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

if __name__ == "__main__":
    df_path = "data/output/COMPILED_TEAMS_RESULTS.parquet"
    df = parquet_to_dataFrame(df_path, "", True)

    for index, row in df.iterrows():
        download_image(row)