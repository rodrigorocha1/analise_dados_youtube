import pickle
import os
from datetime import datetime
from typing import List, B

global CAMINHO_BASE
CAMINHO_BASE = os.path.join(os.getcwd(), 'src', 'depara')


def obter_lista_canais() -> List[datetime.date]:
    CAMINHO_LISTA_DATA = os.path.join(CAMINHO_BASE, 'trends')
    with open(os.path.join(CAMINHO_LISTA_DATA, 'lista_datas.pkl'), 'rb') as datas:
        lista_datas = pickle.load(datas)
    return lista_datas
