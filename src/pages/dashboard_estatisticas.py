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

dash.register_page(__name__, name='Analise Estátistica', path='/')


class DashboardEstatistica:

    def __init__(self) -> None:
        self.tela = self.__get_layout()
        self.__gerar_calbacks()

    def __obter_opcoes(self, indice_opcao: str) -> List[str] | None:
        opcoes = {
            '1': ['assunto_cities_skylines', 'Cities Skylines', 2],
            '2': ['assunto_cities_skylines_2', 'Cities Skylines 2', 0],
            '3': ['assunto_python_and_dados', 'Python e dados', 3],
            '4': ['assunto_power_bi', 'Power Bi', 1]
        }
        opcao = opcoes.get(indice_opcao)
        return opcao
    
    def __obter_opcao_peformance(self, opcao: int) -> str:
        if int(opcao) == 1:
            coluna_analise = 'TOTAL_LIKES_TURNO'
        elif int(opcao) == 2:
            coluna_analise = 'TOTAL_COMENTARIOS_TURNO'
        else:
            coluna_analise = 'TOTAL_VISUALIZACOES_TURNO'
        return coluna_analise

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
                            [
                                 html.P(
                                    'Desempenho Geral Por Assunto',
                                    id='id_titulo_desempenho_geral',
                                    className='class_titulo_grafico'
                                ),
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            dcc.Graph(
                                                id='id_grafico_historico_video',
                                                className='graficos_um'
                                            ),
                                            label='Gráfico Envio de Vídeo por Semana',
                                            id='id_tab_historico_video'
                                        ),
                                        dbc.Tab(
                                            [
                                                dbc.RadioItems(
                                                    id='id_checklist_perfomance',
                                                    options=[
                                                        {
                                                            'label': 'Likes',
                                                            'value': '1'
                                                        },
                                                        {
                                                            'label': 'Comentários',
                                                            'value': '2'
                                                        },
                                                        {
                                                            'label': 'Visualizações',
                                                            'value': '3'
                                                        },
                                                    ],
                                                    value='1',
                                                    inline=True
                                                ),
                                               
                                                dcc.Graph(
                                                    id='id_grafico_desempenho_completo')

                                            ],
                                            label='Performance Assunto',
                                            id='id_perfomance_video',
                                        ),
                                        html.Div(id='id_grafico_visualizacao')
                                    ]
                                )
                            ],
                            lg=4,
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    'Desempenho por Canal', 
                                    id='id_titulo_desempenho', 
                                    className='class_titulo_grafico'
                                ),
                                dbc.Select(
                                    id='id_select_canais',
                                    className='class_select_canais',
                                ),
                                dbc.Tabs(
                                    [
                                        dbc.Tab(

                                            label='Análise likes',
                                            tab_id='id_tab_likes'
                                        ),
                                        dbc.Tab(

                                            label='Análise Comentários',
                                            tab_id='id_tab_comentarios'
                                        ),
                                        dbc.Tab(
                                            label='Análise Visualizações',
                                            tab_id='id_tab_visualizações'
                                        ),
                                    ],
                                    id='id_tabs_desempenho',
                                    active_tab='id_tab_likes'
                                ),
                                html.Div(id='grafico-selecionado')
                            ],
                            lg=4,
                            id='id_colunas_desempeho',
                            className='class_coluna_desempenho'
                        ),
                        dbc.Col(
                            [
                                 html.P(
                                    'TOP 10 desempenho do canal por dia', 
                                    id='id_titulo_top_dez', 
                                    className='class_titulo_grafico'
                                ),
                                dbc.RadioItems(
                                    id='id_checklist_perfomance_top_10',
                                    options=[
                                        {
                                            'label': 'Likes',
                                            'value': '1'
                                        },
                                        {
                                            'label': 'Comentários',
                                            'value': '2'
                                        },
                                        {
                                            'label': 'Visualizações',
                                            'value': '3'
                                        },
                                    ],
                                    value='1',
                                    inline=True
                                ),
                                dcc.DatePickerSingle(
                                    id='id_data_desempenho',
                                    min_date_allowed=(min(obter_lista_datas())),
                                    max_date_allowed=(max(obter_lista_datas())),
                                    display_format='DD/MM/YYYY',
                                    date=date(2023, 10, 27)
                                ),
                                dcc.Graph(id='id_grafico_top_10'),
                            ],
                            lg=4,
                        )
                    ],
                    id='id_linha_graficos',
                    className='class_graficos'
                ),
                dbc.Row(
                    [
                        html.P('Análise de desempenho do Vídeo',
                               style={'color': 'white', 'textAlign': 'center'},
                               id='id_titulo_video'
                               ),
                        dbc.Select(
                            id='id_select_canal_desempenho',
                            placeholder='Selecione o canal'

                        ),
                        dbc.Select(
                            id='id_select_video',
                        ),
                        dbc.Col(
                            [
                                dcc.DatePickerRange(
                                    display_format='DD/MM/YYYY',
                                    start_date=date(2023, 10, 15),
                                    end_date=date(2023, 10, 27),
                                    id='id_range_data',
                                    min_date_allowed=date(2023, 10, 15),
                                    max_date_allowed=date(2023, 10, 27),
                                    
                                ),
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            label='Análise likes',
                                            tab_id='id_tab_like_video',
                                           
                                        ),
                                        dbc.Tab(
                                            label='Análise Comentários',
                                            tab_id='id_tab_comentarios_video',
                                          
                                            
                                        ),
                                        dbc.Tab(
                                            label='Análise Visualizações',
                                            tab_id='id_tab_visualizacoes_video',
                                       
                                        )
                                    ],
                                    id='id_tabs_desempenho_video',
                                    className='class_tab_desempenho_video'
                                ),
                                html.Div(id='id_content_video')

                            ],
                            id='id_coluna_desempenho_video',
                            className='class_coluna_desempenho_video',
                            lg=6
                        ),
                        dbc.Col(
                            [
                                html.Iframe(
                                    width='730',
                                    height='492',
                                    id='id_video_url',
                                    style={
                                        'border': 'none',
                                        'margin-top': '10px'
                                    }
                                ),
                            ],
                            lg=6,
                            md=12,
                            xs=12
                        ),
                    ],
                    id='id_segunda_linha_dsh',
                    className='class_segunda_linha_dsh',
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
                nome_arquivo='total_video_publicado_semana.csv')

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
                # id_select_canal_desempenho
                Output('id_select_canais', 'value'),
                Output('id_select_canal_desempenho', 'options'),
                Output('id_select_canal_desempenho', 'value'),
            ],
            Input('id_input_assunto', 'value')
        )
        def trocar_input_desempenho(indice_assunto: str):
            assunto = self.__obter_opcoes(indice_assunto)
            numero_assunto = assunto[2]
            assunto = assunto[0]

            valor_padrao = obter_lista_canais(
            )[numero_assunto]['VALORES'][0]['value']
            canal_valores = obter_lista_canais()[numero_assunto]['VALORES']
            return canal_valores, valor_padrao, canal_valores, valor_padrao
        
        @callback(
            [
                Output('id_select_video', 'options'),
                Output('id_select_video', 'value')
            ],
            Input('id_select_canal_desempenho', 'value'),
            Input('id_input_assunto', 'value')   
        )
        def trocar_input_desempeho_canais_video(id_canal: str, indice_assunto: str):
            assunto = self.__obter_opcoes(indice_assunto)

            assunto = assunto[0]
            gerador_consulta = GeradorConsulta(
                assunto=assunto,
                metricas='total_visualizacoes_por_semana',
                nome_arquivo='total_visualizacoes_por_semana.csv'
                )
            lista_inputs_videos = gerador_consulta.obter_input_canais(id_canal=id_canal)
            valor_padrao = lista_inputs_videos[0]['value']
            return lista_inputs_videos, valor_padrao

        @callback(
            Output('grafico-selecionado', 'children'),
            Input('id_input_assunto', 'value'),
            Input('id_select_canais', 'value'),
            [Input('id_tabs_desempenho', 'active_tab')]

        )
        def obter_desempenho_canal(indice_assunto: str, id_canal: str, tab):
            assunto = self.__obter_opcoes(indice_assunto)
            gerador_consulta = GeradorConsulta(
                assunto=assunto[0],
                metricas='total_visualizacoes_por_semana',
                nome_arquivo='total_visualizacoes_por_semana.csv'
            )

            dataframe = gerador_consulta.gerar_indicadores(
                id_canal=id_canal,
            )

            visualizacao = Visualizacao(df_resultado=dataframe)
            if tab == 'id_tab_likes':
                titulo = 'Desempenho de likes'
                coluna_analise = 'total_likes'
                fig = visualizacao.gerar_tabela_desempenho(
                    titulo=titulo,
                    coluna_analise=coluna_analise
                )
                return dcc.Graph(figure=fig)
            elif tab == 'id_tab_comentarios':
                titulo = 'Desempenho de comentários'
                coluna_analise = 'total_comentarios'
                fig = visualizacao.gerar_tabela_desempenho(
                    titulo=titulo, coluna_analise='total_comentarios')
                return dcc.Graph(figure=fig)
            else:
                titulo = 'Desempenho de visualização'
                coluna_analise = 'total_visualizacoes'
                fig = visualizacao.gerar_tabela_desempenho(
                    titulo=titulo, coluna_analise=coluna_analise
                )
                return dcc.Graph(figure=fig)
    
        @callback(
            Output('id_content_video', 'children'),
            Input('id_input_assunto', 'value'),
            Input('id_select_video', 'value'),
            [
                Input('id_tabs_desempenho_video', 'active_tab'),
                Input('id_range_data', 'start_date'),
                Input('id_range_data', 'end_date'),
            ]
        )
        def obter_desempeho_video(indice_assunto: str, id_video: str, tab, data_inicio, data_fim ):
            assunto = self.__obter_opcoes(indice_assunto)
            gerador_consulta = GeradorConsulta(
                assunto=assunto[0],
                metricas='total_visualizacoes_por_semana',
                nome_arquivo='total_visualizacoes_por_semana.csv'
            )
            if tab == 'id_tab_like_video':
                coluna_analise = 'TOTAL_LIKES_TURNO'
                dataframe = gerador_consulta.obter_desempenho_video(
                    id_video=id_video,
                    coluna_analise=coluna_analise,
                    data_fim=data_fim,
                    data_inicio=data_inicio
                )
                if dataframe.empty:
                    return
                visualizacao = Visualizacao(df_resultado=dataframe)
                fig = visualizacao.gerar_grafico_barras_agrupado(
                    coluna_analise=coluna_analise,
                    titulo_grafico='Analise Likes',
                )

                return dcc.Graph(figure=fig)
            elif tab == 'id_tab_comentarios_video':
                coluna_analise = 'TOTAL_COMENTARIOS_TURNO'
                dataframe = gerador_consulta.obter_desempenho_video(
                    id_video=id_video,
                    coluna_analise=coluna_analise,
                    data_fim=data_fim,
                    data_inicio=data_inicio
                )
                if dataframe.empty:
                    return
                visualizacao = Visualizacao(df_resultado=dataframe)

                fig = visualizacao.gerar_grafico_barras_agrupado(
                    coluna_analise=coluna_analise,
                    titulo_grafico='Analise Comentários'
                )
                return dcc.Graph(figure=fig)
            else:
                coluna_analise = 'TOTAL_VISUALIZACOES_TURNO'
                dataframe = gerador_consulta.obter_desempenho_video(
                    id_video=id_video,
                    coluna_analise=coluna_analise,
                    data_fim=data_fim,
                    data_inicio=data_inicio
                )
                if dataframe.empty:
                    return
                visualizacao = Visualizacao(df_resultado=dataframe)

                fig = visualizacao.gerar_grafico_barras_agrupado(
                    coluna_analise=coluna_analise,
                    titulo_grafico='Analise Visualizações'
                )
                return dcc.Graph(figure=fig)

        @callback(
            Output('id_video_url', 'src'),
            Input('id_select_video', 'value'),

        )
        def gerar_url_video(id_video: str):
            return f'https://www.youtube.com/embed/{id_video}'

        @callback(
            Output('id_grafico_desempenho_completo', 'figure'),
            Input('id_input_assunto', 'value'),
            Input('id_checklist_perfomance', 'value')
        )
        def obter_desempenho_completo(id_assunto: str, id_performance: int):
            assunto = self.__obter_opcoes(id_assunto)
            gerador_consulta = GeradorConsulta(
                assunto=assunto[0],
                metricas='total_visualizacoes_por_semana',
                nome_arquivo='total_visualizacoes_por_semana.csv'
            )
            coluna_analise = self.__obter_opcao_peformance(id_performance)
            dataframe = gerador_consulta.obter_desempenho_assunto_completo(
                coluna_analise=coluna_analise)
            visualizacao = Visualizacao(df_resultado=dataframe)
            coluna_df = coluna_analise.split('_')

            dataframe.rename(columns={'TOTAL': '_'.join(coluna_df[0:2])}, inplace=True)
            fig = visualizacao.gerar_tabela_desempenho(
                titulo='Desempenho por Assunto', 
                coluna_analise='_'.join(coluna_df[0:2])
            )
            return fig
        
        @callback(
            Output('id_grafico_top_10', 'figure'),
            Input('id_input_assunto', 'value'),
            Input('id_checklist_perfomance_top_10', 'value'),
            Input('id_data_desempenho', 'date')
        )
        def obter_top_dez(id_assunto: str, id_performance: int, data_extracao: str):
        
            assunto = self.__obter_opcoes(id_assunto)
            gerador_consulta = GeradorConsulta(
                assunto=assunto[0],
                metricas='total_visualizacoes_por_semana',
                nome_arquivo='total_visualizacoes_por_semana.csv'
            )
            coluna_analise = self.__obter_opcao_peformance(id_performance)
            dataframe = gerador_consulta.obter_top_dez(
                coluna_analise=coluna_analise,
                data_extracao=data_extracao
            )
            titulo_grafico = ' '.join(dataframe.columns.values[1].split('_')[0:2])
            visualizacao = Visualizacao(df_resultado=dataframe)
            fig = visualizacao.gerar_grafico_barra_horizontal(
                coluna_x=coluna_analise,
                coluna_y='ID_CANAL',
                titulo=f'TOP 10 {titulo_grafico}'
            )
            return fig


de = DashboardEstatistica()
layout = de.tela
