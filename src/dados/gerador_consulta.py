import os
from typing import List, Dict
import pandas as pd


class GeradorConsulta:
    def __init__(self, assunto: str, metricas: str, nome_arquivo: str) -> None:
        self.__caminho_base = os.getcwd()
        self.__caminho_completo = os.path.join(
            self.__caminho_base, "data", "ouro_csv", metricas, assunto, nome_arquivo
        )

    def __indice_semana(self, dia: str) -> int | None:
        dias_semana = {
            "Domingo": 1,
            "Segunda-feira": 2,
            "Terça-feira": 3,
            "Quarta-feira": 4,
            "Quinta-feira": 5,
            "Sexta-feira": 6,
            "Sábado": 7,
        }

        return dias_semana.get(dia)

    def __carregar_dataframe(
        self, colunas: List, tipos: Dict, parse_dates: List = None
    ):
        if parse_dates is not None:
            dataframe = pd.read_csv(
                self.__caminho_completo,
                usecols=colunas,
                dtype=tipos,
                sep="|",
                parse_dates=parse_dates,
            )
        else:
            dataframe = pd.read_csv(
                self.__caminho_completo,
                usecols=colunas,
                dtype=tipos,
                sep="|",
            )
        return dataframe

    def gerar_consulta_publicacao_video(self) -> pd.DataFrame:
        tipos = {
            "SEMANA_TRADUZIDA": "string",
            "NM_CANAL": "string",
            "TOTAL_VIDEOS": "int32",
        }
        colunas = ["SEMANA_TRADUZIDA", "NM_CANAL", "TOTAL_VIDEOS", "DATA_PUBLICACAO"]
        dataframe = self.__carregar_dataframe(
            colunas=colunas, tipos=tipos, parse_dates=["DATA_PUBLICACAO"]
        )

        dataframe[["SEMANA_TRADUZIDA", "NM_CANAL"]] = dataframe[
            ["SEMANA_TRADUZIDA", "NM_CANAL"]
        ].astype("string")

        dataframe["TOTAL_VIDEOS"] = dataframe["TOTAL_VIDEOS"].astype("int32")

        dataframe = (
            dataframe.groupby("SEMANA_TRADUZIDA").sum("TOTAL_VIDEOS").reset_index()
        )

        dataframe["INDICE_SEMANA"] = dataframe["SEMANA_TRADUZIDA"].apply(
            self.__indice_semana
        )

        dataframe.sort_values(by="INDICE_SEMANA", inplace=True)
        dataframe.drop(["INDICE_SEMANA"], axis=1, inplace=True)
        return dataframe

    def gerar_indicadores(self, id_canal: str):
        colunas = [
            "data_extracao",
            "TURNO_EXTRACAO",
            "ID_CANAL",
            "TOTAL_VISUALIZACOES_TURNO",
            "TOTAL_COMENTARIOS_TURNO",
            "TOTAL_LIKES_TURNO",
        ]
        tipos = {
            "TURNO_EXTRACAO": "string",
            "ID_CANAL": "string",
            "TOTAL_VISUALIZACOES_TURNO": "float32",
            "TOTAL_COMENTARIOS_TURNO": "float32",
            "TOTAL_LIKES_TURNO": "float32",
        }
        dataframe = self.__carregar_dataframe(
            colunas=colunas, parse_dates=["data_extracao"], tipos=tipos
        )
        dataframe = dataframe[dataframe["ID_CANAL"] == id_canal]

        dataframe["data_extracao"] = pd.to_datetime(dataframe["data_extracao"]).dt.date

        dataframe[["TURNO_EXTRACAO", "ID_CANAL"]] = dataframe[
            ["TURNO_EXTRACAO", "ID_CANAL"]
        ].astype("string")

        dataframe = (
            dataframe.groupby("data_extracao")
            .agg(
                total_visualizacoes=("TOTAL_VISUALIZACOES_TURNO", "sum"),
                total_comentarios=("TOTAL_COMENTARIOS_TURNO", "sum"),
                total_likes=("TOTAL_LIKES_TURNO", "sum"),
            )
            .reset_index()
        )

        dataframe["total_visualizacoes_dia_anterior"] = dataframe[
            "total_visualizacoes"
        ].shift(1)
        dataframe["total_comentarios_dia_anterior"] = dataframe[
            "total_comentarios"
        ].shift(1)
        dataframe["total_likes_dia_anterior"] = dataframe["total_likes"].shift(1)

        dataframe["PERCENTUAL_VISUALIZACOES"] = round(
            (
                dataframe["total_visualizacoes"]
                - dataframe["total_visualizacoes_dia_anterior"]
            )
            / dataframe["total_visualizacoes_dia_anterior"]
            * 100,
            2,
        )

        dataframe["PERCENTUAL_COMENTARIOS"] = round(
            (
                dataframe["total_comentarios"]
                - dataframe["total_comentarios_dia_anterior"]
            )
            / dataframe["total_comentarios_dia_anterior"]
            * 100,
            2,
        )

        dataframe["PERCENTUAL_LIKES"] = round(
            (
                (dataframe["total_likes"] - dataframe["total_likes_dia_anterior"])
                / dataframe["total_likes_dia_anterior"]
            )
            * 100,
            2,
        )

        dataframe.drop(
            [
                "total_likes_dia_anterior",
                "total_comentarios_dia_anterior",
                "total_likes_dia_anterior",
            ],
            axis=1,
            inplace=True,
        )

        dataframe.fillna(0, axis=1, inplace=True)

        dataframe = dataframe[
            [
                "data_extracao",
                "total_visualizacoes",
                "PERCENTUAL_VISUALIZACOES",
                "total_comentarios",
                "PERCENTUAL_COMENTARIOS",
                "total_likes",
                "PERCENTUAL_LIKES",
            ]
        ]
        dataframe.dropna(inplace=True)
        dataframe["data_extracao"] = pd.to_datetime(dataframe["data_extracao"])
        dataframe["total_visualizacoes"] = dataframe["total_visualizacoes"].astype(
            "int32"
        )
        dataframe["PERCENTUAL_VISUALIZACOES"] = dataframe[
            "PERCENTUAL_VISUALIZACOES"
        ].astype("float32")

        dataframe["total_comentarios"] = dataframe["total_comentarios"].astype("int32")
        dataframe["PERCENTUAL_COMENTARIOS"] = dataframe[
            "PERCENTUAL_COMENTARIOS"
        ].astype("float32")
        dataframe["total_likes"] = dataframe["total_likes"].astype("int32")
        dataframe["PERCENTUAL_LIKES"] = dataframe["PERCENTUAL_LIKES"].astype("float32")

        return dataframe

    def obter_desempenho_video(
        self, coluna_analise: str, id_video: str, data_inicio: str, data_fim: str
    ):
        colunas = [
            "INDICE_TURNO_EXTRACAO",
            coluna_analise,
            "data_extracao",
            "TURNO_EXTRACAO",
            "ID_VIDEO",
        ]

        tipos = {
            "INDICE_TURNO_EXTRACAO": "string",
            f"{coluna_analise}": "float32",
            "TURNO_EXTRACAO": "string",
            "ID_VIDEO": "string",
        }

        dataframe = self.__carregar_dataframe(
            colunas=colunas, tipos=tipos, parse_dates=["data_extracao"]
        )
        dataframe = dataframe[
            (dataframe["ID_VIDEO"] == id_video)
            & (dataframe["data_extracao"] >= data_inicio)
            & (dataframe["data_extracao"] <= data_fim)
        ]
        dataframe = dataframe.sort_values(by=["data_extracao", "INDICE_TURNO_EXTRACAO"])

        dataframe["ID_VIDEO"] = dataframe["ID_VIDEO"].astype("string")
        dataframe["TURNO_EXTRACAO"] = dataframe["TURNO_EXTRACAO"].astype("string")
        dataframe[f"{coluna_analise}_DESLOCADO"] = round(
            dataframe[coluna_analise].shift(1), 0
        )

        dataframe[["ID_VIDEO", "TURNO_EXTRACAO"]] = dataframe[
            ["ID_VIDEO", "TURNO_EXTRACAO"]
        ].astype("string")
        dataframe.fillna("0", axis=1, inplace=True)

        dataframe[
            [coluna_analise, "INDICE_TURNO_EXTRACAO", f"{coluna_analise}_DESLOCADO"]
        ] = dataframe[
            [coluna_analise, "INDICE_TURNO_EXTRACAO", f"{coluna_analise}_DESLOCADO"]
        ].astype(
            "int32"
        )

        dataframe[["data_extracao"]] = dataframe[["data_extracao"]].astype(
            "datetime64[ns]"
        )

        dataframe[f"{coluna_analise}_VARIACAO"] = (
            dataframe[coluna_analise] - dataframe[f"{coluna_analise}_DESLOCADO"]
        )
        # dataframe = dataframe[['data_extracao', 'INDICE_TURNO_EXTRACAO', 'ID_VIDEO', coluna_analise, f'{coluna_analise}_DESLOCADO', f'{coluna_analise}_VARIACAO']]
        # print(dataframe)

        return dataframe

    def obter_desempenho_assunto_completo(self, coluna_analise: str):
        colunas = [coluna_analise, "data_extracao"]
        tipos = {
            f"{coluna_analise}": "float32",
        }
        dataframe = self.__carregar_dataframe(
            colunas=colunas, tipos=tipos, parse_dates=["data_extracao"]
        )
        dataframe = (
            dataframe.groupby("data_extracao", observed=False)
            .agg(TOTAL=(coluna_analise, "sum"))
            .reset_index()
        )
        return dataframe

    def obter_top_dez(self, data_extracao: str, coluna_analise: str):
        tipos = {
            "id_canal": "string",
            "total_visualizacoes_turno": "int32",
            f"{coluna_analise}": "float32",
        }
        colunas = ["ID_CANAL", "data_extracao", coluna_analise]

        dataframe = self.__carregar_dataframe(
            colunas=colunas, tipos=tipos, parse_dates=["data_extracao"]
        )

        dataframe = dataframe.query(f'data_extracao == "{data_extracao}"')

        df_views_canal = (
            dataframe.groupby("ID_CANAL")
            .sum(coluna_analise)
            .sort_values(by=coluna_analise, ascending=False)
            .reset_index()
        )
        df_views_canal["ID_CANAL"] = df_views_canal["ID_CANAL"].astype("string")

        return df_views_canal.head(10)

    def obter_input_canais(self, id_canal: str) -> List[Dict]:
        lista_inputs_videos = []
        tipos = {"ID_VIDEO": "string", "TITULO_VIDEO": "string", "ID_CANAL": "string"}
        colunas = ["ID_VIDEO", "TITULO_VIDEO", "ID_CANAL"]
        dataframe = self.__carregar_dataframe(colunas=colunas, tipos=tipos)
        dataframe = dataframe.query(f'ID_CANAL == "{id_canal}"')
        dataframe = dataframe[["ID_VIDEO", "TITULO_VIDEO"]]
        dataframe = dataframe.drop_duplicates()
        for _, valor in dataframe.iterrows():
            inputs_video = {"label": valor["TITULO_VIDEO"], "value": valor["ID_VIDEO"]}
            lista_inputs_videos.append(inputs_video)
        return lista_inputs_videos


if __name__ == "__main__":
    gerador_consulta = GeradorConsulta(
        assunto="assunto_cities_skylines",
        metricas="total_visualizacoes_por_semana",
        nome_arquivo="total_visualizacoes_por_semana.csv",
    )
    coluna_analise = "TOTAL_VISUALIZACOES_TURNO"
    dataframe = gerador_consulta.obter_top_dez(
        data_extracao="2023-10-26", coluna_analise=coluna_analise
    )

    print(dataframe)
    print(len(dataframe))
    print(dataframe.columns)
    print(dataframe.info())
    print()
