"""A query built by pasting text, attacked; then the same query with a parameter."""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE notes (owner TEXT, note TEXT)")
conn.executemany("INSERT INTO notes VALUES (?, ?)",
                 [("bea", "renew The Paper Forest"), ("omar", "book the reading room"),
                  ("wen", "my locker code is 4417")])


def notes_unsafe(owner):
    query = f"SELECT note FROM notes WHERE owner = '{owner}'"   # pasted text
    print("  query sent:", query)
    return conn.execute(query).fetchall()


def notes_safe(owner):
    return conn.execute("SELECT note FROM notes WHERE owner = ?", (owner,)).fetchall()


print("unsafe, an honest name:", notes_unsafe("bea"))
attack = "bea' OR '1' = '1"
print("unsafe, the attack:", notes_unsafe(attack))
print("safe, an honest name:", notes_safe("bea"))
print("safe, the attack:", notes_safe(attack))
