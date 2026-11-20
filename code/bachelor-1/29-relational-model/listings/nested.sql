-- load: town
SELECT title FROM books
WHERE book_id IN (SELECT book_id FROM loans WHERE return_date IS NULL)
  AND genre = 'science';
SELECT b.title, b.genre, b.pages FROM books AS b
WHERE b.pages > (SELECT 1.7 * avg(pages) FROM books AS c WHERE c.genre = b.genre);
SELECT count(*) FROM members AS m
WHERE EXISTS (SELECT * FROM loans AS l
              WHERE l.member_id = m.member_id AND l.return_date IS NULL);
