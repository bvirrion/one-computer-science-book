-- load: town
SELECT loans.loan_id, books.title, loans.out_date
FROM loans JOIN books ON loans.book_id = books.book_id
WHERE loans.loan_id <= 3;
SELECT l.out_date, b.title, p.first_name, p.last_name
FROM loans AS l
  JOIN books AS b ON l.book_id = b.book_id
  JOIN members AS m ON l.member_id = m.member_id
  JOIN people AS p ON m.person_id = p.person_id
WHERE l.return_date IS NULL AND l.out_date < '2025-04-01'
ORDER BY l.out_date;
