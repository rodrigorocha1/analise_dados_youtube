from airflow.models import Variable
import requests


def checar_url(url: str, key: str):
    params = {
        'part': 'snippet',
        'regionCode': 'BR',
        'key':  key

    }
    url = url + '/videoCategories/'
    req = requests.get(url, params=params)
    print('status code', req.status_code)
    if req.status_code == 200:
        return True
    return False


if checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube')):
    print('key_youtube')
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube')
elif checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube_dois')):
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube_dois')
    print('key_youtube_dois')
elif checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube_tres')):
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube_tres')
    print('key_youtube_tres')
elif checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube_quatro')):
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube_quatro')
    print('key_youtube_quatro')
elif checar_url(Variable.get('URL_API_YOUTUBE'), Variable.get('key_youtube_cinco')):
    url_youtube = Variable.get('URL_API_YOUTUBE')
    chave_youtube = Variable.get('key_youtube_cinco')
    print('key_youtube_quatro')
else:
    url_youtube = ''
    chave_youtube = ''
