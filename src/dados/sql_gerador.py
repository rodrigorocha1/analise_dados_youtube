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
