-- load: town
SELECT DISTINCT genre FROM books ORDER BY genre;
SELECT title, year FROM books WHERE author = 'Zoe Stoneton' ORDER BY year DESC;
SELECT title, pages FROM books ORDER BY pages DESC, title LIMIT 3;
