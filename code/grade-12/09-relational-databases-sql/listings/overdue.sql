-- load: town
SELECT COUNT(*) FROM loans
WHERE out_date <= '2025-09-01' AND due_date < '2025-09-01'
  AND (return_date IS NULL OR return_date > '2025-09-01');
SELECT l.loan_id, b.title, l.due_date, l.return_date
FROM loans AS l JOIN books AS b ON l.book_id = b.book_id
WHERE l.out_date <= '2025-09-01' AND l.due_date < '2025-09-01'
  AND (l.return_date IS NULL OR l.return_date > '2025-09-01')
ORDER BY l.due_date;
SELECT DISTINCT p.first_name, p.last_name, s.name AS street
FROM loans AS l
  JOIN members AS m ON l.member_id = m.member_id
  JOIN people AS p ON m.person_id = p.person_id
  JOIN streets AS s ON p.street_id = s.street_id
WHERE l.out_date <= '2025-09-01' AND l.due_date < '2025-09-01'
  AND (l.return_date IS NULL OR l.return_date > '2025-09-01')
ORDER BY s.name, p.last_name;
SELECT SUM(julianday('2025-09-01') - julianday(due_date)) AS days_late,
       MAX(julianday('2025-09-01') - julianday(due_date)) AS longest
FROM loans
WHERE out_date <= '2025-09-01' AND due_date < '2025-09-01'
  AND (return_date IS NULL OR return_date > '2025-09-01');
