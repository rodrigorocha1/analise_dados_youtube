from dash import html, Dash
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Analise Estátisticas', path='/')


class DashboardEstatistica:
    def __init__(self) -> None:
        self.tela = self.__get_layout()

    def __get_layout(self):
        return html.Div(
            [
                dbc.Row(
                    [
                        html.P('Página analise estátistica',
                               style={'color': 'white'})
                    ],
                    id='id_linha_um_analise',
                    className='class_linha_analise'
                )
            ],
            id='id_main_analise',
            className='class_main_analise'
        )


de = DashboardEstatistica()
layout = de.tela
