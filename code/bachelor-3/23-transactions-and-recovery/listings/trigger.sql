-- trigger.sql: the library's rule "at most five books out per member", enforced by
-- the database itself, whatever program inserts the loan.
-- load: town
CREATE TRIGGER five_books_out BEFORE INSERT ON loans
WHEN (SELECT count(*) FROM loans
      WHERE member_id = NEW.member_id AND return_date IS NULL) >= 5
BEGIN
  SELECT RAISE(ABORT, 'member already has five books out');
END;
SELECT count(*) AS out_now FROM loans WHERE member_id = 41 AND return_date IS NULL;
-- quiet
INSERT INTO loans (book_id, member_id, out_date, due_date)
  VALUES (1, 41, '2025-12-01', '2025-12-22');
INSERT INTO loans (book_id, member_id, out_date, due_date)
  VALUES (2, 41, '2025-12-01', '2025-12-22');
INSERT INTO loans (book_id, member_id, out_date, due_date)
  VALUES (3, 41, '2025-12-01', '2025-12-22');
INSERT INTO loans (book_id, member_id, out_date, due_date)
  VALUES (4, 41, '2025-12-01', '2025-12-22');
-- loud
SELECT count(*) AS out_now FROM loans WHERE member_id = 41 AND return_date IS NULL;
INSERT INTO loans (book_id, member_id, out_date, due_date)
  VALUES (5, 41, '2025-12-02', '2025-12-23');
INSERT INTO loans (book_id, member_id, out_date, due_date)
  VALUES (6, 41, '2025-12-02', '2025-12-23');
SELECT count(*) AS out_now FROM loans WHERE member_id = 41 AND return_date IS NULL;
