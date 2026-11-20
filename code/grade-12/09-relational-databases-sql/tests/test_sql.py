import importlib.util
import io
import sqlite3
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(ROOT / "code" / "shared" / "town"))
sys.path.insert(0, str(ROOT / "code" / "shared" / "sqlrun"))
import sqlrun  # noqa: E402


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_exercise_numbers():
    ex = load("exercises", "sql_ex")
    conn = ex.town_db()
    assert ex.count_authors(conn) == 23
    assert ex.by_author(conn, "Caio Lakeby") == [
        ("A Year by the Lighthouse", 1955), ("The Hidden Harbour", 1959),
        ("The Hidden Machine", 1961), ("The Last Forest", 1995)]
    assert ex.cross_size(conn) == 400 * 80
    assert len(ex.members_still_out(conn)) == 17
    assert ex.join_rows(conn) == 400
    n = conn.execute("SELECT COUNT(*) FROM loans WHERE return_date = NULL").fetchone()[0]
    assert n == 0
    assert ex.extend_still_out(conn, 14) == 22
    for table, key, refused in [("streets", "street_id", True), ("loans", "loan_id", False),
                                ("people", "person_id", True), ("members", "member_id", True)]:
        result = ex.try_delete(conn, f"DELETE FROM {table} WHERE {key} = 1")
        assert (result == "FOREIGN KEY constraint failed") == refused
    assert ex.books_between(conn, 1950, 1951) == ["The Silent Kingdom", "Beyond the Code",
                                                  "The Paper Comet"]


def test_timetable_constraints():
    ex = load("exercises", "sql_ex")
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(ex.TIMETABLE)
    conn.execute("INSERT INTO teacher VALUES (1, 'Ines')")
    conn.execute("INSERT INTO room VALUES ('B12', 30)")
    conn.execute("INSERT INTO lesson VALUES ('Mon', 9, 'B12', 1, 'physics')")
    for bad in ["INSERT INTO lesson VALUES ('Mon', 9, 'B12', 1, 'maths')",
                "INSERT INTO lesson VALUES ('Sun', 9, 'B12', 1, 'maths')",
                "INSERT INTO lesson VALUES ('Tue', 9, 'C1', 1, 'maths')"]:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(bad)


def test_injection_and_python(monkeypatch):
    inj = load("listings", "injection")
    assert len(inj.notes_unsafe("bea' OR '1' = '1")) == 3
    assert inj.notes_safe("bea' OR '1' = '1") == []
    fp = load("listings", "from_python")
    assert fp.loans_of is not None


def test_problem_numbers():
    conn = sqlite3.connect(":memory:")
    sqlrun.load_town(conn)
    d = "'2025-09-01'"
    where = (f"out_date <= {d} AND due_date < {d} AND "
             f"(return_date IS NULL OR return_date > {d})")
    rows = conn.execute(f"SELECT due_date, return_date FROM loans WHERE {where}").fetchall()
    assert len(rows) == 18 and sum(r[1] is not None for r in rows) == 4
    late = conn.execute(f"SELECT SUM(julianday({d}) - julianday(due_date)) FROM loans "
                        f"WHERE {where}").fetchone()[0]
    assert late == 1696
