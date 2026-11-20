-- load: town
SELECT title, author, year FROM books WHERE year < 1955;
SELECT title, pages FROM books WHERE genre = 'poetry' AND pages > 300;
SELECT first_name, last_name FROM people WHERE last_name LIKE 'Stonew%';
