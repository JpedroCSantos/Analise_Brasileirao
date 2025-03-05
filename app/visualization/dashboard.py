import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
from io import BytesIO
from dash.dependencies import Input, Output

def run_dashboard(df_compiled_teams, season_tables):
    """
    Executa o dashboard interativo do Brasileirão.

    Parâmetros:
        df_compiled_teams (pd.DataFrame): Dados compilados para os gráficos (relacionado à Team_ID).
        season_tables (dict): Dicionário onde as chaves são anos (str) e os valores são DataFrames das temporadas.
    """

    def generate_wordcloud(df):
        word_freq = {row["Team_Name"]: row["Draws_Without_Goals"] for _, row in df.iterrows()}
        wordcloud = WordCloud(width=800, height=400, background_color="black", colormap="viridis") \
                    .generate_from_frequencies(word_freq)

        img = BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Empates Sem Gols por Time")
        plt.savefig(img, format='png', bbox_inches="tight")
        plt.close()
        return base64.b64encode(img.getvalue()).decode()

    fig_bubble = px.scatter(df_compiled_teams, x="Victories", y="Defeats", 
                            size="Draws_Without_Goals", text="Team_Name",
                            title="Gráfico de Bolhas - Empates Sem Gols",
                            hover_data={"Team_Name": True, "Victories": True, "Defeats": True, "Team_ID": True},
                            size_max=40)

    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1("Dashboard do Brasileirão"),
        
        html.Div([
            html.Label("Selecione a Temporada:"),
            dcc.Dropdown(
                id="season_selector",
                options=[{"label": year, "value": year} for year in season_tables.keys()],
                value=next(iter(season_tables.keys()))  # Primeiro ano como padrão
            )
        ], style={"width": "30%", "display": "inline-block", "margin-bottom": "20px"}),

        html.Div(children=[
            html.Div(children=[dcc.Graph(id="bubble_chart", figure=fig_bubble)], style={"width": "50%", "display": "inline-block"}),
            html.Div(children=[html.Img(id="wordcloud", src=f"data:image/png;base64,{generate_wordcloud(df_compiled_teams)}", 
                                        style={"width": "100%"})], style={"width": "50%", "display": "inline-block", "textAlign": "center"})
        ], style={"display": "flex", "justify-content": "center"}),

        html.Div(children=[
            html.H2("Tabela do Brasileirão"),
            dash_table.DataTable(
                id="season_table",
                style_table={'overflowX': 'auto', "width": "100%"},
                row_selectable="single",
                columns=[{"name": i, "id": i} for i in ["Position", "Position_1", "Position_2", "Team_Name", 
                                                        "Score_Normal", "Score_Type1", "Score_Type2",
                                                        "Draws_Without_Goals","Variation_1", "Variation_2"]],
                data=[],
                sort_action="native",  
                style_data_conditional=[

                    # Regra 1: Gradiente de cor para Position_1 e Position_2 baseado na Position
                    # 🔴🟠🟡 Se um time PERDEU posição
                    {
                        "if": {"column_id": col, "filter_query": "{%s} > {Position} && {Diff_%s} >= 4" % (col, col)},
                        "backgroundColor": "rgba(255, 0, 0, 0.7)", "color": "white"  # Vermelho (maior perda)
                    } for col in ["Position_1", "Position_2"]
                ] + [
                    {
                        "if": {"column_id": col, "filter_query": "{%s} > {Position} && {Diff_%s} < 4" % (col, col)},
                        "backgroundColor": "rgba(255, 140, 0, 0.7)", "color": "black"  # Laranja (perda média)
                    } for col in ["Position_1", "Position_2"]
                ] + [
                    {
                        "if": {"column_id": col, "filter_query": "{%s} > {Position} && {Diff_%s} < 2" % (col, col)},
                        "backgroundColor": "rgba(255, 255, 0, 0.7)", "color": "black"  # Amarelo (perda pequena)
                    } for col in ["Position_1", "Position_2"]
                ] + [
                    # 🟢🔵 Se um time GANHOU posição
                    {
                        "if": {"column_id": col, "filter_query": "{%s} < {Position} && {Diff_%s} >= 2" % (col, col)},
                        "backgroundColor": "rgba(0, 128, 0, 0.7)", "color": "white"  # Verde (maior ganho)
                    } for col in ["Position_1", "Position_2"]
                ] + [
                    {
                        "if": {"column_id": col, "filter_query": "{%s} < {Position} && {Diff_%s} < 2" % (col, col)},
                        "backgroundColor": "rgba(0, 0, 255, 0.7)", "color": "white"  # Azul (pequeno ganho)
                    } for col in ["Position_1", "Position_2"]
                ] + [
                    # Regra 2: Gradiente de cor para Score_Type1 e Score_Type2 baseado na diferença de Score_Normal
                    # 🔴🟠🟡 Se for MENOR que Score_Normal
                    {
                        "if": {"column_id": col, "filter_query": "{%s} < {Score_Normal} && {Diff_%s} >= 6" % (col, col)},
                        "backgroundColor": "rgba(255, 0, 0, 0.7)", "color": "white"  # Vermelho (maior diferença negativa)
                    } for col in ["Score_Type1", "Score_Type2"]
                ] + [
                    {
                        "if": {"column_id": col, "filter_query": "{%s} < {Score_Normal} && {Diff_%s} >= 3 && {Diff_%s} < 6" % (col, col, col)},
                        "backgroundColor": "rgba(255, 140, 0, 0.7)", "color": "black"  # Laranja (diferença média negativa)
                    } for col in ["Score_Type1", "Score_Type2"]
                ] + [
                    {
                        "if": {"column_id": col, "filter_query": "{%s} < {Score_Normal} && {Diff_%s} < 3" % (col, col)},
                        "backgroundColor": "rgba(255, 255, 0, 0.7)", "color": "black"  # Amarelo (pequena diferença negativa)
                    } for col in ["Score_Type1", "Score_Type2"]
                ] + [
                    # 🟢🔵 Se for MAIOR que Score_Normal
                    {
                        "if": {"column_id": col, "filter_query": "{%s} > {Score_Normal} && {Diff_%s} >= 5" % (col, col)},
                        "backgroundColor": "rgba(0, 128, 0, 0.7)", "color": "white"  # Verde (maior diferença positiva)
                    } for col in ["Score_Type1", "Score_Type2"]
                ] + [
                    {
                        "if": {"column_id": col, "filter_query": "{%s} > {Score_Normal} && {Diff_%s} < 5" % (col, col)},
                        "backgroundColor": "rgba(0, 0, 255, 0.7)", "color": "white"  # Azul (pequena diferença positiva)
                    } for col in ["Score_Type1", "Score_Type2"]
                ]
            )
        ], style={"margin-top": "30px"})
    ])

    @app.callback(
        Output("season_table", "data"),
        Input("season_selector", "value")
    )
    def update_table(selected_season):
        if selected_season not in season_tables:
            return []

        df = season_tables[selected_season].copy()
        df["Diff_Score_Type1"] = (df["Score_Type1"] - df["Score_Normal"]).abs()
        df["Diff_Score_Type2"] = (df["Score_Type2"] - df["Score_Normal"]).abs()
        df["Diff_Position_1"] = (df["Position"] - df["Position_1"]).abs()
        df["Diff_Position_2"] = (df["Position"] - df["Position_2"]).abs()
        df = df.sort_values(by="Position")

        return df.to_dict("records")

    app.run_server(debug=True)
