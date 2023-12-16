try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from src.dados.depara import obter_lista_canais


lista_canais = obter_lista_canais()

for canal in lista_canais:
    if canal['ASSUNTO'] == 'assunto_cities_skylines_2':

        canal_valores = canal['VALORES']
        print(canal['VALORES'][0]['value'])
        print()
