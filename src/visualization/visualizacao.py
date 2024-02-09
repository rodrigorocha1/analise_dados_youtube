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
            self,
            coluna_x: str,
            coluna_y: str,
            valor_maximo: float = None,
            valor_minimo: float = None,
            text_anotation: str = None,
            color: bool = True,
            tickfont: str = None,
            hovertemplate: str = None,
            text_update_traces: str = None
    ):
        if color:

            param_color = self.__df_resultado[coluna_y].apply(
                lambda x: 'blue' if x == valor_minimo else ('green' if x == valor_maximo else 'red'))
        else:
            param_color = None

        fig = px.bar(
            self.__df_resultado,
            x=coluna_x,
            y=coluna_y,
            text_auto='0',
            color=param_color,
        )
        fig.update_layout(
            xaxis_tickformat='%d/%m/%Y',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                showline=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
            ),
            showlegend=False,

        )
        fig.add_annotation(
            text=text_anotation,
            xref="paper",
            yref="paper",
            axref='x',
            ayref='y',
            x=0.01,
            y=1,
            ax=8,
            ay=40e3,
            showarrow=False
        )
        fig.update_traces(
            hovertemplate=hovertemplate,
            text=text_update_traces
        )
        return fig
