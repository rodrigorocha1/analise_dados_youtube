import os
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np


class GeradorConsulta:
    def __init__(self, arquivo: str, colunas: List[str]) -> None:
        self.__caminho_dataframe = os.getcwd()

        self.__arquivo = arquivo
        self.__colunas = colunas
        self.__caminho_completo = os.path.join(
            self.__caminho_dataframe, 'dados', 'ouro', self.__arquivo)

        self.__dataframe = pd.read_parquet(
            self.__caminho_completo, columns=self.__colunas)

    def gerar_desempenho_dia(self, assunto: str, coluna_analise: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        dataframe = self.__dataframe.query(f'ASSUNTO == "{assunto}"')
        dataframe = dataframe.query(f'ASSUNTO == "{assunto}"')
        dataframe['data_extracao'] = dataframe['data_extracao'].astype(
            'datetime64[ns]')
        dataframe.fillna(0, inplace=True)
        dataframe[coluna_analise] = dataframe[coluna_analise].astype('int32')
        dataframe['TURNO_EXTRACAO'] = dataframe['TURNO_EXTRACAO'].astype(
            'string')
        dataframe['INDICE_TURNO_EXTRACAO'] = dataframe['INDICE_TURNO_EXTRACAO'].astype(
            'string')
        dataframe['ASSUNTO'] = dataframe['ASSUNTO'].astype('string')

        dataframe = dataframe.groupby(['data_extracao', 'ID_VIDEO'])  \
            .agg(
            TOTAL_MAX=(coluna_analise, 'max')
        ).reset_index().sort_values(by='data_extracao')
        dataframe = dataframe.groupby('data_extracao') \
            .agg(
            TOTAL_MAX=(f'TOTAL_MAX', 'sum')
        ).reset_index()
        dataframe['TOTAL_MAX_DESLOCADO'] = dataframe['TOTAL_MAX'].shift(1)
        dataframe.fillna(0, inplace=True)
        dataframe['TOTAL_MAX_DIA'] = dataframe['TOTAL_MAX'] - \
            dataframe['TOTAL_MAX_DESLOCADO'].astype('int32')
        dataframe['TOTAL_MAX_DIA_DESLOCADO'] = dataframe['TOTAL_MAX_DIA'].shift(
            1)
        dataframe.fillna(0, inplace=True)
        dataframe['PERCENTUAL_VARIACAO'] = round(
            ((dataframe['TOTAL_MAX_DIA'] - dataframe['TOTAL_MAX_DIA_DESLOCADO']) / dataframe['TOTAL_MAX_DIA_DESLOCADO']) * 100, 2)
        dataframe.drop(
            ['TOTAL_MAX_DESLOCADO', 'TOTAL_MAX_DIA_DESLOCADO'], axis=1, inplace=True)
        dataframe.replace([np.inf, -np.inf], 0, inplace=True)

        top_dez_asc = dataframe.nlargest(1, columns=['PERCENTUAL_VARIACAO'])
        top_dez_desc = dataframe.nsmallest(1, columns=['PERCENTUAL_VARIACAO'])

        min_value = dataframe['TOTAL_MAX_DIA'].min()
        max_value = dataframe['TOTAL_MAX_DIA'].max()

        return dataframe, top_dez_asc, top_dez_desc, min_value, max_value
