
SELECT * FROM exibicao_por_canal 
WHERE num_canal = 1 AND data_exibicao = '2024-07-01';

SELECT * FROM exibicao_por_filme 
WHERE num_filme = 90001;


SELECT * FROM filme_por_ano 
WHERE ano = 2022;


SELECT * FROM elenco_por_filme 
WHERE num_filme = 90001;



UPDATE exibicao_por_canal
SET nome_filme = 'A Origem dos Sonhos (Versão Estendida)'
WHERE num_canal = 1 AND data_exibicao = '2024-07-01' AND hora_exibicao = '20:00:00';


UPDATE exibicao_por_canal
SET nome_filme = 'Filme Fantasma'
WHERE num_canal = 99 AND data_exibicao = '2099-01-01' AND hora_exibicao = '00:00:00';


DELETE FROM exibicao_por_canal
WHERE num_canal = 1 AND data_exibicao = '2024-07-01' AND hora_exibicao = '20:00:00';
