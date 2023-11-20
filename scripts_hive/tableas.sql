-------------------------------------------------------------------------

CREATE EXTERNAL TABLE TOTAL_VISUALIZACOES_POR_SEMANA(
	NM_CANAL string,
	ID_VIDEO string,
	TITULO_VIDEO string,
	TOTAL_CARACTERE_VIDEO INT,
	TAGS ARRAY<string>,
	DURACAO_VIDEO_MINUTOS FLOAT,
	TOTAL_TAGS INT,
	TOTAL_VISUALIZACOES INT,
	TOTAL_COMENTARIOS INT,
	TOTAL_LIKES INT,
	TOTAL_VISUALIZACOES_DIA INT, 
	TOTAL_COMENTARIOS_DIA INT,
	TOTAL_LIKES_DIA INT
) 
PARTITIONED BY(ASSUNTO STRING, data_extracao DATE, ID_CANAL STRING)
STORED AS PARQUET


LOAD DATA INPATH 'hdfs://localhost:9000/projeto/datalake_youtube/total_visualizacoes_semana.parquet' INTO TABLE TOTAL_VISUALIZACOES_POR_SEMANA;


SELECT * FROM TOTAL_VISUALIZACOES_POR_SEMANA;



---------------------------------



CREATE EXTERNAL TABLE IF NOT EXISTS TOTAL_VIDEO_PUBLICADO_SEMANA (
    SEMANA_TRADUZIDA STRING,
    NM_CANAL STRING,
    TOTAL_VIDEOS INT
)
PARTITIONED BY( DATA_PUBLICACAO DATE, ID_CANAL INT, ASSUNTO STRING,)
STORED AS PARQUET;

LOAD DATA INPATH 'hdfs://localhost:9000/projeto/datalake_youtube/video_publicado_semana.parquet' INTO TABLE TOTAL_VIDEO_PUBLICADO_SEMANA;


SELECT * 
FROM TOTAL_VIDEO_PUBLICADO_SEMANA
--------------------------------------------------------------------------------------




CREATE TABLE zipcodes(
	RecordNumber int,
	Country string,
	City string,
	Zipcode int)
	PARTITIONED BY(state string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';


LOAD DATA INPATH 'hdfs://localhost:9000/teste/zipcodes20.csv' INTO TABLE zipcodes;



CREATE TABLE zipcodes_multiple(
RecordNumber int,
Country string,
City string)
PARTITIONED BY(state string, zipcode string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';


LOAD DATA INPATH 'hdfs://localhost:9000/teste/zipcodes20.csv' INTO TABLE zipcodes_multiple;

SELECT * FROM zipcodes ;

select * from zipcodes_multiple;


---------------------------------------------------------------------------------------------


CREATE EXTERNAL TABLE resposta_comentarios_youtube(
  `id_resposta_comentarios` string, 
  `texto` varchar(700))
PARTITIONED BY ( 
  `assunto` string, 
  `id_canal` string, 
  `id_comentario` string)
STORED AS PARQUET;



LOAD DATA INPATH 'hdfs://localhost:9000/projeto/teste/resposta_comentarios/resposta_comentarios_assunto_cities_skylines.parquet' 
INTO TABLE resposta_comentarios_youtube;


SELECT COUNT(*)
FROM resposta_comentarios_youtube
where assunto  = 'assunto_cities_skylines';


---------------------------------------------------
CREATE EXTERNAL TABLE comentarios_youtube (
    ID_COMENTARIO STRING,
    TEXTO_COMENTARIO VARCHAR(700)
    
)
PARTITIONED BY(ASSUNTO STRING, ID_CANAL STRING, ID_VIDEO STRING)
STORED AS PARQUET;


MSCK REPAIR TABLE nome_da_tabela;


LOAD DATA INPATH 'hdfs://localhost:9000/projeto/teste/comentarios/comentarios_assunto_cities_skylines.parquet' INTO TABLE comentarios;


select * from comentarios;


DESCRIBE zipcodes;


DESCRIBE FORMATTED zipcodes;

SHOW PARTITIONS comentarios;


