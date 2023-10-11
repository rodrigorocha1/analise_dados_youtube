# try:
#     import sys
#     import os
#     sys.path.insert(0, os.path.abspath(os.curdir))
# except ModuleNotFoundError:
#     pass
# from typing import Dict, List
# from datetime import datetime
# from hook.youtube_hook import YoutubeHook


# class UtilsHook(YoutubeHook):

#     def __init__(self, opcao: int, param_req: Dict, conn_id=None) -> None:
#         super().__init__(opcao, param_req, conn_id)

#     @classmethod
#     def extrair_dados_busca(cls, response_api: Dict, indice: int) -> List[Dict[str, str | int]]:
#         """Extrai os dados da busca de vídeos da API de busca (Search) do Youtube

#         Args:
#             response_api (Dict): Resultado da chamada da api
#             indice (int): indice loop

#         Returns:
#             List[Dict[str, str | int]]: uma lista de dicionários de id_video, canal, titulo_video, token_pg, while_i
#         """
#         lista_videos = []
#         for item in response_api['items']:
#             if cls.verificar_idioma_canal(item['snippet']['channelId']):
#                 try:
#                     dados_videos = {
#                         'id_video': item['id']['videoId'],
#                         'canal': item['snippet']['channelTitle'],
#                         'titulo_video': item['snippet']['title'],
#                         'token_pg': response_api['nextPageToken'],
#                         'while_i': indice
#                     }
#                     lista_videos.append(dados_videos)
#                 except:
#                     pass
#         return lista_videos

#     @staticmethod
#     def verificar_idioma_canal(query: str):
#         return query

#     @classmethod
#     def extrair_dados_video(cls, response_api: Dict) -> List[Dict[str, str | int]]:
#         """Método para extração dos dados do vídeo

#         Args:
#             response_api (Dict): _description_

#         Returns:
#             List[Dict[str, str | int]]: Lista de dicionários com os dados dos vídeos
#         """
#         lista_dados_video = []
#         for dados_video in response_api['items']:
#             dict_info_video = {
#                 'id_video': dados_video['id'],
#                 'titulo_video': dados_video['snippet']['title'],
#                 'id_canal': dados_video['snippet']['channelId'],
#                 'nome_canal': dados_video['snippet']['channelTitle'],
#                 'total_visualizacoes': int(dados_video['statistics']['viewCount']),
#                 'total_likes': int(dados_video['statistics']['likeCount']),
#                 'total_favoritos': int(dados_video['statistics']['favoriteCount']),
#                 'total_comentarios': int(dados_video['statistics']['commentCount']),
#                 'data_publicacao': dados_video['snippet']['publishedAt'],
#                 'duracao_video': (dados_video['contentDetails']['duration']),
#                 'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             }
#             try:
#                 tags = dados_video['snippet']['tags']
#             except KeyError:
#                 tags = None
#             dict_info_video['tags'] = tags
#             lista_dados_video.append(dict_info_video)
#         return lista_dados_video

#     @classmethod
#     def extrair_comentarios_superior(cls):
#         pass

#     @classmethod
#     def extrair_comentarios_inferios(cls):
#         pass
