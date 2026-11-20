"""The listings and exercise solutions of grade 6, chapter 1, print what the text says."""

import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def run(folder, name):
    r = subprocess.run([sys.executable, name], cwd=HERE / folder, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def lines(folder, name):
    code, out, _ = run(folder, name)
    assert code == 0
    return out.splitlines()


def test_arithmetic_listings():
    assert lines("listings", "prices.py") == ["21.75"]
    assert lines("listings", "operations.py") == ["12", "2", "35", "1.4", "5.0"]
    assert lines("listings", "share.py") == ["4", "3"]
    assert lines("listings", "order.py") == ["First line", "14", "20", "Last line"]
    assert 23 // 5 * 5 + 23 % 5 == 23


def test_comments_are_skipped():
    assert lines("listings", "comments.py") == ["School fair", "Saturday at 10", "Come and play!"]


def test_staged_errors(tmp_path):
    code, out, err = run("listings", "typo.py")
    assert code == 1 and out == "Hello\n" and "NameError" in err
    bad = tmp_path / "quote.py"
    bad.write_text((HERE / "listings" / "quote.txt").read_text())
    r = subprocess.run([sys.executable, str(bad)], capture_output=True, text=True)
    assert r.returncode == 1 and r.stdout == "" and "SyntaxError" in r.stderr


def test_trip_numbers():
    assert lines("listings", "trip.py") == ["pupils: 137", "buses: 3", "empty seats: 13", "museum groups: 12"]
    table = [tuple(map(int, line.split())) for line in lines("listings", "buses_table.py")]
    assert [n for n, b in table] == list(range(1, 201))
    changes = [n for (n, b), (_, before) in zip(table[1:], table) if b != before]
    assert changes == [51, 101, 151]
    assert lines("listings", "buses_check.py") == ["values that disagree: 0"]
    for n in range(1, 2001):
        assert (n + 49) // 50 == math.ceil(n / 50)


def test_exercise_solutions():
    assert len(lines("exercises", "poster.py")) == 3
    assert lines("exercises", "three_prints.py") == ["3", "2", "1", "Go!"]
    assert lines("exercises", "weeks.py") == ["14 weeks", "2 days"]
    assert lines("exercises", "tickets.py") == ["31.5"]
    assert lines("exercises", "cards_bug.py") == ["8", "42"]
    assert lines("exercises", "cards.py") == ["8", "2"]
    assert lines("exercises", "count_lines.py") == ["one", "three four", "", "five"]
    rows = [list(map(int, line.split())) for line in lines("exercises", "give_back.py")]
    assert len(rows) == 10 and all(r[0] == r[3] for r in rows)
    for n in range(0, 5000):
        assert (n // 5) * 5 + n % 5 == n
