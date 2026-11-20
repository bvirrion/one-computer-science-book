-- wide_build.sql: the library's spreadsheet, one line per loan with everything on it.
-- load: town
CREATE TABLE wide AS
SELECT l.loan_id, l.out_date, l.due_date, l.return_date,
       b.book_id, b.title, b.author, b.genre, b.pages,
       m.member_id, p.first_name, p.last_name, s.name AS street, s.postcode
FROM loans AS l
JOIN books AS b ON b.book_id = l.book_id
JOIN members AS m ON m.member_id = l.member_id
JOIN people AS p ON p.person_id = m.person_id
JOIN streets AS s ON s.street_id = p.street_id;
