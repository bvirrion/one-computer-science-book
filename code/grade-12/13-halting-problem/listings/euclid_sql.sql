-- Euclid's algorithm as a recursive query: each row is the next pair.
WITH RECURSIVE pairs(a, b) AS (
    SELECT 252, 198
    UNION ALL
    SELECT b, a % b FROM pairs WHERE b > 0
)
SELECT a, b FROM pairs;
