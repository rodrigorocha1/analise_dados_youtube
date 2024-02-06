from datetime import date
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
# from src.dados.gerador_consulta_trends import GeradorConsultaTrends
# from src.visualization.visualizacao_trends import VisualizacaoTrends
# from src.dados.depara import obter_lista_categorias_trends


dash.register_page(__name__, name="Analise Assunto", path='/')


def gerar_layout_dashboard():
    return html.Div(
        [
            dbc.Row(
                [
                    html.Div(
                        html.H3(
                            'Escolha o assunto de Análise:',
                            id='id_titulo_pprimeira_linha',
                            className='class_titulo_primeira_linha'
                        ),
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
