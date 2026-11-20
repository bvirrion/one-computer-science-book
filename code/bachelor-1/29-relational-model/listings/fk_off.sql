-- load: schema.sql
PRAGMA foreign_keys = OFF;
INSERT INTO loan VALUES (2, 999, 10, '2025-01-02', '2025-01-23', NULL);
PRAGMA foreign_key_check;
