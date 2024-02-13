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
            self.__caminho_dataframe,
            'dados',
            'ouro',
            self.__arquivo
        )

        self.__dataframe = pd.read_parquet(
            self.__caminho_completo,
            columns=self.__colunas
        )

        self.__traducao = {
            'Monday': 'Segunda-feira',
            'Tuesday': 'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira',
            'Friday': 'Sexta-feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }

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

    def gerar_publicacao_video(self, assunto: str) -> pd.DataFrame:
        base = self.__dataframe.query(
            f'ASSUNTO == "{assunto}"')

        base['DATA_PUBLICACAO'] = pd.to_datetime(
            base['DATA_PUBLICACAO']).dt.date
        base['DIA_PUBLICACAO'] = pd.to_datetime(
            base['DATA_PUBLICACAO']).dt.day_name()
        base['INDEX_DIA_PUBLICACAO'] = pd.to_datetime(
            base['DATA_PUBLICACAO']).dt.day_of_week
        base['DIA_PUBLICACAO'] = base['DIA_PUBLICACAO'].map(
            self.__traducao)
        base = base.drop_duplicates()
        base = base.groupby(['DIA_PUBLICACAO', 'INDEX_DIA_PUBLICACAO']) \
            .agg(
            TOTAL_VIDEOS_PUBLICADOS=('ID_VIDEO', 'count')
        ).sort_values(by='INDEX_DIA_PUBLICACAO').reset_index()
        return base

    def gerar_top_dez(self, assunto: str, data: str, metrica: str):
        base = self.__dataframe.query(
            f' ASSUNTO == "{assunto}" and TURNO_EXTRACAO == "Noite" and data_extracao == "{data}"')
        base['data_extracao'] = pd.to_datetime(
            base['data_extracao']).dt.tz_localize(None)
        base['data_extracao'] = base['data_extracao'].dt.date
        base['ASSUNTO'] = base['ASSUNTO'].astype('string')
        base['ID_VIDEO'] = base['ID_VIDEO'].astype('string')
        base['TURNO_EXTRACAO'] = base['TURNO_EXTRACAO'].astype('string')
        base['INDICE_TURNO_EXTRACAO'] = base['INDICE_TURNO_EXTRACAO'].astype(
            'int8')
        base[metrica] = round(base[metrica].astype('float32'), 0)
        base = base.groupby(['ID_VIDEO']).agg(
            TOTAL=(metrica, 'max')
        ).reset_index()

        base = base.nlargest(10, columns=['TOTAL'])
        return base

    def gerar_desempenho_canal(self, id_canal: List | str, metrica: str) -> pd.DataFrame:
        if isinstance(id_canal, List):
            query = f'ID_CANAL in {id_canal}'
        else:
            query = f'ID_CANAL == "{id_canal}"'
        base_canal = self.__dataframe.query(query)
        base_canal[['ID_CANAL', 'NM_CANAL', 'ID_VIDEO', 'TURNO_EXTRACAO', ]] = base_canal[[
            'ID_CANAL', 'NM_CANAL', 'ID_VIDEO', 'TURNO_EXTRACAO']].astype('string')

        base_canal['data_extracao'] = pd.to_datetime(
            base_canal['data_extracao'], format='%Y-%m-%d').dt.date
        base_canal = base_canal.groupby(['data_extracao', 'ID_CANAL', 'NM_CANAL']) \
            .agg(TOTAL=(metrica, 'max')).reset_index().sort_values(by=['NM_CANAL'])
        base_canal['TOTAL_DESLOCADO'] = (
            base_canal.groupby('NM_CANAL')['TOTAL'].shift(1))
        base_canal.fillna(0, axis=1, inplace=True)
        base_canal[['TOTAL_DESLOCADO', 'TOTAL']] = base_canal[[
            'TOTAL_DESLOCADO', 'TOTAL']].astype('float32')
        base_canal[['data_extracao', 'ID_CANAL',  'NM_CANAL']] = base_canal[[
            'data_extracao', 'ID_CANAL', 'NM_CANAL']].astype('string')
        base_canal['TOTAL_DIA'] = base_canal['TOTAL'] - \
            base_canal['TOTAL_DESLOCADO']
        base_canal.drop(['TOTAL', 'TOTAL_DESLOCADO'], axis=1, inplace=True)
        return base_canal

    def gerar_desempenho_video(self, id_video: str | List):
        if isinstance(id_video, List):
            query = f'ID_VIDEO in {id_video}'
        else:
            query = f'ID_VIDEO == "{id_video}"'
        base_video = self.__dataframe.query(query)

        base_video = base_video.groupby(['data_extracao', 'ID_VIDEO', 'TITULO_VIDEO']) \
            .agg(
            TOTAL=('TOTAL_LIKES', 'max')
        ).reset_index()
        base_video['TOTAL_DESLOCADO'] = base_video['TOTAL'].shift(1)

        base_video.fillna(0, inplace=True)
        base_video['TOTAL_DIA'] = base_video['TOTAL'] - \
            base_video['TOTAL_DESLOCADO']
        base_video.drop(['TOTAL_DESLOCADO', 'TOTAL'], axis=1, inplace=True)
        return base_video

    def __calcular_taxa_engajamento(self, linha: pd.Series):
        try:
            taxa_engajamento = (
                (linha['TOTAL_LIKES_DIAS'] + linha['TOTAL_COMENTARIOS_DIAS']) / linha['TOTAL_VISUALIZACAO_DIAS']) * 100
        except ZeroDivisionError:
            taxa_engajamento = 0
        return round(taxa_engajamento, 2)

    def gerar_top_dez_engagamento(self, assunto: str, data: str) -> pd.DataFrame:
        base_video = self.__dataframe.query(
            'ASSUNTO == "assunto_cities_skylines" and data_extracao == "2024-01-23"')
        base_video = base_video.groupby(['ID_VIDEO']) \
            .agg(
            TOTAL_LIKES=('TOTAL_LIKES', 'max'),
            TOTAL_COMENTARIOS=('TOTAL_COMENTARIOS', 'max'),
            TOTAL_VISUALIZACOES=('TOTAL_VISUALIZACOES', 'max')
        ).reset_index()
        base_video['TOTAL_VISUALIZACOES_DESLOCADO'] = base_video.groupby(
            'ID_VIDEO')['TOTAL_VISUALIZACOES'].shift(1)

        base_video['TOTAL_COMENTARIOS_DESLOCADO'] = base_video.groupby('ID_VIDEO')[
            'TOTAL_COMENTARIOS'].shift(1)
        base_video['TOTAL_LIKES_DESLOCADO'] = base_video.groupby('ID_VIDEO')[
            'TOTAL_LIKES'].shift(1)
        base_video.fillna(0, axis=1, inplace=True)
        base_video['TOTAL_LIKES_DIAS'] = base_video['TOTAL_LIKES'] - \
            base_video['TOTAL_LIKES_DESLOCADO']
        base_video['TOTAL_COMENTARIOS_DIAS'] = base_video['TOTAL_COMENTARIOS'] - \
            base_video['TOTAL_COMENTARIOS_DESLOCADO']
        base_video['TOTAL_VISUALIZACAO_DIAS'] = base_video['TOTAL_VISUALIZACOES'] - \
            base_video['TOTAL_VISUALIZACOES_DESLOCADO']
        base_video.drop(['TOTAL_LIKES', 'TOTAL_LIKES_DESLOCADO', 'TOTAL_COMENTARIOS', 'TOTAL_COMENTARIOS_DESLOCADO',
                        'TOTAL_VISUALIZACOES', 'TOTAL_VISUALIZACOES_DESLOCADO'], axis=1, inplace=True)
        base_video['TAXA_ENGAJAMENTO_DIA'] = base_video.apply(
            self.__calcular_taxa_engajamento, axis=1)
        base_video[['ID_VIDEO']] = base_video[['ID_VIDEO']].astype('string')
        base_video[['TOTAL_LIKES_DIAS', 'TOTAL_COMENTARIOS_DIAS', 'TOTAL_VISUALIZACAO_DIAS', 'TAXA_ENGAJAMENTO_DIA']] = base_video[[
            'TOTAL_LIKES_DIAS', 'TOTAL_COMENTARIOS_DIAS', 'TOTAL_VISUALIZACAO_DIAS', 'TAXA_ENGAJAMENTO_DIA']].astype('float')
        base_video = base_video.nlargest(
            10, columns=['TOTAL_VISUALIZACAO_DIAS'])
        return base_video
