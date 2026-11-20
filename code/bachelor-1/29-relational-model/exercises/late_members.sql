-- load: town
-- Exercise: the members with more than three late returns.
SELECT member_id, count(*) AS late FROM loans
WHERE return_date > due_date
GROUP BY member_id HAVING count(*) > 3
ORDER BY member_id;
