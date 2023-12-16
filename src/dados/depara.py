import pickle
import os
from datetime import datetime
from typing import List, Dict

global CAMINHO_BASE
CAMINHO_BASE = os.path.join(os.getcwd(), 'src', 'depara')


def obter_lista_datas() -> List[datetime.date]:
    CAMINHO_LISTA_DATA = os.path.join(CAMINHO_BASE, 'trends')
    with open(os.path.join(CAMINHO_LISTA_DATA, 'lista_datas.pkl'), 'rb') as datas:
        lista_datas = pickle.load(datas)
    return lista_datas


def obter_lista_canais():
    CAMINHO_LISTA_CANAIS = os.path.join(CAMINHO_BASE, 'outros')
    with open(os.path.join(CAMINHO_LISTA_CANAIS, 'lista_canais_depara.pkl'), 'rb') as canais:
        lista_canais = pickle.load(canais)
    return lista_canais


def obter_lista_video():
    CAMINHO_LISTA_VIDEO = os.path.join(CAMINHO_BASE, 'outros')
    with open(os.path.join(CAMINHO_LISTA_VIDEO, 'lista_video_depara.pkl'), 'rb') as canais:
        lista_canais = pickle.load(canais)
    return lista_canais
