from pyhive import hive


class ConexaoBanco:
    conexao = None

    @classmethod
    def connect(cls):
        conexao = hive.Connection(
            host='localhost',
            port=10000,
            username='rodrigo',
            database='youtube'
        )
        cls.conexao = conexao
