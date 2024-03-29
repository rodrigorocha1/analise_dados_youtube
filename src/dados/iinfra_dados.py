from abc import ABC, abstractmethod


class IIIInfraDados(ABC):

    @abstractmethod
    def salvar_dados(
        self,
        **kwargs
    ):
        pass

    @abstractmethod
    def carregar_dados(self):
        pass
