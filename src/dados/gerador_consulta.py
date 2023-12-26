import pandas as pd
from typing import Tuple, Dict
from datetime import date
import os


class GeradorConsulta:

    def __init__(self, assunto: str, metricas: str, nome_arquivo: str) -> None:
        self.__caminho_base = os.getcwd()
        self.__caminho_completo = os.path.join(
            self.__caminho_base, 
            'data',
            'ouro_csv',
            metricas,
            assunto,
            nome_arquivo
        )

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

        }
        colunas = ['SEMANA_TRADUZIDA', 'NM_CANAL', 'TOTAL_VIDEOS',
                   'DATA_PUBLICACAO']

        dataframe = pd.read_csv(
            self.__caminho_completo,
            usecols=colunas,
            dtype=tipos,
            sep='|',
            parse_dates=['DATA_PUBLICACAO']
        )
        dataframe[['SEMANA_TRADUZIDA', 'NM_CANAL']] = dataframe[[
            'SEMANA_TRADUZIDA', 'NM_CANAL']].astype('string')
   

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
            id_canal: str

    ):
        colunas = [

            'data_extracao',
            'TURNO_EXTRACAO',
            'ID_CANAL',
            'TOTAL_VISUALIZACOES_TURNO',
            'TOTAL_COMENTARIOS_TURNO',
            'TOTAL_LIKES_TURNO'


        ]

        dataframe = pd.read_csv(
            self.__caminho_completo,
            usecols=colunas,
            sep='|',
            parse_dates=['data_extracao']

        )
        dataframe = dataframe[dataframe['ID_CANAL'] == id_canal]

        dataframe['data_extracao'] = pd.to_datetime(
            dataframe['data_extracao']).dt.date

        dataframe[['TURNO_EXTRACAO', 'ID_CANAL']] = dataframe[[
            'TURNO_EXTRACAO', 'ID_CANAL']].astype('string')

        dataframe = dataframe.groupby('data_extracao') \
            .agg(
                total_visualizacoes=('TOTAL_VISUALIZACOES_TURNO', 'sum'),
                total_comentarios=('TOTAL_COMENTARIOS_TURNO', 'sum'),
                total_likes=('TOTAL_LIKES_TURNO', 'sum'),
        ).reset_index()

        dataframe['total_visualizacoes_dia_anterior'] = dataframe['total_visualizacoes'].shift(
            1)
        dataframe['total_comentarios_dia_anterior'] = dataframe['total_comentarios'].shift(
            1)
        dataframe['total_likes_dia_anterior'] = dataframe['total_likes'].shift(
            1)

        dataframe['PERCENTUAL_VISUALIZACOES'] = round((
            dataframe['total_visualizacoes'] -
            dataframe['total_visualizacoes_dia_anterior']
        ) / dataframe['total_visualizacoes_dia_anterior'] * 100, 2)

        dataframe['PERCENTUAL_COMENTARIOS'] = round(
            (dataframe['total_comentarios'] - dataframe['total_comentarios_dia_anterior']) / dataframe['total_comentarios_dia_anterior'] * 100, 2)

        dataframe['PERCENTUAL_LIKES'] = round((
            (dataframe['total_likes'] - dataframe['total_likes_dia_anterior']) / dataframe['total_likes_dia_anterior']) * 100, 2)

        dataframe.drop(['total_likes_dia_anterior',
                       'total_comentarios_dia_anterior', 'total_likes_dia_anterior'], axis=1, inplace=True)

        dataframe.fillna(0, axis=1, inplace=True)

        dataframe = dataframe[[
            'data_extracao',
            'total_visualizacoes',
            'PERCENTUAL_VISUALIZACOES',
            'total_comentarios',
            'PERCENTUAL_COMENTARIOS',
            'total_likes',
            'PERCENTUAL_LIKES']]
        dataframe.dropna(inplace=True)

        return dataframe

    def obter_desempenho_video(self, coluna_analise, id_video: str):
        colunas = [
            'INDICE_TURNO_EXTRACAO',
            coluna_analise,
            'data_extracao',
            'TURNO_EXTRACAO',
            'ID_VIDEO'
        ]

        dataframe = pd.read_csv(
            self.__caminho_completo,
            usecols=colunas,
            sep='|',
            parse_dates=['data_extracao']

        )
        dataframe = dataframe[dataframe['ID_VIDEO'] == id_video]

        dataframe = dataframe.sort_values(by='INDICE_TURNO_EXTRACAO')
        dataframe['ID_VIDEO'] = dataframe['ID_VIDEO'].astype('string')
        dataframe['TURNO_EXTRACAO'] = dataframe['TURNO_EXTRACAO'].astype(
            'string')

        return dataframe

    def obter_desempenho_assunto_completo(self, coluna_analise: str):
        colunas = [coluna_analise, 'data_extracao']

        dataframe = pd.read_csv(
            self.__caminho_completo,
            usecols=colunas,
            sep='|',
            parse_dates=['data_extracao']
        )     
        dataframe = dataframe.groupby('data_extracao', observed=False).agg(
            TOTAL=(coluna_analise, 'sum')
        ).reset_index()  

        return dataframe
    
    def obter_top_dez(self, data_extracao: str, coluna_analise: str):
        tipos = {
            'id_canal': 'string',
            'total_visualizacoes_turno': 'int32'
        }
        colunas = ['ID_CANAL', 'TOTAL_VISUALIZACOES_TURNO']

        dataframe = pd.read_csv(
            self.__caminho_base,
            usecols=colunas,
            dtype=tipos
        )
        df_views_canal = dataframe.groupby('id_canal') \
            .sum('total_visualizacoes_turno') \
                .sort_values(
                    by='total_visualizacoes_turno',
                      ascending=False
                      ).reset_index()

        return df_views_canal


if __name__ == '__main__':
    gerador_consulta = GeradorConsulta(
                assunto='assunto_cities_skylines',
                metricas='total_video_publicado_semana',
                nome_arquivo='total_video_publicado_semana.csv')

    dataframe_resultado = gerador_consulta.gerar_consulta_publicacao_video()
    print(dataframe_resultado)
    print()
