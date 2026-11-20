-- load: town
SELECT COUNT(*), MIN(year), MAX(year), AVG(pages) FROM books;
SELECT COUNT(*), SUM(pages) FROM books WHERE genre = 'history';
SELECT COUNT(*), COUNT(return_date) FROM loans;
SELECT COUNT(DISTINCT member_id) FROM loans WHERE out_date >= '2025-11-01';
