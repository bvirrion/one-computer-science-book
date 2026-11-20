import sqlite3
from pathlib import Path

import sqlrun

from schedules import CASES, POLICIES, Db

LISTINGS = Path(__file__).resolve().parent.parent / "listings"


def test_decomposition_round_trip_on_the_town():
    conn = sqlite3.connect(":memory:")
    sqlrun.run(conn, str(LISTINGS / "decomposed.sql"), echo=False)
    wide = set(conn.execute("SELECT * FROM wide").fetchall())
    joined = set(conn.execute("SELECT * FROM joined").fetchall())
    assert wide == joined and len(wide) == 400
    for table, key in [("d_loans", "loan_id"), ("d_books", "book_id"),
                       ("d_members", "member_id"), ("d_streets", "street")]:
        n, k = conn.execute(f"SELECT count(*), count(DISTINCT {key}) FROM {table}").fetchone()
        assert n == k  # the key really is a key in the data


def test_schedules_table():
    expected = {"dirty read": ["seen", "-", "-"],
                "non-repeatable read": ["seen", "seen", "-"],
                "phantom": ["seen", "seen", "-"],
                "lost update": ["seen", "seen", "refused"],
                "write skew": ["seen", "seen", "seen"]}
    for name, case, data in CASES:
        got = []
        for p in POLICIES:
            r = case(Db(data, p))
            got.append(r if isinstance(r, str) else "seen" if r else "-")
        assert got == expected[name]
