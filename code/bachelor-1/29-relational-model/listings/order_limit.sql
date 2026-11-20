-- load: town
SELECT title, pages FROM books ORDER BY pages DESC, title LIMIT 3;
SELECT title, pages FROM books ORDER BY pages DESC, title LIMIT 3 OFFSET 3;
