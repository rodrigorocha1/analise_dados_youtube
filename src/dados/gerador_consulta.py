import pandas as pd
from typing import Tuple, Dict
from datetime import date
import os


class GeradorConsulta:

    def __init__(self, assunto: str, metricas: str, nome_arquivo: str) -> None:
        self.__caminho_base = os.getcwd()
        self.__caminho_completo = os.path.join(
            self.__caminho_base, 'data', 'projetos_youtube_v2', 'ouro', assunto, metricas, nome_arquivo)

    def __indice_semana(self, dia: str) -> int | None:
        dias_semana = {
            'Domingo': 1,
            'Segunda-feira': 2,
            'Terça-feira': 3,
            'Quarta-feira': 4,
            'Quinta-feira': 5,
            'Sexta-feira': 6,
            'Sábado': 7
        }

        return dias_semana.get(dia)

    def gerar_consulta_publicacao_video(self) -> pd.DataFrame:
        tipos = {
            'SEMANA_TRADUZIDA': 'string',
            'NM_CANAL': 'string',
            'TOTAL_VIDEOS': 'int32',
            'DATA_PUBLICACAO': 'datetime64[ns]',
        }
        colunas = ['SEMANA_TRADUZIDA', 'NM_CANAL', 'TOTAL_VIDEOS',
                   'DATA_PUBLICACAO']

        dataframe = pd.read_parquet(
            self.__caminho_completo,
            columns=colunas,

        )
        dataframe[['SEMANA_TRADUZIDA', 'NM_CANAL']] = dataframe[[
            'SEMANA_TRADUZIDA', 'NM_CANAL']].astype('string')
        dataframe['DATA_PUBLICACAO'] = dataframe['DATA_PUBLICACAO'].astype(
            'datetime64')

        dataframe['TOTAL_VIDEOS'] = dataframe['TOTAL_VIDEOS'].astype('int32')

        dataframe = dataframe.groupby('SEMANA_TRADUZIDA').sum(
            'TOTAL_VIDEOS').reset_index()

        dataframe['INDICE_SEMANA'] = dataframe['SEMANA_TRADUZIDA'].apply(
            self.__indice_semana)

        dataframe.sort_values(by='INDICE_SEMANA', inplace=True)
        dataframe.drop(['INDICE_SEMANA'], axis=1, inplace=True)
        return dataframe

    def gerar_indicadores(
            self,
            id_canal: str,
            data_fim: date,
            coluna: str
    ):
        colunas = [
            coluna,
            'data_extracao',
            'TURNO_EXTRACAO',
            'ID_CANAL'
        ]

        dataframe = pd.read_parquet(
            self.__caminho_completo,
            columns=colunas
        )

        dataframe['data_extracao'] = dataframe['data_extracao'].astype(
            'datetime64')

        dataframe[['TURNO_EXTRACAO', 'ID_CANAL']] = dataframe[[
            'TURNO_EXTRACAO', 'ID_CANAL']].astype('string')

        dataframe = dataframe[dataframe['ID_CANAL'] == id_canal]

        dataframe = dataframe.groupby('data_extracao') \
            .agg(total_visualizacoes=(coluna, 'sum')
                 ).reset_index()

        dataframe['total_visualizacoes_dia_anterior'] = dataframe['total_visualizacoes'].shift(
            1)

        dataframe.dropna(inplace=True)

        dataframe['total_visualizacoes_dia_anterior'] = dataframe['total_visualizacoes_dia_anterior'].astype(
            'float32')

        dataframe = dataframe[dataframe['data_extracao'] == str(data_fim)]

        return dataframe
