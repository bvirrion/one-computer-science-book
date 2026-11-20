-- load: town
EXPLAIN QUERY PLAN
SELECT loan_id, out_date FROM loans WHERE member_id = 55;
CREATE INDEX loans_member ON loans (member_id);
EXPLAIN QUERY PLAN
SELECT loan_id, out_date FROM loans WHERE member_id = 55;
EXPLAIN QUERY PLAN
SELECT loan_id, out_date FROM loans WHERE member_id + 0 = 55;
