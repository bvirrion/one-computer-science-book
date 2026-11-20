-- plan.sql: how SQLite answers one query on the town's loans, before and after an index.
-- load: town
SELECT count(*) AS loans FROM loans;
EXPLAIN QUERY PLAN SELECT out_date FROM loans WHERE member_id = 41;
CREATE INDEX loans_member ON loans(member_id);
EXPLAIN QUERY PLAN SELECT out_date FROM loans WHERE member_id = 41;
CREATE INDEX loans_member_out ON loans(member_id, out_date);
EXPLAIN QUERY PLAN SELECT out_date FROM loans WHERE member_id = 41;
EXPLAIN QUERY PLAN SELECT * FROM loans WHERE out_date > '2025-06-01';
