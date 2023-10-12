import os
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f


def transform_resposta_comentarios(df_comentarios_json: DataFrame):
    df_comentarios_json.select(
        f.col('data_extracao').alias('DATA_EXTRACAO'),
        f.explode('items').alias('ITEMS')
    ) \
        .select(
            f.col('DATA_EXTRACAO'),
            f.col('ITEMS.id').alias('ID_RESPOSTA_COMENTARIOS'),
            f.col('ITEMS.snippet.channelId').alias('ID_CANAL'),
            f.col('ITEMS.snippet.textDisplay').alias('TEXTO'),
            f.col('ITEMS.snippet.likeCount').alias('TOTAL_LIKES'),
            f.col('ITEMS.snippet.publishedAt').alias('DATA_PUBLICACAO'),
            f.col('ITEMS.snippet.updatedAt').alias('DATA_ATUALIZACAO'),
    )
    return df_comentarios_json


def transform_comentarios(df_comentarios_json: DataFrame):
    df_comentarios_json.select(
        'data_extracao',
        f.explode('items').alias('ITEMS'),
    ) \
        .select(
        f.col('data_extracao').alias('DATA_EXTRACAO'),
        f.col('ITEMS.snippet.channelId').alias('ID_CANAL'),
        f.col('ITEMS.id').alias('ID_COMENTARIO'),
        f.col('ITEMS.snippet.videoId').alias('ID_VIDEO'),
        f.col('ITEMS.snippet.topLevelComment.snippet.textDisplay').alias(
            'TEXTO_COMENTARIO'),
        f.col('ITEMS.snippet.topLevelComment.snippet.likeCount').alias(
            'TOTAL_LIKES'),
        f.col('ITEMS.snippet.topLevelComment.snippet.publishedAt').alias(
            'DATA_PUBLICACAO'),
        f.col('ITEMS.snippet.topLevelComment.snippet.updatedAt').alias(
            'DATA_PUBLICACAO'),
        f.col('ITEMS.snippet.totalReplyCount').alias('TOTAL_RESPOSTAS')
    )
    return df_comentarios_json


def transform_estatisticas_videos(df_video_json: DataFrame):
    df_video_json.select(
        'data_extracao',
        f.col('items.id').alias('ID_VIDEO'),
        f.col('items.snippet.publishedAt').alias('DATA_PUBLICACAO'),
        f.col('items.snippet.channelId').alias('ID_CANAL'),
        f.col('items.snippet.channelTitle').alias('NM_CANAL'),
        f.col('items.snippet.categoryId').alias('ID_CATEGORIA'),
        f.col('items.snippet.title').alias('TITULO_VIDEO'),
        f.col('items.snippet.description').alias('DESCRICAO'),
        f.col('items.snippet.tags').alias('TAGS'),
        f.col('items.contentDetails.duration').alias('DURACAO_VIDEOS'),
        f.col('items.statistics.viewCount').alias('TOTAL_VISUALIZACOES'),
        f.col('items.statistics.likeCount').alias('TOTAL_LIKES'),
        f.col('items.statistics.favoriteCount').alias('TOTAL_FAVORITOS'),
        f.col('items.statistics.commentCount').alias('TOTAL_COMENTARIOS'),
    )
    return df_video_json


def save_parquet(df_json: DataFrame, diretorio_salvar: str):
    df_json.coalesce(1) \
        .write \
        .mode('overwrite')\
        .parquet(diretorio_salvar)


def transform_youtube(spark: SparkSession,
                      param_datalake_load: str,
                      path_extracao: str,
                      param_datalake_save: str,
                      assunto: str,
                      opcao: str,
                      ):
    caminho_base = '/home/rodrigo/projetos/dados_youtube/analise_dados_youtube/data/projeto_youtube'
    print(opcao)
    metrica = 'estatisticas'
    load_arquivo = 'req_video.json'
    save_arquivo = 'historico_video_tratada.parquet'
    caminho_load = os.path.join(
        caminho_base,
        param_datalake_load,
        assunto,
        path_extracao,
        metrica,
        load_arquivo
    )
    print(caminho_load)
    df_req = spark.read.json(caminho_load)
    df_req = transform_estatisticas_videos(df_req)
    diretorio_save = os.path.join(
        caminho_base,
        param_datalake_save,
        assunto,
        path_extracao,
        metrica,
        save_arquivo
    )
    save_parquet(df_req, diretorio_save)


if __name__ == "__main__":
    from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
    from airflow.models import DAG, TaskInstance
    import pendulum
    with DAG(
        dag_id='extracao_youtube',
        schedule_interval=None,
        catchup=False,
        start_date=pendulum.datetime(2023, 9, 8, tz='America/Sao_Paulo')
    ) as dag:
        transform_spark_submit = SparkSubmitOperator(
            task_id='teste_spark_cities_skylines',
            conn_id='id_spark',
            application='/home/rodrigo/projetos/dados_youtube/analise_dados_youtube/spark_etl/transform.py',
            name='transform_youtube',
            application_args=[
                    '--param_datalake_load', 'bronze',
                    '--path_extracao', 'extracao_data_2023_10_11',
                    '--param_datalake_save', 'prata',
                    '--assunto', 'cities_skylines',
                    '--opcao', 'um',
            ]
        )
        ti = TaskInstance(task=transform_spark_submit)
        transform_spark_submit.execute(ti.task_id)

#     import argparse

#     parser = argparse.ArgumentParser(
#         description="Spark youtube Transformation"
#     )
#     parser.add_argument("--assunto", required=True)
#     parser.add_argument("--path_extracao", required=True)
#     parser.add_argument("--param_datalake_load", required=True)
#     parser.add_argument("--param_datalake_save", required=True)
#     parser.add_argument("--opcao", required=True)

#     args = parser.parse_args()

#     spark = SparkSession\
#         .builder\
#         .appName("twitter_transformation")\
#         .getOrCreate()
#     transform_youtube(spark=spark, assunto=args.assunto, path_extracao=args.path_extracao,
#                       param_datalake_load=args.param_datalake_load,
#                       param_datalake_save=args.param_datalake_save, opcao=args.opcao)

# #     assunto = 'cities_skylines'
# #     path_extracao = 'extracao_data_2023_10_11'
# #     path_save = 'estatisticas'
# #     metrica = 'estatisticas'
# #     load_arquivo = 'req_video.json'
# #     save_arquivo = 'historico_video.parquet'
# #     param_datalake_load = 'bronze'
# #     param_datalake_save = 'prata'
#     transform_youtube(
#         opcao='1',
#         assunto='cities_skylines',
#         path_extracao='extracao_data_2023_10_11',
#         param_datalake_load='bronze',
#         param_datalake_save='prata',
#         spark=spark
#     )
