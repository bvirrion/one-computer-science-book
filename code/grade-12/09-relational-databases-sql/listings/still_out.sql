-- load: town
SELECT COUNT(*) FROM loans WHERE return_date IS NULL;
SELECT COUNT(*) FROM loans WHERE return_date = NULL;
SELECT COUNT(*) FROM loans WHERE return_date IS NOT NULL AND return_date > due_date;
SELECT MIN(out_date), MAX(out_date) FROM loans WHERE return_date IS NULL;
