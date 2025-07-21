-- Keyspace
CREATE KEYSPACE IF NOT EXISTS filmes WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

USE filmes;

-- Tabela: filme_por_ano
CREATE TABLE filme_por_ano (
    ano INT,
    num_filme INT,
    nome TEXT,
    duracao INT,
    PRIMARY KEY (ano, num_filme)
);

-- Tabela: exibicao_por_canal
CREATE TABLE exibicao_por_canal (
    num_canal INT,
    data_exibicao DATE,
    hora_exibicao TIME,
    num_filme INT,
    nome_filme TEXT,
    PRIMARY KEY ((num_canal, data_exibicao), hora_exibicao)
) WITH CLUSTERING ORDER BY (hora_exibicao ASC);

-- Tabela: elenco_por_filme
CREATE TABLE elenco_por_filme (
    num_filme INT,
    nome_ator TEXT,
    protagonista BOOLEAN,
    PRIMARY KEY (num_filme, nome_ator)
);

-- Tabela: exibicao_por_filme
CREATE TABLE exibicao_por_filme (
    num_filme INT,
    data_exibicao DATE,
    hora_exibicao TIME,
    num_canal INT,
    PRIMARY KEY (num_filme, data_exibicao, hora_exibicao)
) WITH CLUSTERING ORDER BY (data_exibicao DESC, hora_exibicao DESC);

-- Tabela: filmes_por_ator
CREATE TABLE filmes_por_ator (
    nome_ator TEXT,
    num_filme INT,
    nome_filme TEXT,
    protagonista BOOLEAN,
    PRIMARY KEY (nome_ator, num_filme)
);
