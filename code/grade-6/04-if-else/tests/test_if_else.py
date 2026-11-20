"""The listings and exercise solutions of grade 6, chapter 4."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def run(folder, name, typed=""):
    r = subprocess.run(
        [sys.executable, name], cwd=HERE / folder, input=typed, capture_output=True, text=True
    )
    return r.returncode, r.stdout.splitlines(), r.stderr


def out(folder, name, typed=""):
    code, lines, _ = run(folder, name, typed)
    assert code == 0
    return lines


def price(age):
    return 5 if age < 12 else 9 if age < 65 else 6


def is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def test_comparisons_and_truth_table():
    assert out("listings", "compare.py") == ["True", "False", "True", "False", "False", "False"]
    rows = [line.split() for line in out("listings", "truth.py")]
    assert rows == [[str(a), str(b), str(a and b), str(a or b)] for a in (False, True) for b in (False, True)]


def test_branches():
    assert out("listings", "even_odd.py", "17\n")[-1] == "Thank you!"
    assert out("listings", "even_odd.py", "17\n")[-2].endswith("17 is odd")
    assert out("listings", "even_odd.py", "8\n")[-2].endswith("8 is even")
    for age in [0, 11, 12, 64, 65, 99]:
        assert out("listings", "ticket.py", f"{age}\n")[-1].endswith(f"Ticket: {price(age)} euros")
    assert out("listings", "wrong_order.py") == ["8 9", "30 9", "70 6"]
    assert out("listings", "all_prices.py") == [f"{a} {price(a)}" for a in range(0, 81, 5)]
    assert out("listings", "boundaries.py") == ["11 5", "12 9", "64 9", "65 6"]


def test_staged_syntax_error(tmp_path):
    bad = tmp_path / "assign_vs_equal.py"
    bad.write_text((HERE / "listings" / "assign_vs_equal.txt").read_text())
    r = subprocess.run([sys.executable, str(bad)], capture_output=True, text=True)
    assert r.returncode == 1 and "SyntaxError" in r.stderr and "==" in r.stderr


def test_leap_years():
    for y in [2024, 2100, 2000, 1900, 2023]:
        word = "is a leap year" if is_leap(y) else "is not a leap year"
        assert out("listings", "leap.py", f"{y}\n")[-1].endswith(f"{y} {word}")
    assert out("listings", "count_leap.py") == [
        "1901 to 2100: 49", "2001 to 2400: 97", "days in 400 years: 146097", "average year: 365.2425"
    ]
    assert sum(is_leap(y) for y in range(1601, 2001)) == 97
    assert out("exercises", "leap_bug.py", "1900\n")[-1].endswith("1900 is a leap year")


def test_exercise_solutions():
    assert out("exercises", "which.py") == ["medium"]
    assert out("exercises", "sign.py", "0\n")[-1].endswith("positive or zero")
    assert out("exercises", "sign.py", "-2\n")[-1].endswith("negative")
    assert out("exercises", "senior_bug.py") == ["adult"]
    assert out("exercises", "senior.py") == ["senior"]
    assert out("exercises", "largest.py", "4\n9\n2\n")[-1].endswith("The largest is 9.0")
    for typed in ["9\n4\n2\n", "2\n4\n9\n", "9\n9\n1\n"]:
        assert out("exercises", "largest.py", typed)[-1].endswith("The largest is 9.0")
    assert out("exercises", "grade.py", "13.5\n")[-1].endswith("Grade: B")
    for t, word in [(-5, "ice"), (0, "cool"), (19, "cool"), (20, "warm"), (30, "warm"), (31, "hot")]:
        assert out("exercises", "reach.py", f"{t}\n")[-1].endswith(word)
    assert out("exercises", "password.py", "abc\n")[-1].endswith("Too short: 9 more characters needed.")
    assert out("exercises", "password.py", "correcthorse\n")[-1].endswith("Long enough.")
    rows = [line.split() for line in out("exercises", "nested_vs_and.py")]
    assert len(rows) == 4 and all(r[2] == r[3] for r in rows)
    assert not (True and False) and (not (True and False)) is True
