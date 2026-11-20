"""sqlite_isolation.py -- two connections to one SQLite file, A and B, driven step
by step from one script, with no waiting (timeout 0): first in the default rollback-
journal mode, then in WAL mode."""

import sqlite3
import tempfile
from pathlib import Path


def run(conn, name, sql):
    try:
        rows = conn.execute(sql).fetchall()
        shown = f" -> {rows[0][0]}" if rows else ""
        print(f"{name}: {sql}{shown}")
        return True
    except sqlite3.OperationalError as e:
        print(f"{name}: {sql} -> error: {e}")
        return False


with tempfile.TemporaryDirectory() as d:
    for mode in ("delete", "wal"):
        path = Path(d) / f"{mode}.db"
        setup = sqlite3.connect(path)
        setup.execute(f"PRAGMA journal_mode={mode}")
        setup.execute("CREATE TABLE stock (book TEXT PRIMARY KEY, copies INTEGER)")
        setup.execute("INSERT INTO stock VALUES ('atlas', 3)")
        setup.commit()
        setup.close()
        a = sqlite3.connect(path, timeout=0, isolation_level=None)
        b = sqlite3.connect(path, timeout=0, isolation_level=None)
        print(f"-- journal mode {mode}")
        q = "SELECT copies FROM stock WHERE book = 'atlas'"
        run(a, "A", "BEGIN IMMEDIATE")
        run(a, "A", "UPDATE stock SET copies = 2 WHERE book = 'atlas'")
        run(b, "B", "BEGIN IMMEDIATE")
        run(b, "B", "BEGIN")
        run(b, "B", q)
        committed = run(a, "A", "COMMIT")
        run(b, "B", q)
        run(b, "B", "COMMIT")
        if not committed:
            run(a, "A", "COMMIT")
        run(b, "B", q)
        a.close()
        b.close()
