"""SQL from Python: the town's tables in sqlite3, and a query with parameters."""
import sqlite3

import town

conn = sqlite3.connect(":memory:")              # a database in memory
conn.execute("PRAGMA foreign_keys = ON")
town.to_sqlite(conn)                            # create and fill the tables


def loans_of(conn, last_name, since):
    """Titles borrowed by members with this last name, from a date on."""
    rows = conn.execute(
        """SELECT p.first_name, b.title, l.out_date
           FROM loans AS l
             JOIN books AS b ON l.book_id = b.book_id
             JOIN members AS m ON l.member_id = m.member_id
             JOIN people AS p ON m.person_id = p.person_id
           WHERE p.last_name = ? AND l.out_date >= ?
           ORDER BY l.out_date""",
        (last_name, since))                     # the values travel apart
    return rows.fetchall()


for first, title, day in loans_of(conn, "Stoneford", "2025-09-01"):
    print(day, first, "borrowed", title)
total = conn.execute("SELECT COUNT(*) FROM loans WHERE return_date IS NULL")
print("still out:", total.fetchone()[0])
conn.close()
