from airflow.models import Variable
import requests


def checar_url(url: str, key: str):
    params = {
        'part': 'snippet',
        'regionCode': 'BR',
        'key':  key

    }
    req = requests.get(url, params=params)
    if req.status_code == 200:
        return True
    return False


if checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube')):
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube')
elif checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube_dois')):
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube_dois')
else:
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube_tres')
