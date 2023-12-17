try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from dash import html, Dash, dcc, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
from dados.gerador_consulta import GeradorConsulta
from src.etl_base.etl_base import *
from src.visualization.visualizacao import Visualizacao
from src.dados.depara import *
from typing import List
from datetime import datetime, timedelta, date

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
                                    [
                                        dbc.Col(
                                            dcc.DatePickerSingle(
                                                date=date(2023, 10, 21),
                                                display_format='DD/MM/YYYY',
                                                min_date_allowed=min(
                                                    obter_lista_datas()
                                                ),
                                                max_date_allowed=max(
                                                    obter_lista_datas()
                                                ),
                                                placeholder='Selecione uma data',
                                                id='id_date_desempenho'
                                            ),
                                        ),
                                        dbc.Col(
                                            dbc.Select(
                                                id='id_select_canais',
                                                className='class_select_canais',
                                            )
                                        ),
                                    ],
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
                                            [
                                                dcc.Graph(
                                                    id='id_grafico_desempenho_visualizacoes'
                                                ),
                                            ],
                                            lg=4
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id='id_grafico_desempenho_comentarios'
                                            ),
                                            lg=4
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id='id_grafico_desempenho_likes'
                                            ),
                                            lg=4
                                        ),
                                    ],
                                    className='class_desempenho',
                                    id='id_desempenho',
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
            Input('id_input_assunto', 'value'),
        )
        def gerar_grafico_publicacao_semana(indice_assunto: str):

            assunto = self.__obter_opcoes(indice_assunto)

            gerador_consulta = GeradorConsulta(
                assunto=assunto[0],
                metricas='total_video_publicado_semana',
                nome_arquivo='total_video_publicado_semana.parquet')

            dataframe_resultado = gerador_consulta.gerar_consulta_publicacao_video()
            visualizacao = Visualizacao(df_resultado=dataframe_resultado)

            fig = visualizacao.gerar_grafico_de_barras(
                coluna_x='SEMANA_TRADUZIDA',
                coluna_y='TOTAL_VIDEOS',
                titulo=f'Envio de Vídeo por semana para o assunto {assunto[1]}'
            )
            return fig

        @callback(
            [
                Output('id_select_canais', 'options'),
                Output('id_select_canais', 'value'),
            ],
            Input('id_input_assunto', 'value')
        )
        def trocar_input_desempenho(indice_assunto: str):
            assunto = self.__obter_opcoes(indice_assunto)
            assunto = assunto[0]
            for canal in obter_lista_canais():
                if canal['ASSUNTO'] == assunto:
                    canal_valores = canal['VALORES']
            valor_padrao = obter_lista_canais()[0]['VALORES'][0]['value']

            return canal_valores, valor_padrao

        @callback(
            Output('id_grafico_desempenho_visualizacoes', 'figure'),
            Input('id_input_assunto', 'value'),
            Input('id_select_canais', 'value'),
            Input('id_date_desempenho', 'date'),
        )
        def obter_desempenho(indice_assunto: str, id_canal: str, data_final: date):
            data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
            data_inicial = data_final - timedelta(days=1)
            assunto = self.__obter_opcoes(indice_assunto)

            gerador_consulta = GeradorConsulta(
                assunto=assunto[0],
                metricas='total_visualizacoes_por_semana',
                nome_arquivo='total_visualizacoes_por_semana.parquet'
            )
            coluna = 'TOTAL_VISUALIZACOES_TURNO'
            dataframe = gerador_consulta.gerar_indicadores(
                id_canal=id_canal,
                data_fim=data_final,
                coluna=coluna
            )
            if dataframe.empty:
                pass

            visalizacao = Visualizacao(df_resultado=dataframe)
            fig = visalizacao.gerar_indicador()
            return fig


de = DashboardEstatistica()

layout = de.tela
