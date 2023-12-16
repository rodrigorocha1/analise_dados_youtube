try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from src.dados.depara import obter_lista_canais


lista_canais = obter_lista_canais()
print(lista_canais, type(lista_canais[0]))
print(lista_canais, type(lista_canais[0]))
