-- load: town
-- The days on which books went out but none came back.
SELECT count(DISTINCT out_date) FROM loans
WHERE out_date NOT IN (SELECT return_date FROM loans);
SELECT count(DISTINCT out_date) FROM loans AS l
WHERE NOT EXISTS (SELECT * FROM loans AS r WHERE r.return_date = l.out_date);
