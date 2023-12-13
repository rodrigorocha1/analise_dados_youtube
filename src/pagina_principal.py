from dash import Dash, html, dash
import dash
import dash_bootstrap_components as dbc


class APP:
    def __init__(self) -> None:
        self.app = Dash(
            __name__,
            use_pages=True,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.app.config['suppress_callback_exceptions'] = True
        self.app.layout = self.__get_layout()

    def __get_layout(self):
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.NavbarSimple(
                            children=[
                                dbc.NavLink(
                                    pagina['Name'],
                                    href=pagina['relative_path'],
                                    className='nav_custom'

                                ) for pagina in dash.page_registry.values()
                            ],
                            brand='Dashboard Youtube',
                            brand_href='#',

                        )
                    ],
                    id='id_barra_principal',
                    className='class_barra_principal'
                ),
                dbc.Row(
                    dash.page_container,
                    id='id_container_pages',
                    className='class_container_pagers'
                )
            ],
            className='class_main_div',
            id='id_main_div'
        )

    def rodar_servico(self):
        self.app.run_server(debug=True)


app = APP()

server = app.app.server

if __name__ == '__main__':
    app.rodar_servico()
