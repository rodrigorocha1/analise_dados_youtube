try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
import pickle
from typing import List
from src.dados.infra_dados import InfraDados


class InfraPicke(InfraDados):

    def __init__(
        self, diretorio_datalake: str,
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
            nome_arquivo (str): nome do arquivo que ira ser salvo
        """
        super().__init__(diretorio_datalake, termo_assunto,
                         data_extracao, metrica, nome_arquivo)

    def salvar_dados(self, **kwargs):
        """Método para guardar lista de vídeos str
        """

        if not os.path.exists(self._diretorio_completo):
            os.makedirs(self._diretorio_completo)
            var = kwargs['lista']
        else:
            try:
                lista = self.carregar_dados()
                var = kwargs['lista'] + lista
                var = list(set(var))
            except:
                var = kwargs['lista']

        with open(os.path.join(self._diretorio_completo, self._nome_arquivo), 'wb') as arquivo_pickle:
            if arquivo_pickle is not None:
                pickle.dump(var, arquivo_pickle)

    def carregar_dados(self) -> List[str]:
        """Método para abrir os id únicos, sejá vídeos, comentários e respostas

        Returns:
            List[str]: Lista de strings
        """
        caminho = os.path.join(self._diretorio_completo, self._nome_arquivo)
        if os.path.exists(caminho):
            with open(caminho, 'rb') as arquivo_pickle:
                lista_videos = pickle.load(arquivo_pickle)
            return lista_videos
