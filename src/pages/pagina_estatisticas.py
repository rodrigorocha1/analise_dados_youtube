try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from datetime import date
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
from src.dados.gerador_consulta import GeradorConsulta
from src.visualization.visualizacao import Visualizacao

dash.register_page(__name__, name="Analise Assunto", path='/')


def gerar_comparacao():
    return [
        html.H5('Comparação desempenho vídeo',
                id='id_titulo_comparacao_video'),
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
        dcc.Graph(id='id_grafico_comparacao_video')
    ]


def gerar_layout_videos_publicados():
    return [
        html.H5(
            'Frequência dos vídeos públicados',
            id='id_titulo_video_publicado'
        ),
        dcc.Graph('id_video_publicado')
    ]


def gerar_layout_dashboard():
    return html.Div(
        [
            dbc.Row(
                [
                    html.Div(
                        [
                            html.H5(
                                'Escolha o assunto de Análise:',
                                id='id_titulo_pprimeira_linha',
                                className='class_titulo_primeira_linha'
                            ),
                            dbc.RadioItems(
                                options=[
                                    {
                                        'label': 'Cites Skylines',
                                        'value': 'assunto_cities_skylines'
                                    },
                                    {
                                        'label': 'Linux',
                                        'value': 'assunto_linux'
                                    },
                                    {
                                        'label': 'Power BI',
                                        'value': 'assunto_power_bi'
                                    },
                                    {
                                        'label': 'Python AND dados',
                                        'value': 'assunto_python_and_dados'
                                    },
                                    {
                                        'label': 'Cities Skylines 2',
                                        'value': 'assunto_cities_skylines_2'
                                    },
                                    {
                                        'label': 'Linux Gamming',
                                        'value': 'assunto_linux_gamming'
                                    },
                                    {
                                        'label': 'Gensim Impact',
                                        'value': 'assunto_genshin_impact'
                                    },
                                    {
                                        'label': 'Zelda',
                                        'value': 'assunto_zelda'
                                    }
                                ],
                                inline=True,
                                id='id_select_assunto',
                                value='assunto_cities_skylines'
                            )
                        ],


                        id='id_div_primeira_coluna_label_dashboard',
                        className='class_div_primeira_linha_primeira_coluna_label_dashboard'
                    )
                ],
                id='id_input_primeira_linha_dashboard',
                className='class_primeira_linha_dashboad'
            ),

            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            gerar_comparacao(),
                            id='id_div_segunda_linha_primeira_coluna_label_dashboard',
                            className='class_div_segunda_linha_primeira_coluna_label_dashboard'
                        ),
                        lg=4,
                        id='id_segunda_linha_segunda_coluna_label_dashboard',
                        className='class_segunda_linha_primeira_coluna_label_dashboard'
                    ),
                    dbc.Col(
                        html.Div(
                            gerar_layout_videos_publicados(),
                            id='id_div_segunda_linha_segunda_coluna_input_dashboard',
                            className='class_div_segunda_linha_segunda_coluna_input_dashboard'

                        ),
                        lg=4,
                        id='id_segunda_linha_segunda_coluna_input_dashboard',
                        className='class_segunda_linha_segunda_coluna_input_dashboard'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_segunda_linha_terceira_coluna_input_dashboard',
                            className='class_div_segunda_linha_terceira_coluna_input_dashboard'

                        ),
                        lg=4,
                        id='id_segunda_linha_terceira_coluna_input_dashboard',
                        className='class_segunda_linha_terceira_coluna_input_dashboard'
                    ),
                ],
                id='id_segunda_linha_input_dashboard',
                className='class_segunda_linha_name_dashboad'
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id='id_div_terceira_linha_primeira_coluna_dashboard',
                            className='class_div_terceira_linha_primeira_coluna_dashboard'
                        ),
                        lg=6,
                        id='id_terceira_linha_primeira_coluna_dashboard',
                        className='class_terceira_linha_primeira_coluna_dashboard'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_terceira_linha_segunda_coluna_dashboard',
                            className='class_div_terceira_linha_segunda_coluna_dashboard'
                        ),
                        lg=6,
                        id='id_terceira_linha_segunda_coluna_dashboard',
                        className='class_terceira_linha_segunda_coluna_dashboard'
                    )
                ],
                id='id_terceira_linha_dashboard',
                class_name='class_terceira_linha_dashboard'
            )
        ],
        id='id_main_page_dashboard',
        className='class_name_dashboard'
    )


@callback(
    Output('id_grafico_comparacao_video', 'figure'),
    Input('id_select_assunto', 'value'),
    Input('id_input_desempenho', 'value')
)
def gerar_desempenho(assunto: str, desempenho: str):
    print('assunto', assunto, 'desempenho', desempenho)
    nome_arquivo = 'dados_tratado_estatisticas_gerais.parquet'
    columns = ['ASSUNTO', 'data_extracao', 'ID_VIDEO',
               desempenho, 'TURNO_EXTRACAO', 'INDICE_TURNO_EXTRACAO']
    gerador_consulta = GeradorConsulta(arquivo=nome_arquivo, colunas=columns)

    dataframe, top_dez_max, top_dez_min, valor_maximo, valor_minimo = gerador_consulta.gerar_desempenho_dia(
        assunto=assunto, coluna_analise=desempenho)
    print(dataframe)
    visualizacao = Visualizacao(df_resultado=dataframe)
    fig = visualizacao.gerar_grafico_de_barras(
        coluna_x='data_extracao', coluna_y='TOTAL_MAX_DIA', valor_maximo=valor_maximo, valor_minimo=valor_minimo, text_anotation='teste')
    return fig


layout = gerar_layout_dashboard()
