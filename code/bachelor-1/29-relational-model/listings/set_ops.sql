-- load: town
SELECT count(*) FROM (
  SELECT author FROM books WHERE genre = 'poetry'
  UNION SELECT author FROM books WHERE genre = 'science');
SELECT author FROM books WHERE genre = 'poetry'
INTERSECT SELECT author FROM books WHERE genre = 'science';
SELECT author FROM books WHERE genre = 'poetry'
EXCEPT SELECT author FROM books WHERE genre = 'science';
