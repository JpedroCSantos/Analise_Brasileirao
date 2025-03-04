import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

# Exemplo de dataframe com dados fictícios
data = {
    "Team_Name": ["Time A", "Time B", "Time C", "Time D"],
    "Victories": [10, 15, 8, 12],  # Eixo X
    "Goals_difference": [5, 10, -3, 7],  # Eixo Y
    "Bubble_Size": [500, 800, 400, 600],  # Tamanho das bolhas
    "Team_Logo": ["time_a.png", "time_b.png", "time_c.png", "time_d.png"]  # Caminho das imagens
}

df = pd.DataFrame(data)

# Criando a figura
fig, ax = plt.subplots(figsize=(8, 6))

# Criando bolhas no gráfico
scatter = ax.scatter(df["Victories"], df["Goals_difference"], s=df["Bubble_Size"], alpha=0.5, color="lightblue")

# Função para carregar e redimensionar imagens
def get_image(path, zoom=0.1):
    img = Image.open(path)
    return OffsetImage(img, zoom=zoom)

# Adicionando imagens dentro das bolhas
for i, row in df.iterrows():
    image = get_image(row["Team_Logo"], zoom=0.2)  # Ajuste o zoom conforme necessário
    ab = AnnotationBbox(image, (row["Victories"], row["Goals_difference"]), frameon=False)
    ax.add_artist(ab)

# Ajustes visuais
ax.set_xlabel("Vitórias")
ax.set_ylabel("Saldo de Gols")
ax.set_title("Gráfico de Bolhas com Logos dos Times")

plt.grid(True, linestyle="--", alpha=0.5)
plt.show()
