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
                    dbc.Col(
                        html.Div(
                            id='id_div_primeira_coluna_label_dashboard',
                            className='class_div_primeira_coluna_label_dashboard'
                        ),
                        lg=6,
                        id='id_primeira_coluna_label_dashboard',
                        className='class_primeira_coluna_label_dashboard'
                    ),
                    dbc.Col(
                        html.Div(
                            id='id_div_segunda_coluna_input_dashboard',
                            className='class_div_segunda_coluna_input_dashboard'

                        ),
                        lg=6,
                        id='id_segunda_coluna_input_dashboard',
                        className='class_segunda_coluna_input_dashboard'),
                ],
                id='id_input_dashboard',
                className='class_name_dashboad'
            )
        ],
        id='id_main_page_dashboard',
        className='class_name_dashboard'
    )


layout = gerar_layout_dashboard()
