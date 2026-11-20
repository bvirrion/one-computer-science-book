"""rollback.py: a late return is recorded in two tables, the loan and a new fine, as
one transaction; a failure in the middle undoes the first change too."""
import sqlite3

import town

conn = sqlite3.connect(":memory:", isolation_level=None)  # we BEGIN and COMMIT
conn.execute("PRAGMA foreign_keys = ON")
town.to_sqlite(conn)
conn.execute("CREATE TABLE fines (loan_id INTEGER PRIMARY KEY REFERENCES loans,"
             " amount INTEGER NOT NULL CHECK (amount > 0))")
loan, due = conn.execute("SELECT loan_id, due_date FROM loans WHERE return_date IS NULL"
                         " ORDER BY loan_id LIMIT 1").fetchone()


def record_return(day, amount):
    conn.execute("BEGIN")
    try:
        conn.execute("UPDATE loans SET return_date = ? WHERE loan_id = ?", (day, loan))
        conn.execute("INSERT INTO fines VALUES (?, ?)", (loan, amount))
        conn.execute("COMMIT")
        print(f"returned on {day}, fine {amount}: committed")
    except sqlite3.Error as e:
        conn.execute("ROLLBACK")
        print(f"returned on {day}, fine {amount}: {e}; rolled back")


def state():
    ret = conn.execute("SELECT return_date FROM loans WHERE loan_id = ?", (loan,))
    fines = conn.execute("SELECT count(*) FROM fines").fetchone()[0]
    print(f"   loan {loan} (due {due}): return_date {ret.fetchone()[0]}, fines {fines}")


state()
record_return("2026-02-03", 0)  # a fine of 0 breaks the CHECK, after the UPDATE
state()
record_return("2026-02-03", 2)
state()
