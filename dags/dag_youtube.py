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
data_hora_busca = data_hora_atual.subtract(minutes=15)
data_hora_busca = data_hora_busca.strftime('%Y-%m-%dT%H:%M:%SZ')

lista_assunto = ['Cities Skylines', 'Trópico 6',
                 'Genshim impact', 'Cities Skylines 2']


data = 'extracao_data_' + data_hora_busca.split('T')[0].replace('-', '_')


with DAG(
    dag_id='extracao_youtube',
    schedule_interval=None,
    catchup=False,
    start_date=pendulum.datetime(2023, 9, 8, tz='America/Sao_Paulo')
) as dag:
    task_inicio = EmptyOperator(
        task_id='task_inicio_dag',
        dag=dag
    )
    with TaskGroup('task_youtube_api_historico_pesquisa', dag=dag) as tg1:
        lista_task_historico = []
        for termo_assunto in lista_assunto:
            id_termo_assunto = termo_assunto.replace(' ', '_').lower()
            extracao_api_youtube_historico_pesquisa = YoutubeBuscaOperator(
                task_id=f'id_youtube_api_historico_pesquisa_{id_termo_assunto}',
                data_inicio=data_hora_busca,
                ordem_extracao=YoutubeBuscaPesquisaHook(
                    data_inicio=data_hora_busca,
                    consulta=termo_assunto
                ),
                termo_consulta=termo_assunto,
                extracao_dados=(
                    InfraJson(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='requisicao_busca',
                        nome_arquivo='req_busca.json'
                    ),
                    InfraPicke(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='id_video',
                        nome_arquivo='id_video.pkl'
                    )
                )
            )
            lista_task_historico.append(
                extracao_api_youtube_historico_pesquisa
            )

    with TaskGroup('tsk_extracao_api_youtube_dados_videos_estatistica', dag=dag) as tg2:
        lista_task_dados_videos = []
        for termo_assunto in lista_assunto:
            id_termo_assunto = termo_assunto.replace(' ', '_').lower()
            extracao_api_youtube_dados_videos_estatistica = YoutubeBuscaVideoOperator(
                task_id=f'id_extracao_api_youtube_dados_videos_estatistica_{id_termo_assunto}',
                data_inicio=None,
                ordem_extracao=YoutubeBuscaVideoHook(
                    data_inicio=data_hora_busca,
                    carregar_dados=InfraPicke(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='id_video',
                        nome_arquivo='id_video.pkl'
                    )
                ),
                extracao_dados=None,
                extracao_unica=InfraJson(
                    diretorio_datalake='bronze',
                    termo_assunto=termo_assunto.replace(' ', '_'),
                    data_extracao=data,
                    metrica='estatisticas',
                    nome_arquivo='req_video.json'

                )
            )
            lista_task_dados_videos.append(
                extracao_api_youtube_dados_videos_estatistica
            )

    with TaskGroup('tsk_extracao_youtube_dados_videos_comentarios', dag=dag) as tg3:
        lista_task_comentarios = []
        for termo_assunto in lista_assunto:
            id_termo_assunto = termo_assunto.replace(' ', '_').lower()
            extracao_api_youtube_dados_videos_comentarios = YoutubeBuscaComentariosOperator(
                task_id=f'id_extracao_comentarios_{id_termo_assunto}',
                data_inicio=None,
                ordem_extracao=YoutubeBuscaComentarioHook(
                    data_inicio=data_hora_busca,
                    carregar_dados=InfraPicke(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='id_video',
                        nome_arquivo='id_video.pkl'
                    )
                ),
                extracao_dados=(
                    InfraJson(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='comentarios',
                        nome_arquivo='req_comentarios.json'
                    ),
                    InfraPicke(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='id_comentario',
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
            id_termo_assunto = termo_assunto.replace(' ', '_').lower()
            extracao_api_youtube_dados_videos_respostas = YoutubeBuscaRespostasOperator(
                task_id=f'id_extracao_resposta_comentario_{id_termo_assunto}',
                data_inicio=None,
                ordem_extracao=YoutubeBuscaRespostaHook(
                        data_inicio=data_hora_busca,
                        carregar_dados=InfraPicke(
                            diretorio_datalake='bronze',
                            termo_assunto=termo_assunto.replace(' ', '_'),
                            data_extracao=data,
                            metrica='id_comentario',
                            nome_arquivo='id_comentario.pkl'
                        )
                ),
                extracao_dados=None,
                extracao_unica=(
                    InfraJson(
                        diretorio_datalake='bronze',
                        termo_assunto=termo_assunto.replace(' ', '_'),
                        data_extracao=data,
                        metrica='resposta_comentarios',
                        nome_arquivo='id_resposta_comentarios.json'
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

    extracao_api_video_trends = YoutubeBuscaTrendsOperator(
        task_id='id_extracao_api_video_trends',
        data_inicio=data_hora_busca,
        ordem_extracao=YoutubeTrendsYook(
            data_inicio=data_hora_busca
        ),
        extracao_dados=None,
        extracao_unica=InfraJson(
            diretorio_datalake='bronze',
            termo_assunto='top_brazil',
            data_extracao=data,
            metrica='top_brazil',
            nome_arquivo='req_top_brazil.json'
        )
    )

    # task_inicio >> extracao_api_youtube_historico_pesquisa >> task_fim


task_inicio >> tg1 >> tg2 >> tg3 >> tg4 >> extracao_api_video_trends >> task_fim
# tg1 >> tg2
# tg2 >> tg3
# tg3 >> tg4
# tg4 >> extracao_api_video_trends >> task_fim
