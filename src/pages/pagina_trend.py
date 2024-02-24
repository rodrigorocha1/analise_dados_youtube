try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from datetime import date
from typing import List
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
from src.dados.gerador_consulta import GeradorConsulta
from src.visualization.visualizacao import Visualizacao
from src.dados.depara import Depara

dash.register_page(__name__, name="Analise Trends")


def gerar_layout_dashboard():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id='id_div_primeira_coluna_primeira_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=6,
                        id='id_primeira_coluna_primeira_linha_trend',
                        class_name='class_primeira_coluna_primeira_linha_trend'),
                    dbc.Col(
                        html.Div(
                            id='id_div_segunda_coluna_primeira_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=6,
                        id='id_segunda_coluna_primeira_linha_trend',
                        class_name='class_segunda_coluna_primeira_linha_trend'),
                ],
                id='id_primeira_linha_trend',
                class_name='class_primeira_linha_trend'
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id='id_div_primeira_coluna_segunda_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=6,
                        id='id_primeira_coluna_segunda_linha_trend',
                        class_name='class_primeira_coluna_segunda_linha_trend'),
                    dbc.Col(
                        html.Div(
                            id='id_div_segunda_coluna_segunda_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=6,
                        id='id_segunda_coluna_segunda_linha_trend',
                        class_name='class_segunda_coluna_segunda_linha_trend'),
                ],
                id='id_segunda_linha_trend',
                class_name='class_segunda_linha_trend'
            )
        ],
        id='id_main_page_trend',
        className='class_name_trend'
    )


layout = gerar_layout_dashboard()
