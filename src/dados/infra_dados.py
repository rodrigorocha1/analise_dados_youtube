import os
from src.dados.iinfra_dados import IInfraDados


class InfraDados(IInfraDados):
    def __init__(
        self,
        diretorio_datalake: str,
            termo_assunto: str,
            path_extracao: str,
            nome_arquivo: str,
            metrica: str = None,
    ) -> None:
        """Classe para criação do datalake

        Args:
            diretorio_datalake (str): diretório (ouro, prata, bronze)
            termo_assunto (str): termo de busca
            path_extracao (str): caminho extração
            metrica (str): metrica de análise
            nome_arquivo (str): nome arquivo
        """
        self._diretorio_datalake = diretorio_datalake
        self._termo_assunto = termo_assunto.lower()
        self._path_extracao = path_extracao
        self._metrica = metrica
        self._nome_arquivo = nome_arquivo
        self._CAMINHO_BASE = '/home/rodrigo/projetos/dados_youtube/analise_dados_youtube/data/projeto_youtube'
        self._diretorio_completo = os.path.join(
            self._CAMINHO_BASE,
            self._diretorio_datalake,
            self._termo_assunto,
            self._path_extracao,
            self._metrica
        )
