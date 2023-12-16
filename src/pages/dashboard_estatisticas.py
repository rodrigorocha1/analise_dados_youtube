try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from dash import html, Dash, dcc, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
from src.dados.sql_gerador import gerar_consulta_publicacao_video
from src.etl_base.etl_base import fazer_tratamento_etl_publicacao_video
from src.infra.repositorio_banco import RepositorioBanco
from src.visualization.visualizacao import Visualizacao
from src.dados.depara import *
from typing import List

dash.register_page(__name__, name='Analise Estátistica', path='/')


class DashboardEstatistica:

    def __init__(self) -> None:
        self.tela = self.__get_layout()
        self.__gerar_calbacks()

    def __obter_opcoes(self, indice_opcao: str) -> List[str] | None:
        opcoes = {
            '1': ['assunto_cities_skylines', 'Cities Skylines'],
            '2': ['assunto_cities_skylines_2', 'Cities Skylines 2'],
            '3': ['assunto_python_and_dados', 'Python e dados'],
            '4': ['assunto_power_bi', 'Power Bi']
        }
        opcao = opcoes.get(indice_opcao)
        return opcao

    def __gerar_inputs_assunto(self):
        return [
            dbc.Label(
                'Selecione o assunto de interesse',
                id='id_label_assunto',
                className='class_label_assunto',
                style={'text-align': 'center'}
            ), dbc.RadioItems(
                options=[
                    {'label': 'Cities Skylines', 'value': '1'},
                    {'label': 'Cities Skylines 2', 'value': '2'},
                    {'label': 'Python e Dados', 'value': '3'},
                    {'label': 'Power Bi', 'value': '4'}
                ],
                value='1',
                inline=True,
                id='id_input_assunto',
                style={'text-align': 'center'}
            ),
        ]

    def __get_layout(self):
        return html.Div(
            [
                dbc.Row(
                    self.__gerar_inputs_assunto(),
                    id='id_linha_selecao_assunto',
                    className='class_linha_selecao_assunto',
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id='id_grafico_historico_video',
                                className='graficos_um'
                            ),
                            lg=6
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    dcc.DatePickerSingle(
                                        date=min(obter_lista_datas()),
                                        display_format='DD/MM/YYYY',
                                        min_date_allowed=min(
                                            obter_lista_datas()
                                        ),
                                        max_date_allowed=max(
                                            obter_lista_datas()
                                        ),
                                        placeholder='Selecione uma data'

                                    ),
                                    id='id_linha_input_tempo',
                                    className='class_input_desempenho'
                                ),
                                dbc.Row(
                                    id='id_linha_input_canal',
                                    className='class_input_canal'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            'Coluna1',
                                            lg=4,
                                        ),
                                        dbc.Col(
                                            'Coluna2',
                                            lg=4,
                                        ),
                                        dbc.Col(
                                            'Coluna2',
                                            lg=4,
                                        ),
                                    ]
                                ),
                            ],
                            lg=6,
                            id='id_colunas_desempeho',
                            className='class_coluna_desempenho'
                        ),
                    ],
                    id='id_linha_graficos',
                    className='class_graficos'
                )
            ],
            id='id_main_analise',
            className='class_main_analise',

        )

    def __gerar_calbacks(self):
        @callback(
            Output('id_grafico_historico_video', 'figure'),
            Input('id_input_assunto', 'value')
        )
        def gerar_grafico_publicacao_semana(indice_assunto: str):

            assunto = self.__obter_opcoes(indice_assunto)

            sql, tipos = gerar_consulta_publicacao_video(
                assunto=assunto[0]
            )

            dataframe_resultado = RepositorioBanco.consultar_banco(
                consulta_sql=sql,
                tipos_dados=tipos
            )

            dataframe_resultado = fazer_tratamento_etl_publicacao_video(
                dataframe=dataframe_resultado
            )

            visualizacao = Visualizacao(df_resultado=dataframe_resultado)

            fig = visualizacao.gerar_grafico_de_barras(
                coluna_x='semana_traduzida',
                coluna_y='total_videos',
                titulo=f'Envio de Vídeo por semana para o assunto {assunto[1]}'
            )
            return fig


de = DashboardEstatistica()
layout = de.tela
