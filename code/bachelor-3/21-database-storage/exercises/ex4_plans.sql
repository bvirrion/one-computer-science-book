-- ex4_plans.sql: predict each plan line before running it.
-- load: town
CREATE INDEX loans_member ON loans(member_id);
EXPLAIN QUERY PLAN SELECT count(*) FROM loans WHERE member_id = 41;
EXPLAIN QUERY PLAN SELECT member_id FROM loans WHERE member_id > 100;
EXPLAIN QUERY PLAN SELECT book_id FROM loans WHERE book_id = 59;
EXPLAIN QUERY PLAN SELECT * FROM loans WHERE loan_id = 7;
