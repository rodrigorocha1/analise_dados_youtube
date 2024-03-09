
## Introdução
Este projeto tem como a proposta de elaborar uma arquitetura de extração da API do youtube até a elaboração do dashboard.


## Conceitos Rápidos

- DAG: É uma representação do fluxo de trabalho, sem ciclos
- Operators: São classes no Airflow que representam uma tarefa específica.
- Hooks: São usados para fazer iterações entre os sistemas, seja API, banco de dados



# Endpoints utilizados:

1. Pesquisar assunto do YouTube:
   - **URL:** `/youtube/v3/search`
   - **Descrição:** URL para obter os vídeos por assunto. Salva todo o histórico de busca, independente do idioma do canal.

2. Filtrar canais brasileiros:
   - **URL:** `/youtube/v3/channels`
   - **Descrição:** Após salvar os registros, esta URL é usada para consultar o idioma do canal e gerar uma lista de vídeos dos canais.

3. Obter dados dos vídeos:
   - **URL:** `/youtube/v3/videos`
   - **Descrição:** Após obter a lista de vídeos brasileiros, esta URL é usada para obter os dados completos. Os campos `viewCount`, `likeCount`, `favoriteCount`, `commentCount` serão usados, sempre gravando os dados históricos.

4. Extrair comentários:
   - **URL:** `/youtube/v3/commentThreads`
   - **Descrição:** Depois de extrair a lista de vídeos, esta URL é executada para extrair os comentários, gravando a requisição original em um datalakes.

5. Extrair respostas dos comentários:
   - **URL:** `/youtube/v3/comments`
   - **Descrição:** Depois de extrair os comentários, cada comentário tem um ID que mostra se possui respostas. Esta URL é usada para extrair as respostas dos comentários.

# Estrutura do datalake:
 A figura abaixo mostra a estrutura do datalake que foi construido.
 
![Exemplo de imagem](https://github.com/rodrigorocha1/analise_dados_youtube/blob/main/docs/datalake.drawio.png)

A Figura abaixo mostra o fluxo de dados até a geração do dashboard

![Exemplo de imagem](https://github.com/rodrigorocha1/analise_dados_youtube/blob/main/docs/diagrama_datalake.drawio.png)


A figura abaixo mostra o diagrama de classe da composição da dag. A lógica ficaria assim: para cada endpoints da api do youtube, iria herdar da classe base com seus requisitos específicos.

![](https://github.com/rodrigorocha1/analise_dados_youtube/blob/main/docs/diagrama%20de%20classe.png)

A figura abaixo mostra uma proposta de diagrama de atividade para a DAG
![](https://github.com/rodrigorocha1/analise_dados_youtube/blob/main/docs/diagrama_de_atividade_dag.drawio.png)


# Observações:
 Mesmo que o diagrama de atividade apresente, no final do processo, uma execução completa, uma proposta seria de implementar uma verificação de vídeos que contenham comentários antes de fazer todo o fluxo de comentários. 

