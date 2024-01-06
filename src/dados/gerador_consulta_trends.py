import os
from typing import List
import pandas as pd


class GeradorConsultaTrends:
    def __init__(self, nome_arquivo: str) -> None:
        self.__caminho_base = os.getcwd()
        self.__caminho_completo = os.path.join(
            self.__caminho_base, "data", "ouro_csv", "trends", nome_arquivo
        )
        self.__base = pd.read_parquet(self.__caminho_completo)

    def obter_perfomance(self, data: str) -> pd.DataFrame:
        dataframe = self.__base.query(f" DATA_EXTRACAO == '{data}' ")
        return dataframe
