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
    df_tratado = df_comentarios_json.select(
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
            'DATA_ATUALIZACAO'),
        f.col('ITEMS.snippet.totalReplyCount').alias('TOTAL_RESPOSTAS')
    )
    return df_tratado


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


def transform_youtube(
    param_datalake_load: str,
    path_extracao: str,
    param_datalake_save: str,
    assunto: str,
    opcao: str,
):

    spark = SparkSession.builder.appName('Exploracao').getOrCreate()
    caminho_base = '/home/rodrigo/projetos/analise_dados_youtube/data/analise_dados_youtube'
    print(opcao)
    if opcao == '1':
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
        if os.path.exists(caminho_load):

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

            spark.stop()
        else:
            spark.stop()
    elif opcao == '2':
        metrica = 'comentarios'
        load_arquivo = 'req_comentarios.json'
        save_arquivo = 'historico_comentario_tratada.parquet'
        caminho_load = os.path.join(
            caminho_base,
            param_datalake_load,
            assunto,
            path_extracao,
            metrica,
            load_arquivo
        )
        if os.path.exists(caminho_load):

            df_req = spark.read.json(caminho_load)
            df_req = transform_comentarios(df_req)
            print(df_req.show())
            diretorio_save = os.path.join(
                caminho_base,
                param_datalake_save,
                assunto,
                path_extracao,
                metrica,
                save_arquivo
            )
            save_parquet(df_req, diretorio_save)

            spark.stop()
        else:
            spark.stop()
    elif opcao == '3':
        metrica = 'resposta_comentarios'
        load_arquivo = 'resposta_comentarios.json'
        save_arquivo = 'historico_resposta_comentarios.parquet'
        caminho_load = os.path.join(
            caminho_base,
            param_datalake_load,
            assunto,
            path_extracao,
            metrica,
            load_arquivo
        )
        print(caminho_load)
        if os.path.exists(caminho_load):
            df_req = spark.read.json(caminho_load)
            df_req = transform_resposta_comentarios(df_req)

            diretorio_save = os.path.join(
                caminho_base,
                param_datalake_save,
                assunto,
                path_extracao,
                metrica,
                save_arquivo
            )
            save_parquet(df_req, diretorio_save)

            spark.stop()
        else:
            spark.stop()
    else:
        metrica = 'top_brazil'
        load_arquivo = 'req_top_brazil.json'
        save_arquivo = 'historico_top_brazil.parquet'

        caminho_load = os.path.join(
            caminho_base,
            param_datalake_load,
            metrica,
            path_extracao,
            metrica,
            load_arquivo
        )
        print(caminho_load)
        if os.path.exists(caminho_load):
            df_req = spark.read.json(caminho_load)
            df_req = transform_estatisticas_videos(df_req)
            diretorio_save = os.path.join(
                caminho_base,
                param_datalake_save,
                metrica,
                path_extracao,
                save_arquivo
            )

            save_parquet(df_req, diretorio_save)

            spark.stop()
        else:
            spark.stop()

if __name__ == '__main__':
    path_extracao='extracao_data_2023_10_14'
    transform_youtube(param_datalake_load='bronze',
                    path_extracao='extracao_data_2023_10_14',
                    param_datalake_save='prata', assunto='cities_skylines', opcao='2')
