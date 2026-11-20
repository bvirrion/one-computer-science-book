-- ex4_plan.sql: predict the plan before running it.
-- load: town
EXPLAIN QUERY PLAN
SELECT b.title, l.out_date
FROM books b JOIN loans l ON l.book_id = b.book_id
WHERE b.genre = 'mystery';
CREATE INDEX loans_book ON loans(book_id);
EXPLAIN QUERY PLAN
SELECT b.title, l.out_date
FROM books b JOIN loans l ON l.book_id = b.book_id
WHERE b.genre = 'mystery';
