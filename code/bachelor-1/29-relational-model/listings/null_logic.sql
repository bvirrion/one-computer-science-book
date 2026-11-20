SELECT NULL = NULL, NULL <> 1, NULL AND 0, NULL AND 1, NULL OR 1, NOT NULL;
-- load: town
SELECT count(*), count(return_date), count(DISTINCT member_id) FROM loans;
SELECT count(*) FROM loans WHERE return_date > due_date;
SELECT count(*) FROM loans WHERE NOT (return_date > due_date);
