import mplcursors
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from wordcloud import WordCloud


def buildBubbleGraph(df):
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

    # Adicionar interatividade: exibir informações ao passar o mouse sobre as bolhas
    cursor = mplcursors.cursor(scatter, hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        index = sel.index
        team = df.iloc[index]
        sel.annotation.set_text(
            f"{team['Team_Name']}\n"
            f"Vitórias: {team['Victories']}\n"
            f"Derrotas: {team['Defeats']}\n"
            f"Empates com gols: {team['Draws_With_Goals']}\n"
            f"Empates sem gols: {team['Draws_Without_Goals']}"
        )
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)  # Fundo branco semitransparente

    # Exibir o gráfico
    plt.show()

def generate_wordcloud(df):
    """
    Gera um gráfico de nuvem de palavras onde o tamanho do nome do time
    é proporcional ao número de empates sem gols.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados das equipes. Deve conter as colunas:
            - "Team_Name": Nome do time
            - "Draws_Without_Goals": Número de empates sem gols
    """
    # Criando um dicionário com os times e a quantidade de empates sem gols
    word_freq = {row["Team_Name"]: row["Percent_Draws_Without_Goals"] for _, row in df.iterrows()}

    # Criando a nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color="black", colormap="viridis",
                          normalize_plurals=True).generate_from_frequencies(word_freq)

    # Exibir a nuvem de palavras
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Empates Sem Gols por Time (Tamanho proporcional ao número de empates)")
    plt.show()

def generate_table(df):
    """
    Gera uma tabela formatada no estilo do Brasileirão, destacando as variações de posição e pontuação.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo as colunas:
            - "Position"
            - "Position_1"
            - "Position_2"
            - "Team_Name"
            - "Victories"
            - "Draws_With_Goals"
            - "Draws_Without_Goals"
            - "Defeats"
            - "Score_Normal"
            - "Score_Type1"
            - "Score_Type2"
            - "Variation_1"
            - "Variation_2"
            - "Position_Variation_1"
            - "Position_Variation_2"
    """
    # Criar uma função para colorir células com base na variação de posição
    def color_positions(val):
        if val > 0:
            color = f"rgba(0, 200, 0, {min(val / 10, 1)})"  # Verde crescente
        elif val < 0:
            color = f"rgba(200, 0, 0, {min(abs(val) / 10, 1)})"  # Vermelho crescente
        else:
            color = "white"
        return f"background-color: {color}"

    # Criar uma função para colorir células com base nos Scores e Variações
    def color_scores(val):
        min_val, max_val = df["Score_Normal"].min(), df["Score_Normal"].max()
        norm_val = (val - min_val) / (max_val - min_val) if max_val > min_val else 0
        return f"background-color: rgba(0, 0, 255, {norm_val})"  # Azul crescente

    # Aplicar estilos à tabela
    styled_table = df.style.applymap(color_positions, subset=["Position_1", "Position_2", "Position_Variation_1", "Position_Variation_2"]) \
                            .applymap(color_scores, subset=["Score_Normal", "Score_Type1", "Score_Type2", "Variation_1", "Variation_2"])

    styled_table

def buildGraphs(df):
    """
    Gera um gráfico de bolhas com os logos dos times e exibe informações ao passar o mouse sobre as bolhas.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados das equipes. Deve conter as colunas:
            - "Victories": Número de vitórias
            - "Defeats": Número de derrotas
            - "Draws_With_Goals": Número de empates com gols
            - "Draws_Without_Goals": Número de empates sem gols
            - "Logo_File": Caminho local para o logo do time
    """
    buildBubbleGraph(df)
    generate_wordcloud(df)

if __name__ == "__main__":
    df = pd.read_parquet("data/output/COMPILED_TEAMS_RESULTS.parquet")
    buildGraphs(df)