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
                        id='id_input_data_top_dez_categoria'
                    ),
                    lg=6
                )
            ]
        ),
        html.Div(
            dcc.Graph(id='id_grafico_layout_top_dez'),
            id='id_div_grafico_layout_top_dez'
        ),

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


@callback(
    Output('id_grafico_layout_top_dez', 'figure'),
    Input('id_input_desempenho', 'value'),
    Input('id_input_data_top_dez_categoria', 'date')
)
def obter_top_dez_categoria(desempenho: str, data: str):
    colunas = ['data_extracao', 'ID_CATEGORIA', 'TURNO_EXTRACAO',
               'INDICE_TURNO_EXTRACAO', 'ID_VIDEO', desempenho]
    nome_arquivo = 'dados_tratado_estatisticas_trends.parquet'
    gerador_consulta = GeradorConsulta(arquivo=nome_arquivo, colunas=colunas)
    dataframe = gerador_consulta.gerar_df_categorias_populares(
        data=data, metrica=desempenho)
    visualizacao = Visualizacao(df_resultado=dataframe)
    fig = visualizacao.gerar_grafico_de_barras(
        coluna_x='TOTAL_MAX',
        coluna_y='NOME_CATEGORIA',
        orientation='h',
        height=600,
        largura=600,
        texto_posicao='auto',
        category_orders={
            'NOME_CATEGORIA': dataframe['NOME_CATEGORIA'].tolist()
        },
        tickvals_y=False,

    )
    return fig


layout = gerar_layout_dashboard()
