"""lost_update.py: two desk programs lend copies of the same book at the same moment,
each with its own connection to the library's database file."""
import sqlite3
import tempfile
from pathlib import Path


def fresh(folder):
    path = Path(folder) / "library.db"
    path.unlink(missing_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE shelf (book_id INTEGER PRIMARY KEY,"
                     " available INTEGER)")
        conn.execute("INSERT INTO shelf VALUES (7, 3)")
    conn.close()
    a = sqlite3.connect(path, isolation_level=None, timeout=0)
    b = sqlite3.connect(path, isolation_level=None, timeout=0)
    return a, b


def available(conn):
    return conn.execute("SELECT available FROM shelf WHERE book_id = 7").fetchone()[0]


with tempfile.TemporaryDirectory() as folder:
    # 1. Read, then write what was read minus one: each statement on its own.
    a, b = fresh(folder)
    na, nb = available(a), available(b)  # both read 3
    a.execute("UPDATE shelf SET available = ? WHERE book_id = 7", (na - 1,))
    b.execute("UPDATE shelf SET available = ? WHERE book_id = 7", (nb - 1,))
    print("read, then write: two copies lent, available =", available(a))
    a.close()
    b.close()

    # 2. The same inside BEGIN IMMEDIATE: the second desk must wait for the first.
    a, b = fresh(folder)
    a.execute("BEGIN IMMEDIATE")
    na = available(a)
    try:
        b.execute("BEGIN IMMEDIATE")
    except sqlite3.OperationalError as e:
        print("BEGIN IMMEDIATE: the second desk is refused:", e)
    a.execute("UPDATE shelf SET available = ? WHERE book_id = 7", (na - 1,))
    a.execute("COMMIT")
    b.execute("BEGIN IMMEDIATE")  # the desk tries again
    nb = available(b)
    b.execute("UPDATE shelf SET available = ? WHERE book_id = 7", (nb - 1,))
    b.execute("COMMIT")
    print("BEGIN IMMEDIATE: two copies lent, available =", available(a))
    a.close()
    b.close()

    # 3. One statement that reads and writes: nothing to interleave.
    a, b = fresh(folder)
    for conn in (a, b):
        conn.execute("UPDATE shelf SET available = available - 1 WHERE book_id = 7")
    print("update expression: two copies lent, available =", available(a))
    a.close()
    b.close()
