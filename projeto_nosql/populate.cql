USE filmes_ks;

-- filme_por_ano
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2020, 90001, 'A Origem dos Sonhos', 120);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2021, 90002, 'Viagem no Tempo', 95);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2022, 90003, 'Guerra Intergaláctica', 130);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2020, 90004, 'Mistério no Deserto', 110);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2021, 90005, 'O Enigma Final', 105);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2023, 90006, 'Cidade dos Mortos', 102);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2022, 90007, 'Resgate Impossível', 115);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2023, 90008, 'Herança Perdida', 98);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2020, 90009, 'Planeta Azul', 90);
INSERT INTO filme_por_ano (ano, num_filme, nome, duracao) VALUES (2021, 90010, 'Crônicas do Submundo', 125);

-- exibicao_por_canal
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme) VALUES (1, '2024-07-01', '20:00:00', 90001, 'A Origem dos Sonhos');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (1, '2024-07-01', '22:00:00', 90002, 'Viagem no Tempo');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (2, '2024-07-02', '18:30:00', 90003, 'Guerra Intergaláctica');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (2, '2024-07-02', '21:00:00', 90004, 'Mistério no Deserto');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (3, '2024-07-03', '19:00:00', 90005, 'O Enigma Final');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (3, '2024-07-03', '21:30:00', 90006, 'Cidade dos Mortos');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (1, '2024-07-04', '20:15:00', 90007, 'Resgate Impossível');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (1, '2024-07-04', '22:30:00', 90008, 'Herança Perdida');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (2, '2024-07-05', '20:00:00', 90009, 'Planeta Azul');
INSERT INTO exibicao_por_canal (num_canal, data_exibicao, hora_exibicao, num_filme, nome_filme)  VALUES (2, '2024-07-05', '22:00:00', 90010, 'Crônicas do Submundo');

-- elenco_por_filme
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90001, 'João Silva', true);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90001, 'Maria Costa', false);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90002, 'Carlos Pereira', true);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90002, 'Ana Lima', false);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90003, 'Rafael Torres', true);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90003, 'Larissa Melo', true);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90004, 'Vinícius Rocha', false);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90004, 'Paula Souza', true);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90005, 'Marcos Dias', false);
INSERT INTO elenco_por_filme (num_filme, nome_ator, protagonista) VALUES (90005, 'Juliana Alves', true);

-- exibicao_por_filme
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90001, '2024-07-01', '20:00:00', 1);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90001, '2024-07-01', '22:00:00', 1);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90002, '2024-07-02', '18:30:00', 2);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90002, '2024-07-02', '21:00:00', 2);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90003, '2024-07-03', '19:00:00', 3);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90003, '2024-07-03', '21:30:00', 3);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90004, '2024-07-04', '20:15:00', 1);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90004, '2024-07-04', '22:30:00', 1);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90005, '2024-07-05', '20:00:00', 2);
INSERT INTO exibicao_por_filme (num_filme, data_exibicao, hora_exibicao, num_canal) VALUES (90005, '2024-07-05', '22:00:00', 2);

-- filmes_por_ator
INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('João Silva', 90001, 'A Origem dos Sonhos', true);

INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Maria Costa', 90001, 'A Origem dos Sonhos', false);

INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Carlos Pereira', 90002, 'Viagem no Tempo', true);

INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Ana Lima', 90002, 'Viagem no Tempo', false);

INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Rafael Torres', 90003, 'Guerra Intergaláctica', true);

INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Larissa Melo', 90003, 'Guerra Intergaláctica', true);
INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Vinícius Rocha', 90004, 'Mistério no Deserto', false);
INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Paula Souza', 90004, 'Mistério no Deserto', true);
INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Marcos Dias', 90005, 'O Enigma Final', false);
INSERT INTO filmes_por_ator (nome_ator, num_filme, nome_filme, protagonista) VALUES ('Juliana Alves', 90005, 'O Enigma Final', true);
