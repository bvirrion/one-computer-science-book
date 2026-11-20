-- load: town
CREATE VIEW late AS
  SELECT member_id, book_id, julianday(return_date) - julianday(due_date) AS days
  FROM loans WHERE return_date > due_date;
SELECT count(*), max(days), round(avg(days), 1) FROM late;
SELECT member_id, count(*) AS times FROM late
GROUP BY member_id ORDER BY times DESC, member_id LIMIT 3;
