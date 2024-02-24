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


def gerar_layout_categoria_top_dez():
    return [
        html.H5('Top 10 Categoria Populares',
                id='id_titulo_categoria_populares_trends'),
        dbc.Row(
            [
                dbc.Col(
                    dbc.RadioItems(
                        inline=True,
                        value='TOTAL_VISUALIZACOES',
                        options=[
                            {
                                'label': 'Visualizações',
                                'value': 'TOTAL_VISUALIZACOES'
                            },
                            {
                                'label': 'Comentários',
                                'value': 'TOTAL_COMENTARIOS'
                            },
                            {
                                'label': 'Likes',
                                'value': 'TOTAL_LIKES'
                            },
                        ],
                        id='id_input_desempenho',
                    ),
                    lg=6
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        date='2024-01-20',
                        display_format='DD/MM/YYYY',
                        max_date_allowed=date(2024, 1, 23),
                        min_date_allowed=date(2024, 1, 17),
                        id='id_input_data_top_dez'
                    ),
                    lg=6
                )
            ]
        ),
        dcc.Graph(id='id_grafico_layout_top_dez')
    ]


def gerar_layout_dashboard():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            gerar_layout_categoria_top_dez(),
                            id='id_div_primeira_coluna_primeira_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=4,
                        id='id_primeira_coluna_primeira_linha_trend',
                        class_name='class_primeira_coluna_primeira_linha_trend'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_segunda_coluna_primeira_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=4,
                        id='id_segunda_coluna_primeira_linha_trend',
                        class_name='class_segunda_coluna_primeira_linha_trend'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_terceira_coluna_primeira_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=4,
                        id='id_terceira_coluna_primeira_linha_trend',
                        class_name='class_terceira_coluna_primeira_linha_trend'
                    ),
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
                        lg=4,
                        id='id_primeira_coluna_segunda_linha_trend',
                        class_name='class_primeira_coluna_segunda_linha_trend'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_segunda_coluna_segunda_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=4,
                        id='id_segunda_coluna_segunda_linha_trend',
                        class_name='class_segunda_coluna_segunda_linha_trend'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_terceira_coluna_segunda_linha_trend',
                            className='class_div_coluna'
                        ),
                        lg=4,
                        id='id_terceira_coluna_segunda_linha_trend',
                        class_name='class_terceira_coluna_segunda_linha_trend'
                    ),
                ],
                id='id_segunda_linha_trend',
                class_name='class_segunda_linha_trend'
            )
        ],
        id='id_main_page_trend',
        className='class_name_trend'
    )


layout = gerar_layout_dashboard()
