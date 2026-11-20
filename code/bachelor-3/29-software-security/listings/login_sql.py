"""login_sql.py -- the toy app's login against an sqlite3 table. The unsafe query
pastes the typed name into the SQL text; the safe one passes it as a parameter.
(A fast hash keeps the demo short; the previous chapter says how to store passwords.)"""

import hashlib
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT, pw_hash TEXT, role TEXT)")
for name, pw, role in [("ada", "correct horse", "reader"), ("admin", "x7!Kq", "admin")]:
    db.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        (name, hashlib.sha256(pw.encode()).hexdigest(), role),
    )


def login_unsafe(name, password):
    h = hashlib.sha256(password.encode()).hexdigest()
    sql = f"SELECT name, role FROM users WHERE name = '{name}' AND pw_hash = '{h}'"
    print("   SQL:", sql[:72] + ("..." if len(sql) > 72 else ""))
    return db.execute(sql).fetchone()


def login_safe(name, password):
    h = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT name, role FROM users WHERE name = ? AND pw_hash = ?"
    return db.execute(sql, (name, h)).fetchone()  # the values never become SQL text


for name, pw in [("ada", "correct horse"), ("ada", "wrong"), ("admin' --", "anything")]:
    print(f"name {name!r}, password {pw!r}:")
    print("   unsafe ->", login_unsafe(name, pw))
    print("   safe   ->", login_safe(name, pw))
