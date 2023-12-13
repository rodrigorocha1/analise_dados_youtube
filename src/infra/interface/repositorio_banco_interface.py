from typing import Dict
from abc import ABC, abstractmethod
from pandas import DataFrame


class RepositorioBancoInterface(ABC):

    @abstractmethod
    def consultar_banco(self, consulta_sql: str, tipos_dados: Dict) -> DataFrame:
        pass
