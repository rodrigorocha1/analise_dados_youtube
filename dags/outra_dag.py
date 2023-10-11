from airflow.operators.empty import EmptyOperator
from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
import pendulum

dag = DAG(
    dag_id='task_dinamica',
    schedule_interval=None,
    catchup=False,
    start_date=pendulum.datetime(2023, 9, 8, tz='America/Sao_Paulo')
)

task_inicio = EmptyOperator(
    task_id='task_inicio'
)

lista = ['Cities_Skylines', 'Genshin_Impact',
         'Honkai_Star_Rail', 'Apache_Airflow']


with TaskGroup('task_youtube_api_historico_pesquisa', dag=dag) as tg1:
    lista_tasks = []
    for a in lista:
        t = EmptyOperator(
            task_id=f'task_{a}',
            dag=dag
        )
        lista_tasks.append(t)

with TaskGroup('tsk_extracao_api_youtube_dados_videos_estatistica', dag=dag) as tg2:
    lista_tasks = []
    for a in lista:
        t = EmptyOperator(
            task_id=f'task_{a}',
            dag=dag
        )
        lista_tasks.append(t)

with TaskGroup('tsk_extracao_youtube_dados_videos_comentarios', dag=dag) as tg3:
    lista_tasks = []
    for a in lista:
        t = EmptyOperator(
            task_id=f'task_{a}',
            dag=dag
        )
        lista_tasks.append(t)


with TaskGroup('tsk_extracao_youtube_dados_videos_respostas', dag=dag) as tg4:
    lista_tasks = []
    for a in lista:
        t = EmptyOperator(
            task_id=f'task_{a}',
            dag=dag
        )
        lista_tasks.append(t)

task_top_trend = EmptyOperator(
    task_id='task_top_trend'
)


task_fim = EmptyOperator(
    task_id='task_fim'
)

task_inicio >> tg1 >> tg2 >> tg3 >> tg4 >> task_top_trend >> task_fim
