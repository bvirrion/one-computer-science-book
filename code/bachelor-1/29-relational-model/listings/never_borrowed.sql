-- load: town
-- Members who have never borrowed a book of poetry, three ways.
CREATE VIEW poetry_loans AS
  SELECT l.member_id FROM loans AS l JOIN books AS b ON b.book_id = l.book_id
  WHERE b.genre = 'poetry';
SELECT count(*) FROM (
  SELECT member_id FROM members EXCEPT SELECT member_id FROM poetry_loans);
SELECT count(*) FROM members AS m
WHERE NOT EXISTS (SELECT * FROM poetry_loans AS p WHERE p.member_id = m.member_id);
SELECT count(*) FROM members AS m
  LEFT JOIN poetry_loans AS p ON p.member_id = m.member_id
WHERE p.member_id IS NULL;
