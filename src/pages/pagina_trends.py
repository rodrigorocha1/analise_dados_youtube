from datetime import date
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
from src.dados.gerador_consulta_trends import GeradorConsultaTrends
from src.visualization.visualizacao_trends import VisualizacaoTrends
from src.dados.depara import obter_lista_categorias_trends


dash.register_page(__name__, name="Analise Trends Brasil")


class PaginaTrends:
    def __init__(self) -> None:
        self.tela = self.__get_layout()
        self.__gerar_calbacks()

    def __gerar_layout_popularidade(self):
        return [
            html.P(
                "TOP 10 Popularidade da Categoria no dia",
                id="id_titulo_popularidade",
                className="class_titulo_div_popularidede",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Selecione o dia"), lg=6),
                    dbc.Col(
                        dcc.DatePickerSingle(
                            id="id_selecao_data_desempenho",
                            display_format="DD/MM/YYYY",
                            date=date(2023, 10, 27),
                            min_date_allowed=date(2023, 10, 15),
                            max_date_allowed=date(2023, 10, 27),
                        ),
                        lg=6,
                    ),
                ]
            ),
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Visualizações", tab_id="tab_visualizacoes_populares"
                    ),
                    dbc.Tab(label="Comentários", tab_id="tab_comentarios_populares"),
                    dbc.Tab(
                        label="Likes",
                        tab_id="tab_likes_populares",
                    ),
                ],
                id="id_tabs_desempenho_trend",
                className="class_tabs_desempenho_trend",
            ),
            html.Div(id="id_content_desempenho"),
        ]

    def __gerar_layout_desempenho_video(self):
        return [
            html.P(
                "Top 10 desempenho vídeo por categoria",
                id="id_titulo_video_categoria_trends",
                className="class_titulo_video_categoria_trensds",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Label("Selecione a categoria"), lg=3),
                    dbc.Col(
                        dbc.Select(
                            id="id_select_categoria_trends",
                            options=obter_lista_categorias_trends(),
                            value=20,
                        ),
                        lg=3,
                    ),
                    dbc.Col(
                        html.Label("Selecione o dia"),
                        lg=3,
                    ),
                    dbc.Col(
                        dcc.DatePickerSingle(
                            id="id_selecao_data_categoria_trend",
                            display_format="DD/MM/YYYY",
                            date=date(2023, 10, 27),
                            min_date_allowed=date(2023, 10, 15),
                            max_date_allowed=date(2023, 10, 27),
                        ),
                        lg=3,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Visualizações",
                                tab_id="tab_visualizacoes_categoria",
                            ),
                            dbc.Tab(
                                label="Comentários", tab_id="tab_comentarios_categoria"
                            ),
                            dbc.Tab(label="Likes", tab_id="tab_likes_categorias"),
                        ],
                        id="id_tabs_categorias_desempenho",
                        className="class_tabs_categorias_desempenho",
                    ),
                    html.Div(id="id_categorias_desempenho"),
                ]
            ),
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
                                    self.__gerar_layout_desempenho_video(),
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
        @callback(
            Output("id_content_desempenho", "children"),
            Input("id_tabs_desempenho_trend", "active_tab"),
            Input("id_selecao_data_desempenho", "date"),
        )
        def gerar_grafico_desempenho(tab: str, data_selecao_desempenho: str):
            nome_arquivo = "popularidade_categoria_trends.parquet"
            gerador_consulta_trends = GeradorConsultaTrends(nome_arquivo=nome_arquivo)
            datafame = gerador_consulta_trends.obter_perfomance(
                data=data_selecao_desempenho
            )
            if tab == "tab_visualizacoes_populares":
                datafame = datafame[
                    [
                        "NOME_CATEGORIA",
                        "DATA_EXTRACAO",
                        "ID_CATEGORIA",
                        "TOTAL_VISUALIZACOES",
                    ]
                ]
                datafame = datafame.sort_values(
                    by=["TOTAL_VISUALIZACOES"], ascending=True
                )
                datafame = datafame.head(10)
                visualizacao_trends = VisualizacaoTrends(df_resultado=datafame)
                fig = visualizacao_trends.gerar_grafico_barras_horizontal(
                    coluna_x="TOTAL_VISUALIZACOES",
                    coluna_y="NOME_CATEGORIA",
                    titulo="Desempenho de vísualizações",
                    altura=285,
                )

                return dcc.Graph(figure=fig)
            elif tab == "tab_comentarios_populares":
                datafame = datafame[
                    [
                        "NOME_CATEGORIA",
                        "DATA_EXTRACAO",
                        "ID_CATEGORIA",
                        "TOTAL_COMENTARIOS",
                    ]
                ]
                datafame = datafame.sort_values(
                    by=["TOTAL_COMENTARIOS"], ascending=True
                )
                datafame = datafame.head(10)
                visualizacao_trends = VisualizacaoTrends(df_resultado=datafame)
                fig = visualizacao_trends.gerar_grafico_barras_horizontal(
                    coluna_x="TOTAL_COMENTARIOS",
                    coluna_y="NOME_CATEGORIA",
                    titulo="Desempenho de Comentários",
                    altura=285,
                )
                return dcc.Graph(figure=fig)
            else:
                datafame = datafame[
                    [
                        "NOME_CATEGORIA",
                        "DATA_EXTRACAO",
                        "ID_CATEGORIA",
                        "TOTAL_LIKES",
                    ]
                ]
                datafame = datafame.sort_values(by=["TOTAL_LIKES"], ascending=True)
                datafame = datafame.head(10)
                visualizacao_trends = VisualizacaoTrends(df_resultado=datafame)
                fig = visualizacao_trends.gerar_grafico_barras_horizontal(
                    coluna_x="TOTAL_LIKES",
                    coluna_y="NOME_CATEGORIA",
                    titulo="Desempenho de Likes",
                    altura=285,
                )
                return dcc.Graph(figure=fig)

        @callback(
            Output("id_categorias_desempenho", "children"),
            Input("id_tabs_categorias_desempenho", "active_tab"),
            Input("id_select_categoria_trends", "value"),
            Input("id_selecao_data_categoria_trend", "date"),
        )
        def obter_desempenho_video_categoria(
            tabs: str, id_categoria: int, data_desepenho: str
        ):
            print("ccccc")
            print(tabs, id_categoria, data_desepenho)
            nome_arquivo = "popularidade_video_categoria.parquet"
            if tabs == "tab_visualizacoes_categoria":
                gerador_consulta_trends = GeradorConsultaTrends(
                    nome_arquivo=nome_arquivo
                )
                dataframe = gerador_consulta_trends.obter_perfomance(
                    data=data_desepenho, id_categoria=id_categoria
                )
                dataframe = dataframe.head(10)
                dataframe = dataframe.sort_values(
                    by=["TOTAL_VISUALIZACOES_DIA_ATUAL"], ascending=True
                )
                if dataframe.empty:
                    return dbc.Alert("Nenhum dado encontrado", duration=10000)
                visualizacao_trends = VisualizacaoTrends(df_resultado=dataframe)
                fig = visualizacao_trends.gerar_grafico_barras_horizontal(
                    coluna_x="TOTAL_VISUALIZACOES_DIA_ATUAL",
                    coluna_y="TITULO_VIDEO",
                    titulo="Desempenho Vídeo",
                    altura=285,
                )
                return dcc.Graph(figure=fig)


pt = PaginaTrends()
layout = pt.tela
