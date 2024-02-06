from datetime import date
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
# from src.dados.gerador_consulta_trends import GeradorConsultaTrends
# from src.visualization.visualizacao_trends import VisualizacaoTrends
# from src.dados.depara import obter_lista_categorias_trends


dash.register_page(__name__, name="Analise Assunto", path='/')


def gerar_comparacao():
    return [
        html.H5('Comparação desempenho vídeo',
                id='id_titulo_comparacao_video'),
        dbc.Checklist(
            inline=True,
            options=[
                {
                    'label': 'Visualizações',
                    'value': 'visualizacoes'
                },
                {
                    'label': 'Comentários',
                    'value': 'comentarios'
                },
                {
                    'label': 'Likes',
                    'value': 'likes'
                },

            ],
            id='id_input_desempenho'
        )
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


layout = gerar_layout_dashboard()
