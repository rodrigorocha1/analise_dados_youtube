import pandas as pd
from typing import Tuple, Dict


def gerar_consulta_publicacao_video(assunto: str) -> Tuple[str, Dict]:
    tipos = {
        'semana_traduzida': 'string',
        'nm_canal': 'string',
        'total_videos': 'int32',
        'data_publicacao': 'datetime64[ns]',
    }

    sql = 'SELECT semana_traduzida, ' \
        ' nm_canal,  ' \
        ' total_videos, ' \
        ' data_publicacao ' \
        ' FROM youtube.total_video_publicado_semana' \
        f' WHERE assunto = "{assunto}" '
    return sql, tipos


def gerar_consulta_desempenho(id_canal: str, data_extracao_final: str, data_extracao_inicial):
    data_extracao = str(data_extracao_final) + '" , "' + \
        str(data_extracao_inicial)
    tipos = {
        'data_extracao':  'datetime64[ns]',
        'total_visualizacoes_turno': 'int32',
        'turno_extracao': 'string',

    }
    sql_query = ' SELECT data_extracao, ' \
        ' turno_extracao, ' \
        ' total_visualizacoes_turno ' \
        ' FROM youtube.TOTAL_VISUALIZACOES_POR_SEMANA ' \
        ' where assunto = "assunto_cities_skylines" '  \
        f' AND ID_CANAL="{id_canal}" ' \
        f' AND  data_extracao in ("{data_extracao}") '

    return sql_query, tipos
