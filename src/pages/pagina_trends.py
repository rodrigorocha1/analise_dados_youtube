import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc


dash.register_page(__name__, name="Analise Trends")


class PaginaTrends:
    def __init__(self) -> None:
        self.tela = self.__get_layout()
        self.__gerar_calbacks()

    def __get_layout(self):
        pass

    def __gerar_calbacks(self):
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [],
                            lg=6,
                            id="id_top_dez_trends",
                            className="class_top_dez_trends",
                        ),
                        dbc.Col(
                            [],
                            id="id_popularidade_categoria",
                            className="class_popularidade_categoria",
                            lg=6,
                        ),
                    ],
                    id="id_primeira_linha_trends",
                    className="class_linha_trends",
                )
            ],
            id="id_main_trends",
            className="class_name_trends",
        )


pt = PaginaTrends()
layout = pt.tela
