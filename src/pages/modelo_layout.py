try:
    import sys
    import os

    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from typing import List
from datetime import date
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
from src.dados.depara import *
from src.etl_base.etl_base import *
from src.visualization.visualizacao import Visualizacao
from dados.gerador_consulta import GeradorConsulta

# dash.register_page(__name__, name="Analise Estátistica", path="/")


class DashboardEstatistica:
    def __init__(self) -> None:
        self.tela = self.__get_layout()
        self.__gerar_calbacks()

    def __obter_opcoes(self, indice_opcao: str) -> List[str] | None:
        opcoes = {
            "1": ["assunto_cities_skylines", "Cities Skylines", 2],
            "2": ["assunto_cities_skylines_2", "Cities Skylines 2", 0],
            "3": ["assunto_python_and_dados", "Python e dados", 3],
            "4": ["assunto_power_bi", "Power Bi", 1],
        }
        opcao = opcoes.get(indice_opcao)
        return opcao

    def __obter_opcao_peformance(self, opcao: int) -> str:
        if int(opcao) == 1:
            coluna_analise = "TOTAL_LIKES_TURNO"
        elif int(opcao) == 2:
            coluna_analise = "TOTAL_COMENTARIOS_TURNO"
        else:
            coluna_analise = "TOTAL_VISUALIZACOES_TURNO"
        return coluna_analise

    def __gerar_inputs_assunto(self):
        return [
            dbc.Label(
                "Selecione o assunto de interesse",
                id="id_label_assunto",
                className="class_label_assunto",
                style={"text-align": "center"},
            ),
            dbc.RadioItems(
                options=[
                    {"label": "Cities Skylines", "value": "1"},
                    {"label": "Cities Skylines 2", "value": "2"},
                    {"label": "Python e Dados", "value": "3"},
                    {"label": "Power Bi", "value": "4"},
                ],
                value="1",
                inline=True,
                id="id_input_assunto",
                style={"text-align": "center"},
            ),
        ]

    def __get_layout(self):
        return html.Div(
            [
                dbc.Row(
                    self.__gerar_inputs_assunto(),
                    id="id_linha_selecao_assunto",
                    className="class_linha_selecao_assunto",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            "Seu texto aqui", style={"color": "white"}
                                        ),
                                        dcc.Graph(id="gráfico1"),
                                    ]
                                )
                            ],
                            id="coluna1",
                            lg=4,
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        # html.P(
                                        #     "Outro texto aqui", style={"color": "white"}
                                        # ),
                                        dcc.Graph(
                                            id="gráfico2", style={"margin-top": "40px"}
                                        ),
                                    ],
                                )
                            ],
                            id="coluna2",
                            lg=4,
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            "Texto adicional", style={"color": "white"}
                                        ),
                                        dcc.Graph(id="gráfico3"),
                                    ]
                                )
                            ],
                            lg=4,
                        ),
                    ],
                    style={"border": "2px solid #ff0000", "padding": "20px"},
                ),
            ],
        )

    def __gerar_calbacks(self):
        pass


# de = DashboardEstatistica()
# layout = de.tela
