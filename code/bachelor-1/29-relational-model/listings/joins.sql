-- load: town
SELECT b.title, l.out_date, l.return_date
FROM books AS b JOIN loans AS l ON l.book_id = b.book_id
WHERE b.author = 'Vera Ashley' AND l.out_date >= '2025-11-01';
SELECT b.title, l.out_date, l.return_date
FROM books AS b LEFT JOIN loans AS l
  ON l.book_id = b.book_id AND l.out_date >= '2025-11-01'
WHERE b.author = 'Vera Ashley';
