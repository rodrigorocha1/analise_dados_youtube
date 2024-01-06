import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc


dash.register_page(__name__, name="Analise Trends")


class PaginaTrends:
    def __init__(self) -> None:
        self.tela = self.__get_layout()
        self.__gerar_calbacks()

    def __gerar_layout_popularidade(self):
        return [
            html.P(
                "Popularidade",
                id="id_titulo_popularidade",
                className="class_titulo_div_popularidede",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Selecione o dia"), lg=6),
                    dbc.Col(html.Label("Selecione o dia"), lg=6),
                ]
            ),
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Visualizações", tab_id="tab_visualizacoes_populares"
                    ),
                    dbc.Tab(label="Comentários", tab_id="tab_comentarios_populares"),
                    dbc.Tab(label="Likes", tab_id="tab_likes_populares"),
                ]
            ),
            html.Div(id="id_content_desempenho"),
        ]

    def __get_layout(self):
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    self.__gerar_layout_popularidade(),
                                    id="id_div_top_dez_trends",
                                    className="class_div_top_dez_trends",
                                )
                            ],
                            lg=6,
                            id="id_top_dez_trends",
                            className="class_top_dez_trends",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [],
                                    id="id_div_popularidade_categoria",
                                    className="class_div_popularidade_categoria",
                                )
                            ],
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

    def __gerar_calbacks(self):
        pass


pt = PaginaTrends()
layout = pt.tela
