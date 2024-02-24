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

        ],
        id='id_main_page_trend',
        className='class_name_trend'
    )


layout = gerar_layout_dashboard()
