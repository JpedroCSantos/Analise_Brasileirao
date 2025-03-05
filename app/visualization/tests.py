import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image

def plot_bubble_chart(df):
    """
    Gera um gráfico de bolhas com os logos dos times a partir de arquivos locais.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados das equipes. Deve conter as colunas:
            - "Victories": Número de vitórias
            - "Defeats": Número de derrotas
            - "Draws_Without_Goals": Número de empates sem gols
            - "Logo_File": Caminho local para o logo do time
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Normalizar os tamanhos das bolhas com base nos empates sem gols
    bubble_sizes = df["Draws_Without_Goals"] * 200

    # Criar o gráfico de bolhas
    scatter = ax.scatter(df["Victories"], df["Defeats"], s=bubble_sizes, alpha=0.5, color="blue")

    # Adicionar logos dos times a partir de arquivos locais
    for _, row in df.iterrows():
        try:
            img = Image.open(row["Logo_File"])
            img = img.resize((30, 30), Image.LANCZOS)  # Redimensionar a imagem

            # Adicionar a imagem corretamente como anotação no gráfico
            imagebox = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(imagebox, (row["Victories"], row["Defeats"]), frameon=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f"Erro ao carregar imagem para {row['Team_Name']}: {e}")

    # Configurar rótulos e título
    ax.set_xlabel("Vitórias")
    ax.set_ylabel("Derrotas")
    ax.set_title("Número de Empates Sem Gols por Equipe")

    # Exibir o gráfico
    plt.show()

# Exemplo de uso com um DataFrame contendo caminhos locais para os logos
data = {
    "Team_ID": [1062, 127, 121, 794, 131, 154],
    "Team_Name": ["Atletico-MG", "Flamengo", "Palmeiras", "RB Bragantino", "Corinthians", "Fortaleza EC"],
    "Victories": [60, 58, 63, 42, 45, 47],
    "Defeats": [26, 31, 23, 36, 32, 41],
    "Draws_Without_Goals": [8, 6, 10, 6, 7, 10],
    "Logo_File": [
        "images/1062.png",
        "images/127.png",
        "images/121.png",
        "images/794.png",
        "images/131.png",
        "images/154.png"
    ]
}

df = pd.DataFrame(data)

# Chamar a função para gerar o gráfico
plot_bubble_chart(df)
