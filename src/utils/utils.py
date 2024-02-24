import os
import pickle as pk
import pandas as pd


def obter_categorias_youtube() -> pd.DataFrame:
    CAMINHO_BASE = os.getcwd()

    with open(os.path.join(CAMINHO_BASE, 'src', 'depara', 'trends', 'categoria.pkl'), 'rb') as arq:
        df_categorias = pk.load(arq)
        df_categorias['ID'] = df_categorias['ID'].astype('int32')
        df_categorias['NOME_CATEGORIA'] = df_categorias['NOME_CATEGORIA'].astype(
            'string')
    return df_categorias
