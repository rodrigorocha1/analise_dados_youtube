try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
import pendulum
from airflow.operators.empty import EmptyOperator
from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from src.dados.infra_json import InfraJson
from src.dados.infra_pickle import InfraPicke
from operators.youtube_busca_operator import YoutubeBuscaOperator
from operators.youtube_busca_videos_operator import YoutubeBuscaVideoOperator
from operators.youtube_busca_respostas_operator import YoutubeBuscaRespostasOperator
from operators.youtube_busca_comentarios_operator import YoutubeBuscaComentariosOperator
from operators.youtube_busca_trends_operator import YoutubeBuscaTrendsOperator
from hook.youtube_trends_hook import YoutubeTrendsYook
from hook.youtube_busca_pesquisa_hook import YoutubeBuscaPesquisaHook
from hook.youtube_busca_video_hook import YoutubeBuscaVideoHook
from hook.youtube_busca_comentario_hook import YoutubeBuscaComentarioHook
from hook.youtube_busca_resposta_hook import YoutubeBuscaRespostaHook


data_hora_atual = pendulum.now('America/Sao_Paulo').to_iso8601_string()
data_hora_atual = pendulum.parse(data_hora_atual)
data_hora_busca = data_hora_atual.subtract(minutes=60)
data_hora_busca = data_hora_busca.strftime('%Y-%m-%dT%H:%M:%SZ')

lista_assunto = [
    'Power BI',
    'Python AND dados',
    'Cities Skylines',
    'Cities Skylines 2'
]


data = 'extracao_data_' + data_hora_busca.split('T')[0].replace('-', '_')


with DAG(
    dag_id='extracao_youtube_comentario',
    schedule_interval=None,
    catchup=False,
    start_date=pendulum.datetime(2023, 10, 22, tz='America/Sao_Paulo')
) as dag:
    task_inicio = EmptyOperator(
        task_id='task_inicio_dag',
        dag=dag
    )

    with TaskGroup('tsk_extracao_youtube_dados_videos_comentarios', dag=dag) as tg3:
        lista_task_comentarios = []
        for termo_assunto in lista_assunto:
            id_termo_assunto = termo_assunto.replace(
                ' ', '_').lower().replace('|', '_')
            termo_assunto_pasta = termo_assunto.replace(
                ' ', '_').replace('|', '_').replace('ã', 'a').replace('ç', 'c')
            extracao_api_youtube_dados_videos_comentarios = YoutubeBuscaComentariosOperator(
                task_id=f'id_extracao_comentarios_{id_termo_assunto}',
                data_inicio=None,
                ordem_extracao=YoutubeBuscaComentarioHook(
                    data_inicio=data_hora_busca,
                    carregar_dados=InfraPicke(
                        diretorio_datalake='bronze',
                        termo_assunto=f'assunto_{termo_assunto_pasta}',
                        path_extracao='id_video',
                        metrica=None,
                        nome_arquivo='id_video.pkl'
                    )
                ),
                extracao_dados=(
                    InfraJson(
                        diretorio_datalake='bronze',
                        termo_assunto=f'assunto_{termo_assunto_pasta}',
                        path_extracao=data,
                        metrica='comentarios',
                        nome_arquivo='req_comentarios.json'
                    ),
                    InfraPicke(
                        diretorio_datalake='bronze',
                        termo_assunto=f'assunto_{termo_assunto_pasta}',
                        path_extracao='id_comentario',
                        metrica=None,
                        nome_arquivo='id_comentario.pkl'
                    )
                )
            )
            lista_task_comentarios.append(
                extracao_api_youtube_dados_videos_comentarios
            )
    with TaskGroup('tsk_extracao_youtube_dados_videos_respostas', dag=dag) as tg4:
        lista_task_respostas = []
        for termo_assunto in lista_assunto:
            termo_assunto_pasta = termo_assunto.replace(
                ' ', '_').replace('|', '_').replace('ã', 'a').replace('ç', 'c')
            id_termo_assunto = termo_assunto.replace(
                ' ', '_').lower().replace('|', '_')
            extracao_api_youtube_dados_videos_respostas = YoutubeBuscaRespostasOperator(
                task_id=f'id_extracao_resposta_comentario_{id_termo_assunto}',
                data_inicio=None,
                ordem_extracao=YoutubeBuscaRespostaHook(
                        data_inicio=data_hora_busca,
                        carregar_dados=InfraPicke(
                            diretorio_datalake='bronze',
                            termo_assunto=f'assunto_{termo_assunto_pasta}',
                            path_extracao='id_comentario',
                            metrica=None,
                            nome_arquivo='id_comentario.pkl'
                        )
                ),
                extracao_dados=None,
                extracao_unica=(
                    InfraJson(
                        diretorio_datalake='bronze',
                        termo_assunto=f'assunto_{termo_assunto_pasta}',
                        path_extracao=data,
                        metrica='resposta_comentarios',
                        nome_arquivo='resposta_comentarios.json'
                    )
                )
            )
            lista_task_respostas.append(
                extracao_api_youtube_dados_videos_respostas
            )

    task_fim = EmptyOperator(
        task_id='task_fim_dag',
        dag=dag
    )


task_inicio >> tg3
tg3 >> tg4
tg4 >> task_fim


# task_inicio >> transform_spark_submit >> task_fim
