USE FILMES;
INSERT INTO `filmes`.`Canal` (`num_canal`, `nome`)
VALUES ('111', 'AXN'),
		('222', 'HBO'),
        ('333', 'CINEMAX'),
        ('444', 'TNT'),
        (555, 'NETFLIX'),
		(666, 'DISNEY+'),
		(777, 'CRUNCHYROLL');


INSERT INTO `filmes`.`Filme`
(`num_filme`, `nome`, `ano`, `duracao`)
VALUES
		('90001', 'Avatar', '2022', '162'),
		('90002', 'Titanic', '2022', '194'),
		('90003', 'Star Wars', '2022', NULL),
		('90004', 'Vingadores Ultimato', '2022', '180'),
		('90005', 'Lilo & Stich', '2025', '108'),
		(90006, 'Pantera Negra', 2018, 134),
		(90007, 'Matrix', 1999, 136),
		(90008, 'O Rei Leão', 1994, 88),
		(90009, 'Homem-Aranha: Sem Volta Para Casa', 2021, 148),
		(90010, 'Frozen', 2013, 102);


INSERT INTO `filmes`.`Exibicao` (`num_filme`, `num_canal`, `data_exibicao`, `hora_exibicao`) 
VALUES  ('90001', '222', '2025-06-27', '14:00:00'),
		('90003', '111', '2025-06-27', '19:45:00'),
        ('90002', '333', '2025-06-28', '09:30:00'),
        ('90002', '333', '2025-06-28', '20:30:00'),
        ('90005', '222', '2025-08-03', '16:20:00'),
        ('90005', '333', '2025-08-03', '16:20:00'),
        (90006, 444, '2025-07-10', '21:00:00'),
		(90006, 222, '2025-07-11', '15:00:00'),
		(90007, 333, '2025-07-15', '23:30:00'),
		(90008, 555, '2025-07-01', '10:00:00'),
		(90009, 222, '2025-07-20', '18:15:00'),
		(90009, 444, '2025-07-20', '22:00:00'),
		(90010, 666, '2025-07-25', '17:00:00'),
		(90010, 555, '2025-07-26', '11:00:00');
        
        
INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES
	(90001, 'Sam Worthington', TRUE),
	(90001, 'Zoe Saldana', TRUE),
	(90001, 'Sigourney Weaver', FALSE),

	(90002, 'Leonardo DiCaprio', TRUE),
	(90002, 'Kate Winslet', TRUE),
	(90002, 'Billy Zane', FALSE),

	(90003, 'Mark Hamill', TRUE),
	(90003, 'Carrie Fisher', TRUE),
	(90003, 'Harrison Ford', TRUE),

	(90004, 'Robert Downey Jr.', TRUE),
	(90004, 'Chris Evans', TRUE),
	(90004, 'Scarlett Johansson', FALSE),

	(90005, 'Daveigh Chase', TRUE),
	(90005, 'Tia Carrere', FALSE),
    
    (90006, 'Chadwick Boseman', TRUE),
	(90006, 'Lupita Nyong''o', FALSE),
	(90006, 'Michael B. Jordan', FALSE),

	(90007, 'Keanu Reeves', TRUE),
	(90007, 'Laurence Fishburne', FALSE),
	(90007, 'Carrie-Anne Moss', TRUE),

	(90008, 'Matthew Broderick', TRUE),
	(90008, 'James Earl Jones', FALSE),
	(90008, 'Jeremy Irons', FALSE),

	(90009, 'Tom Holland', TRUE),
	(90009, 'Zendaya', FALSE),
	(90009, 'Benedict Cumberbatch', FALSE),

	(90010, 'Idina Menzel', TRUE),
	(90010, 'Kristen Bell', TRUE),
	(90010, 'Josh Gad', FALSE);
