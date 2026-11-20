-- plans.sql: SQLite's plans for two reports on the town's library, before and after
-- an index and ANALYZE.
-- load: town
EXPLAIN QUERY PLAN
SELECT b.title, p.last_name, l.due_date
FROM loans l JOIN books b ON b.book_id = l.book_id
  JOIN members m ON m.member_id = l.member_id
  JOIN people p ON p.person_id = m.person_id
WHERE l.return_date IS NULL OR l.return_date > l.due_date;
EXPLAIN QUERY PLAN
SELECT p.last_name, count(*) AS loans
FROM people p JOIN members m ON m.person_id = p.person_id
  JOIN loans l ON l.member_id = m.member_id
GROUP BY p.person_id;
CREATE INDEX loans_member ON loans(member_id);
EXPLAIN QUERY PLAN
SELECT p.last_name, count(*) AS loans
FROM people p JOIN members m ON m.person_id = p.person_id
  JOIN loans l ON l.member_id = m.member_id
GROUP BY p.person_id;
ANALYZE;
SELECT tbl, idx, stat FROM sqlite_stat1 WHERE tbl IN ('loans', 'members', 'people');
EXPLAIN QUERY PLAN
SELECT p.last_name, count(*) AS loans
FROM people p JOIN members m ON m.person_id = p.person_id
  JOIN loans l ON l.member_id = m.member_id
GROUP BY p.person_id;
