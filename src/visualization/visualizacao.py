import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


class Visualizacao:
    def __init__(self, df_resultado: pd.DataFrame) -> None:
        """Init da classe

        Args:
            df_resultado (pd.DataFrame): recebe um dataframe do pandas
        """
        self.__df_resultado = df_resultado

    def gerar_grafico_de_barras(
        self, coluna_x: str, coluna_y: str, titulo: str, altura: int
    ):
        # Gere documentação
        fig = px.bar(self.__df_resultado, x=coluna_x, y=coluna_y, text_auto=True)

        fig.update_layout(
            title_text=titulo,
            showlegend=True,
            title=dict(x=0.5, font=dict(color="white", size=12)),
            plot_bgcolor="#021E56",
            yaxis=dict(visible=False),
            margin=dict(l=20, r=20, t=40, b=20, pad=4),
            paper_bgcolor="#021E56",
            xaxis=dict(title="", tickfont=dict(color="white")),
            legend=dict(font=dict(color="white")),
            height=altura,
        )

        fig.update_traces(
            textfont_color="white", marker_color="#A343FF", textfont_size=11
        )
        return fig

    def gerar_tabela_desempenho(self, titulo: str, coluna_analise: str, altura: int):
        fig = px.line(
            self.__df_resultado,
            x="data_extracao",
            y=coluna_analise,
            title=titulo,
            markers=True,
        )

        fig.update_xaxes(title="", tickformat="%d/%m/%Y")

        fig.update_yaxes(title="")

        fig.update_layout(
            showlegend=True,
            title=dict(x=0.5, font=dict(color="white")),
            plot_bgcolor="#021E56",
            yaxis=dict(visible=True, tickfont=dict(color="white"), showgrid=True),
            margin=dict(l=20, r=20, t=40, b=20, pad=4),
            paper_bgcolor="#021E56",
            xaxis=dict(title="", tickfont=dict(color="white"), showgrid=False),
            legend=dict(font=dict(color="white")),
            height=altura,
        )

        return fig

    def gerar_grafico_barras_agrupado(self, coluna_analise: str, titulo_grafico: str):
        # cores = ['#FFA500', '#00FF00', '#FF00FF']
        fig = px.bar(
            data_frame=self.__df_resultado,
            x="data_extracao",
            y=coluna_analise,
            color="TURNO_EXTRACAO",
            barmode="group",
            text_auto=True
            # color_discrete_sequence=cores
        )
        fig.update_layout(
            title_text=titulo_grafico,
            showlegend=True,
            title=dict(x=0.5, font=dict(color="white")),
            plot_bgcolor="#021E56",
            yaxis=dict(visible=False),
            margin=dict(l=20, r=20, t=40, b=30, pad=4),
            paper_bgcolor="#021E56",
            xaxis=dict(title="", tickfont=dict(color="white", size=10)),
            legend=dict(font=dict(color="white")),
            xaxis_tickformat="%d/%m/%Y",
            bargap=0.4,
        )
        fig.update_traces(
            textfont_color="white",
            # marker_color='#246DFB',
            textfont_size=12,
            textposition="outside",
        )
        return fig

    def gerar_grafico_barra_horizontal(
        self, coluna_x: str, coluna_y: str, titulo: str, altura: int
    ):
        fig = px.bar(
            self.__df_resultado,
            x=coluna_x,
            y=coluna_y,
            orientation="h",
            text_auto=True,
            category_orders={"ID_CANAL": self.__df_resultado["ID_CANAL"]},
        )
        fig.update_layout(
            title_text=titulo,
            showlegend=True,
            height=altura,
            title=dict(x=0.5, font=dict(color="white")),
            plot_bgcolor="#021E56",
            margin=dict(l=10, r=20, t=40, b=20, pad=2),
            paper_bgcolor="#021E56",
            yaxis=dict(
                title="",
                tickfont=dict(color="white", size=13),
                tickmode="array",
                ticklen=1,
            ),
            xaxis=dict(title="", tickfont=dict(color="white"), visible=False),
            legend=dict(font=dict(color="white"), orientation="h", y=4),
        )

        fig.update_traces(
            textfont_color="white",
            marker_color="#00b3FF",
            textfont_size=14,
            textposition="auto",
        )
        return fig
