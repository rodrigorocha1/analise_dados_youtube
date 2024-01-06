import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


class VisualizacaoTrends:
    def __init__(self, df_resultado: pd.DataFrame) -> None:
        """Init da classe

        Args:
            df_resultado (pd.DataFrame): recebe um dataframe do pandas
        """
        self.__df_resultado = df_resultado

    def gerar_grafico_barras_horizontal(
        self, coluna_x: str, coluna_y: str, titulo: str, altura: int
    ):
        fig = px.bar(
            self.__df_resultado,
            x=coluna_x,
            y=coluna_y,
            title=titulo,
            orientation="h",
            text_auto="0",
        )
        fig.update_layout(
            title_text=titulo,
            showlegend=False,
            title=dict(x=0.5, font=dict(color="white", size=12)),
            plot_bgcolor="#021E56",
            yaxis=dict(title="", visible=True, color="white", showline=False),
            margin=dict(l=20, r=20, t=40, b=20, pad=4),
            paper_bgcolor="#021E56",
            xaxis=dict(
                title="",
                tickfont=dict(color="white"),
                showline=False,
                visible=False,
            ),
            legend=dict(font=dict(color="white")),
            height=altura,
        )

        fig.update_traces(
            textfont_color="white", marker_color="#A343FF", textfont_size=11
        )

        return fig
