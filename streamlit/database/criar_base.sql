DROP DATABASE IF EXISTS FILMES;
CREATE DATABASE FILMES;
USE FILMES;

CREATE TABLE Canal (
	num_canal INT PRIMARY KEY NOT NULL,
    nome VARCHAR(20) NOT NULL
);

CREATE TABLE Filme (
	num_filme INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    ano YEAR(4) NOT NULL,
    duracao INT
    
)AUTO_INCREMENT = 90001;

CREATE TABLE Exibicao (
	num_filme INT NOT NULL,
	num_canal INT NOT NULL,
    data_exibicao DATE NOT NULL,
    hora_exibicao TIME NOT NULL,
    CONSTRAINT fk_exibicao_filme FOREIGN KEY (num_filme) REFERENCES Filme(num_filme),
	CONSTRAINT fk_exibicao_canal FOREIGN KEY (num_canal) REFERENCES Canal(num_canal),
    PRIMARY KEY (num_filme, num_canal, data_exibicao, hora_exibicao)
);

CREATE TABLE Elenco (
	num_filme INT NOT NULL,
	nome_ator VARCHAR(100) NOT NULL,
	protagonista BOOLEAN NOT NULL,
	PRIMARY KEY (num_filme, nome_ator),
	FOREIGN KEY (num_filme) REFERENCES Filme(num_filme)
);

