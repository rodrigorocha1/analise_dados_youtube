from dash import html, Dash, dcc
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
                        dbc.Label(
                            'Selecione o assunto de interesse',
                            id='id_label_assunto',
                            className='class_label_assunto',
                            style={'text-align': 'center'}
                        ),
                        dbc.RadioItems(
                            options=[
                                {'label': 'Cities Skylines', 'value': 1},
                                {'label': 'Cities Skylines 2', 'value': 2},
                                {'label': 'Python e Dados', 'value': 3},
                                {'label': 'Power Bi', 'value': 4}
                            ],
                            inline=True,
                            id='id_input_assunto',
                            style={'text-align': 'center'}
                        ),
                    ],
                    id='id_linha_selecao_assunto',
                    className='class_linha_selecao_assunto',
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id='grafico_1', className='graficos_um'),
                            lg=4
                        ),
                        dbc.Col(
                            dcc.Graph(id='grafico_2', className='graficos_um'),
                            lg=4
                        ),
                        dbc.Col(
                            dcc.Graph(id='grafico_1', className='graficos_um'),
                            lg=4
                        ),
                    ],
                    id='id_linha_graficos',
                    className='class_graficos'
                )
            ],
            id='id_main_analise',
            className='class_main_analise',

        )


de = DashboardEstatistica()
layout = de.tela
