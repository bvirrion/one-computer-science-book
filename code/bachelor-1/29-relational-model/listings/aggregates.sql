-- load: town
SELECT genre, count(*) AS books, round(avg(pages)) AS pages
FROM books GROUP BY genre ORDER BY books DESC;
SELECT genre, count(*) AS books FROM books
WHERE pages > 200 GROUP BY genre HAVING count(*) >= 7;
