"""Every operator of the algebra against SQLite on random tables; the three anti-joins
on random libraries; the schemas' constraints; the exercises."""

import contextlib
import io
import random
import sqlite3
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

import division as division_exo  # noqa: E402
import late_members  # noqa: E402
import sqlrun  # noqa: E402
import superkeys  # noqa: E402
from algebra import (Relation, difference, division, group, intersection,  # noqa: E402
                     natural_join, product, project, select, union)
from laws import check_laws  # noqa: E402

pairs = st.lists(st.tuples(st.integers(0, 3), st.integers(0, 3)), max_size=10)


def db(**tables):
    conn = sqlite3.connect(":memory:")
    for name, (cols, rows) in tables.items():
        conn.execute(f"CREATE TABLE {name} ({', '.join(cols)})")
        conn.executemany(f"INSERT INTO {name} VALUES ({', '.join('?' * len(cols))})", rows)
    return conn


def rows(conn, query):
    return {tuple(r) for r in conn.execute(query)}


@settings(max_examples=150, deadline=None)
@given(pairs, pairs, pairs, st.integers(0, 3))
def test_operators_against_sqlite(r_rows, r2_rows, s_rows, k):
    r, r2 = Relation("ab", r_rows), Relation("ab", r2_rows)
    s, t = Relation("bc", s_rows), Relation("cd", s_rows)
    conn = db(r=(("a", "b"), r_rows), r2=(("a", "b"), r2_rows),
              s=(("b", "c"), s_rows), t=(("c", "d"), s_rows))
    assert set(select(r, lambda d: d["a"] == k).rows) == rows(
        conn, f"SELECT DISTINCT a, b FROM r WHERE a = {k}")
    assert set(project(r, ("b",)).rows) == rows(conn, "SELECT DISTINCT b FROM r")
    assert set(union(r, r2).rows) == rows(conn, "SELECT a, b FROM r UNION SELECT a, b FROM r2")
    assert set(difference(r, r2).rows) == rows(conn, "SELECT a, b FROM r EXCEPT SELECT * FROM r2")
    assert set(intersection(r, r2).rows) == rows(conn, "SELECT * FROM r INTERSECT SELECT * FROM r2")
    assert set(product(r, t).rows) == rows(conn, "SELECT DISTINCT * FROM r, t")
    assert set(natural_join(r, s).rows) == rows(
        conn, "SELECT DISTINCT r.a, r.b, s.c FROM r JOIN s ON r.b = s.b")
    u = project(s, ("b",))
    assert set(division(r, u).rows) == rows(conn, (
        "SELECT DISTINCT a FROM r AS x WHERE NOT EXISTS (SELECT * FROM s AS y WHERE NOT "
        "EXISTS (SELECT * FROM r AS z WHERE z.a = x.a AND z.b = y.b))"))
    assert set(group(r, ("a",), "n", len, "b").rows) == rows(
        conn, "SELECT a, count(DISTINCT b) FROM r GROUP BY a")


def test_laws():
    assert check_laws(300, seed=1) == 300


QUERIES = (CH / "listings" / "never_borrowed.sql").read_text().split(";")[1:4]


def test_three_anti_joins_agree_on_random_libraries():
    rng = random.Random(29)
    for _ in range(200):
        conn = db(members=(("member_id",), [(m,) for m in range(rng.randrange(1, 8))]),
                  books=(("book_id", "genre"), [(b, rng.choice(["poetry", "x"]))
                                               for b in range(5)]),
                  loans=(("member_id", "book_id"), [(rng.randrange(8), rng.randrange(5))
                                                    for _ in range(rng.randrange(10))]))
        conn.execute("CREATE VIEW poetry_loans AS SELECT l.member_id FROM loans AS l "
                     "JOIN books AS b ON b.book_id = l.book_id WHERE b.genre = 'poetry'")
        answers = {conn.execute(q).fetchone()[0] for q in QUERIES}
        assert len(answers) == 1


def run_sql(path):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        sqlrun.run(conn, str(path))
    return out.getvalue()


def test_constraints_refuse_what_they_should():
    out = run_sql(CH / "listings" / "constraints.sql")
    assert out.count("Error:") == 6
    out = run_sql(CH / "listings" / "fk_off.sql")
    assert "Error" not in out and "| loan " in out  # accepted, then found by the check
    out = run_sql(CH / "exercises" / "er_schema.sql")
    assert out.count("Error:") == 5


def test_exercises():
    assert set(late_members.late_members().rows) == late_members.by_sql()
    assert len(late_members.late_members()) == 7
    _, readers = division_exo.every_book_of("Kofi Elmwick")
    assert set(readers.rows) == {(3,)}
    assert len(superkeys.superkeys(5, [0, 1])) == 8
