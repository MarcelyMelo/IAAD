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
) AUTO_INCREMENT = 90001;

CREATE TABLE Exibicao (
	id_exibicao INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	num_filme INT NOT NULL,
	num_canal INT NOT NULL,
	data_exibicao DATE NOT NULL,
	hora_exibicao TIME NOT NULL,
	CONSTRAINT fk_exibicao_filme FOREIGN KEY (num_filme)
		REFERENCES Filme(num_filme)
		ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_exibicao_canal FOREIGN KEY (num_canal)
		REFERENCES Canal(num_canal)
		ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Elenco (
	id_elenco INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	num_filme INT NOT NULL,
	nome_ator VARCHAR(100) NOT NULL,
	protagonista BOOLEAN NOT NULL,
	FOREIGN KEY (num_filme)
		REFERENCES Filme(num_filme)
		ON DELETE CASCADE ON UPDATE CASCADE
);

DELIMITER $$

CREATE TRIGGER trg_valida_data_exibicao
BEFORE INSERT ON Exibicao
FOR EACH ROW
BEGIN
	DECLARE ano_lancamento_filme INT;
	SELECT ano INTO ano_lancamento_filme FROM Filme WHERE num_filme = NEW.num_filme;
	IF YEAR(NEW.data_exibicao) < ano_lancamento_filme THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Regra de negócio violada: Um filme não pode ser exibido antes de seu ano de lançamento.';
	END IF;
END$$
DELIMITER ;