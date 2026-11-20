-- load: town
INSERT INTO books (book_id, title, author, year, genre, pages)
VALUES (81, 'The Tides of Brenmoor', 'Nils Mossham', 2025, 'history', 240);
UPDATE loans SET due_date = '2025-12-31' WHERE loan_id = 400;
SELECT loan_id, book_id, out_date, due_date FROM loans WHERE loan_id = 400;
UPDATE books SET pages = pages + 16 WHERE genre = 'poetry';
DELETE FROM members WHERE member_id = 8;
INSERT INTO loans VALUES (401, 99, 8, '2025-12-01', '2025-12-22', NULL);
DELETE FROM books WHERE book_id = 81;
SELECT COUNT(*) FROM books;
