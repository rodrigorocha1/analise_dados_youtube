try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
import json
from src.dados.infra_dados import InfraDados


class InfraJson(InfraDados):
    def __init__(self, diretorio_datalake: str, termo_assunto: str,
                 path_extracao: str,
                 nome_arquivo: str,
                 metrica: str = None) -> None:
        super().__init__(diretorio_datalake, termo_assunto,
                         path_extracao, metrica, nome_arquivo)

    def salvar_dados(self, **kwargs):
        """Método para guardar json
        """

        if not os.path.exists(self._diretorio_completo):
            os.makedirs(self._diretorio_completo)

        with open(os.path.join(self._diretorio_completo, self._nome_arquivo), 'a') as arquivo_json:
            json.dump(kwargs['req'],  arquivo_json, ensure_ascii=False)
            arquivo_json.write('\n')

    def carregar_dados(self):
        pass
