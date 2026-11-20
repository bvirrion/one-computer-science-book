-- load: wide_build.sql
SELECT count(*) AS lines, count(DISTINCT member_id) AS members,
       count(DISTINCT book_id) AS books FROM wide;
SELECT street, postcode, count(*) AS lines FROM wide
WHERE member_id = 55 GROUP BY street, postcode;
UPDATE wide SET street = 'Garden Lane', postcode = 'B-110'
WHERE member_id = 55
  AND loan_id < (SELECT max(loan_id) FROM wide WHERE member_id = 55);
SELECT street, postcode, count(*) AS lines FROM wide
WHERE member_id = 55 GROUP BY street, postcode;
