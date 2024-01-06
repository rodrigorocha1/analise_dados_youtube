import os
from typing import List
import pandas as pd


class GeradorConsultaTrends:
    def __init__(self, nome_arquivo: str, colunas_dataframe: List[str]) -> None:
        self.__caminho_base = os.getcwd()
        self.__caminho_completo = os.path.join(
            self.__caminho_base, "data", "ouro_csv", "trends", nome_arquivo
        )
        self.__colunas = colunas_dataframe
        self.__base = pd.read_parquet(self.__caminho_completo, columns=self.__colunas)
