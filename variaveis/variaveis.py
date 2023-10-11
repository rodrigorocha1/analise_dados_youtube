from airflow.models import Variable
# import os

url_youtube = Variable.get('URL_API_YOUTUBE')
chave_youtube = Variable.get('key_youtube')

# url_youtube = os.environ['url']
# chave_youtube = os.environ['key']
