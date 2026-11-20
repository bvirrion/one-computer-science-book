-- load: town
SELECT genre, count(*) FROM books WHERE count(*) >= 10 GROUP BY genre;
