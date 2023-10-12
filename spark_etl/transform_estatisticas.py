import os
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f


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


def transform_youtube_video(spark: SparkSession,
                            param_datalake_load: str,
                            param_datalake_save: str,
                            assunto: str,
                            path_extracao: str,
                            path_save: str,
                            metrica: str,
                            load_arquivo: str,
                            save_arquivo,
                            ):
    caminho_base = '/home/rodrigo/projetos/dados_youtube/analise_dados_youtube/data/projeto_youtube'

    caminho_load = os.path.join(
        caminho_base,
        param_datalake_load,
        assunto,
        path_extracao,
        metrica,
        load_arquivo
    )
    print(caminho_load)
    df_video = spark.read.json(caminho_load)
    df_video = transform_estatisticas_videos(df_video)
    diretorio_save = os.path.join(
        caminho_base,
        param_datalake_save,
        assunto,
        path_extracao,
        metrica,
        save_arquivo
    )
    save_parquet(df_video, diretorio_save)


if __name__ == "__main__":
    # import argparse

    # parser = argparse.ArgumentParser(
    #     description="Spark youtube Transformation"
    # )
    # parser.add_argument("--assunto", required=True)
    # parser.add_argument("--path_extracao", required=True)
    # parser.add_argument("--metrica", required=True)
    # parser.add_argument("--load_arquivo", required=True)
    # parser.add_argument("--save_arquivo", required=True)

    # args = parser.parse_args()

    spark = SparkSession\
        .builder\
        .appName("twitter_transformation")\
        .getOrCreate()
    # transform_youtube_video(spark, args.assunto, args.path_extracao,
    #                         args.metrica, args.load_arquivo, args.save_arquivo)

    assunto = 'cities_skylines'
    path_extracao = 'extracao_data_2023_10_11'
    path_save = 'estatisticas'
    metrica = 'estatisticas'
    load_arquivo = 'req_video.json'
    save_arquivo = 'historico_video.parquet'
    param_datalake_load = 'bronze'
    param_datalake_save = 'prata'
    transform_youtube_video(
        spark=spark, assunto=assunto, path_extracao=path_extracao,
        path_save=path_save, metrica=metrica,
        load_arquivo=load_arquivo, save_arquivo=save_arquivo,
        param_datalake_load=param_datalake_load,
        param_datalake_save=param_datalake_save
    )
