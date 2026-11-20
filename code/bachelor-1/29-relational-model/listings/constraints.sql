-- load: schema.sql
INSERT INTO person VALUES (1, 'Iris', 'Brook'), (2, 'Ben', 'Holt');
INSERT INTO member VALUES (10, 1, '2024-05-01');
INSERT INTO book VALUES (100, 'The Silent Code', 'Fatou Dalewell', 65);
INSERT INTO loan VALUES (1, 100, 10, '2025-01-01', '2025-01-22', NULL);
INSERT INTO book VALUES (100, 'Another Book', 'Somebody', 90);
INSERT INTO member VALUES (11, 1, '2025-02-01');
INSERT INTO loan VALUES (2, 999, 10, '2025-01-02', '2025-01-23', NULL);
INSERT INTO book VALUES (101, NULL, 'Nobody', 40);
INSERT INTO loan VALUES (3, 100, 10, '2025-01-05', '2025-01-01', NULL);
DELETE FROM book WHERE book_id = 100;
