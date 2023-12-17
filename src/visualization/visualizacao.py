import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Visualizacao:

    def __init__(self, df_resultado: pd.DataFrame) -> None:
        """Init da classe

        Args:
            df_resultado (pd.DataFrame): recebe um dataframe do pandas
        """
        self.__df_resultado = df_resultado

    def gerar_grafico_de_barras(self, coluna_x: str, coluna_y: str, titulo):
        # Gere documentação
        fig = px.bar(
            self.__df_resultado,
            x=coluna_x,
            y=coluna_y,
            text_auto=True
        )

        fig.update_layout(
            title_text=titulo,
            showlegend=True,
            title=dict(x=0.5, font=dict(color='white')),
            plot_bgcolor='#021E56',
            yaxis=dict(visible=False),
            margin=dict(l=20, r=20, t=40, b=20, pad=4),
            paper_bgcolor='#021E56',
            xaxis=dict(title='', tickfont=dict(color='white')),
            legend=dict(font=dict(color='white')),
        )

        fig.update_traces(
            textfont_color='white',
            marker_color='#A343FF',
            textfont_size=16
        )
        return fig

    def gerar_indicador(self, titulo: str):
        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                mode='number+delta',
                value=self.__df_resultado['total_visualizacoes'].iloc[0],
                delta={
                    'reference':  round(int(self.__df_resultado['total_visualizacoes_dia_anterior'].iloc[0]), 2),
                    'relative': True,
                    'position': 'bottom',
                    'valueformat': '.2%',
                },
                title={
                    'text': titulo,
                    'font': {'size': 14}
                }
            )
        )
        return fig
