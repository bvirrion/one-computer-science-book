-- load: wide_build.sql
CREATE TABLE d_loans AS
  SELECT DISTINCT loan_id, out_date, due_date, return_date, book_id, member_id FROM wide;
CREATE TABLE d_books AS SELECT DISTINCT book_id, title, author, genre, pages FROM wide;
CREATE TABLE d_members AS
  SELECT DISTINCT member_id, first_name, last_name, street FROM wide;
CREATE TABLE d_streets AS SELECT DISTINCT street, postcode FROM wide;
SELECT (SELECT count(*) FROM d_loans) AS loans,
       (SELECT count(*) FROM d_books) AS books,
       (SELECT count(*) FROM d_members) AS members,
       (SELECT count(*) FROM d_streets) AS streets,
       (SELECT count(DISTINCT member_id) FROM d_members) AS member_ids,
       (SELECT count(DISTINCT street) FROM d_streets) AS street_names;
CREATE VIEW joined AS
  SELECT l.loan_id, l.out_date, l.due_date, l.return_date,
         b.book_id, b.title, b.author, b.genre, b.pages,
         m.member_id, m.first_name, m.last_name, s.street, s.postcode
  FROM d_loans AS l NATURAL JOIN d_books AS b
  NATURAL JOIN d_members AS m NATURAL JOIN d_streets AS s;
SELECT (SELECT count(*) FROM (SELECT * FROM wide EXCEPT SELECT * FROM joined))
         AS lost,
       (SELECT count(*) FROM (SELECT * FROM joined EXCEPT SELECT * FROM wide))
         AS invented;
