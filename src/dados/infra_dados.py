import os
from src.dados.iinfra_dados import IInfraDados


class InfraDados(IInfraDados):
    def __init__(
        self,
        diretorio_datalake: str,
            termo_assunto: str,
            data_extracao: str,
            metrica: str,
            nome_arquivo
    ) -> None:
        """Classe para criação do datalake

        Args:
            diretorio_datalake (str): camada do datalake (bronze, prata, ouro)
            termo_assunto (str): termo de assunto de pesquisa
            data_extracao (str): data_de_extracao
            metrica (str): metrica para salvar no diretório
        """
        self._diretorio_datalake = diretorio_datalake
        self._termo_assunto = termo_assunto.lower()
        self._data_extracao = data_extracao
        self._metricas = metrica
        self._nome_arquivo = nome_arquivo
        self._CAMINHO_BASE = '/home/rodrigo/projetos/dados_youtube/analise_dados_youtube/data/projeto_youtube'
        self._diretorio_completo = os.path.join(
            self._CAMINHO_BASE,
            self._diretorio_datalake,
            self._termo_assunto,
            self._data_extracao,
            self._metricas
        )
