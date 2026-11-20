-- load: schema.sql
INSERT INTO street VALUES (1, 'Bridge Road', 'B-100');
INSERT INTO member VALUES (1, 'Iris Hale', 1);
INSERT INTO book VALUES (1, 'The Silent Code', 'Fatou Dalewell', 2002);
INSERT INTO loan VALUES (1, 1, 1, '2025-03-02', NULL);
SELECT * FROM loan;
-- domain: a year no book has
INSERT INTO book VALUES (2, 'The Paper Forest', 'Zoe Stoneton', 3025);
-- relation: a second book with the key 1
INSERT INTO book VALUES (1, 'The Paper Forest', 'Zoe Stoneton', 1996);
-- reference: a loan to member 7, who does not exist
INSERT INTO loan VALUES (2, 1, 7, '2025-03-05', NULL);
-- the street of a member still in use
DELETE FROM street WHERE street_id = 1;
