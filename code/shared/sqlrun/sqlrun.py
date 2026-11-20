#!/usr/bin/env python3
"""The book's SQL runner: run the statements of a .sql file with Python's built-in sqlite3 (frozen).

    python sqlrun.py query.sql             a fresh database in memory
    python sqlrun.py query.sql town.db     an existing database file (created if missing)

Each statement is printed after "sql> " (its continuation lines after "...> "), then its answer:
a table of rows for a query, "OK" with the count of changed rows for a change, or "Error: ..."
(the script goes on, as an interactive session would). Two directives, alone on a line:

    -- load: schema.sql      run another file first, silently (relative to the .sql file)
    -- load: town            load the series' invented town (code/shared/town, every table)
    -- quiet / -- loud       stop / restart printing statements and answers

Columns are left-aligned, NULL prints as NULL, a real number as Python prints it.
"""
import os
import sqlite3
import sys


def split_statements(text):
    """Complete statements (sqlite3.complete_statement), with the directives as their own items."""
    out, buf = [], []
    for line in text.splitlines():
        s = line.strip()
        if not buf and s.startswith("--"):
            low = s[2:].strip()
            if low.startswith("load:") or low in ("quiet", "loud"):
                out.append(("directive", low))
            continue
        if not buf and not s:
            continue
        buf.append(line)
        joined = "\n".join(buf)
        if sqlite3.complete_statement(joined):
            out.append(("sql", joined.strip()))
            buf = []
    if buf and "\n".join(buf).strip():
        out.append(("sql", "\n".join(buf).strip()))
    return out


def table(cols, rows):
    def cell(v):
        return "NULL" if v is None else str(v)
    w = [len(c) for c in cols]
    for r in rows:
        for i, v in enumerate(r):
            w[i] = max(w[i], len(cell(v)))
    line = "+" + "+".join("-" * (x + 2) for x in w) + "+"
    out = [line, "| " + " | ".join(c.ljust(w[i]) for i, c in enumerate(cols)) + " |", line]
    for r in rows:
        out.append("| " + " | ".join(cell(v).ljust(w[i]) for i, v in enumerate(r)) + " |")
    out.append(line)
    out.append(f"({len(rows)} row{'' if len(rows) == 1 else 's'})")
    return "\n".join(out)


def load_town(conn):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "town"))
    import town
    town.to_sqlite(conn)


def run(conn, path, echo=True):
    base = os.path.dirname(os.path.abspath(path))
    with open(path, encoding="utf8") as f:
        items = split_statements(f.read())
    for kind, text in items:
        if kind == "directive":
            if text == "quiet":
                echo = False
            elif text == "loud":
                echo = True
            else:
                target = text.split(":", 1)[1].strip()
                if target == "town":
                    load_town(conn)
                else:
                    run(conn, os.path.join(base, target), echo=False)
            continue
        if echo:
            lines = text.splitlines()
            print("sql> " + lines[0])
            for ln in lines[1:]:
                print("...> " + ln)
        try:
            cur = conn.execute(text)
            if cur.description is not None:
                rows = cur.fetchall()
                if echo:
                    print(table([d[0] for d in cur.description], rows))
            else:
                conn.commit()
                if echo:
                    n = cur.rowcount
                    print("OK" if n < 0 else f"OK ({n} row{'' if n == 1 else 's'} changed)")
        except sqlite3.Error as e:
            if echo:
                print(f"Error: {e}")
        if echo:
            print()


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    conn = sqlite3.connect(argv[2] if len(argv) > 2 else ":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    run(conn, argv[1])
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
