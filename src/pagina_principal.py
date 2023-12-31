from dash import Dash, dash
import dash
import dash_bootstrap_components as dbc


class APP:
    def __init__(self) -> None:
        self.app = Dash(
            __name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.app.config["suppress_callback_exceptions"] = True
        self.app.layout = self.__get_layout()

    def __get_layout(self):
        return dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.NavbarSimple(
                            children=[
                                dbc.NavLink(
                                    pagina["name"],
                                    href=pagina["relative_path"],
                                    className="nav_custom",
                                )
                                for pagina in dash.page_registry.values()
                            ],
                            brand="Dashboard Youtube",
                            className="class_nav_brand",
                            brand_href="#",
                            color="#08235A",
                            dark=True,
                        )
                    ],
                    id="id_barra_principal",
                    className="class_barra_principal",
                ),
                dbc.Row(
                    dash.page_container,
                    id="id_container_pages",
                    className="class_container_pagers",
                ),
            ],
            className="class_main_container",
            id="id_main_container",
            fluid=True,
            style={"height": "100%"},
        )

    def rodar_servico(self):
        self.app.run(debug=True, port=8051)


app = APP()

server = app.app.server

if __name__ == "__main__":
    app.rodar_servico()
