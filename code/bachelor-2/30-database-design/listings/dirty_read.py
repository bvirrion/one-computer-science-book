"""dirty_read.py: two connections to one in-memory database in shared-cache mode;
the reader is allowed to read uncommitted changes."""
import sqlite3

URI = "file:shelf?mode=memory&cache=shared"
writer = sqlite3.connect(URI, uri=True, isolation_level=None)
reader = sqlite3.connect(URI, uri=True, isolation_level=None)
writer.execute("CREATE TABLE shelf (book_id INTEGER PRIMARY KEY, available INTEGER)")
writer.execute("INSERT INTO shelf VALUES (7, 3)")


def read(label):
    try:
        row = reader.execute("SELECT available FROM shelf WHERE book_id = 7").fetchone()
        n = row[0]
        print(f"{label}: the reader sees {n}")
    except sqlite3.OperationalError as e:
        print(f"{label}: the reader gets an error: {e}")


writer.execute("BEGIN")
writer.execute("UPDATE shelf SET available = 0 WHERE book_id = 7")
read("3 changed to 0, not committed")
reader.execute("PRAGMA read_uncommitted = 1")
read("the same, read_uncommitted on")
writer.execute("ROLLBACK")
read("writer rolled back")
