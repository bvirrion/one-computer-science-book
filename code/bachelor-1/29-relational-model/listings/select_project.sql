-- load: town
SELECT title, year FROM books WHERE genre = 'poetry' AND year < 2000;
SELECT genre FROM books WHERE pages > 480;
SELECT DISTINCT genre FROM books WHERE pages > 480;
SELECT title, pages / 30 AS evenings FROM books WHERE author = 'Zoe Stoneton';
