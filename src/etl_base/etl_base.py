import pandas as pd


def indice_semana(dia: str) -> int | None:
    dias_semana = {
        'Domingo': 1,
        'Segunda-feira': 2,
        'Terça-feira': 3,
        'Quarta-feira': 4,
        'Quinta-feira': 5,
        'Sexta-feira': 6,
        'Sábado': 7
    }

    return dias_semana.get(dia)


def fazer_tratamento_etl_publicacao_video(dataframe: pd.DataFrame):
    dataframe = dataframe.groupby('semana_traduzida').sum(
        'total_videos').reset_index()
    dataframe['indice_semana'] = dataframe['semana_traduzida'].apply(
        indice_semana)
    dataframe.sort_values(by='indice_semana', inplace=True)
    dataframe.drop(['indice_semana'], axis=1, inplace=True)
    return dataframe
