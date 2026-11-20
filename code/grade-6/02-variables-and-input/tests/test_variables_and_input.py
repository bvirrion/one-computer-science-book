"""The listings and exercise solutions of grade 6, chapter 2, print what the text says."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def run(folder, name, typed=""):
    r = subprocess.run(
        [sys.executable, name], cwd=HERE / folder, input=typed, capture_output=True, text=True
    )
    return r.returncode, r.stdout, r.stderr


def last(folder, name, typed=""):
    code, out, _ = run(folder, name, typed)
    assert code == 0
    return out.splitlines()[-1]


def typed(folder, name):
    return (HERE / folder / (name[:-3] + ".stdin")).read_text()


def test_variables_and_assignment():
    assert run("listings", "score.py")[1].splitlines() == ["0", "25", "Noor's score: 0"]
    assert last("listings", "update.py") == "30"
    assert last("listings", "swap.py") == "pear apple"
    assert last("listings", "trace_me.py") == "16 -8"


def test_types_and_glue():
    out = run("listings", "kinds.py")[1].split()
    assert out == ["<class", "'int'>", "<class", "'float'>", "<class", "'str'>", "<class", "'str'>"]
    assert run("listings", "glue.py")[1].splitlines() == ["7", "34", "icecream"]


def test_input_programs():
    assert last("listings", "greet.py", "Noor\n") == "Nice to meet you, Noor!"
    assert last("listings", "add_wrong.py", "12\n30\n").endswith("The sum is 1230")
    assert last("listings", "add_right.py", "12\n30\n").endswith("The sum is 42")
    assert last("listings", "rectangle.py", "7.5\n4\n") == "Perimeter: 23.0 metres"


def test_clock_and_back_undo_each_other():
    assert last("listings", "clock.py", "5000\n").endswith("1:23:20")
    assert last("listings", "clock.py", "50000\n").endswith("13:53:20")
    assert last("listings", "back.py", "13\n53\n20\n").endswith("Seconds: 50000")
    assert last("listings", "day.py") == "last second: 86399"
    seen = set()
    for total in range(86400):
        h, m, s = total // 3600, total % 3600 // 60, total % 60
        assert h < 24 and m < 60 and s < 60
        assert h * 3600 + m * 60 + s == total
        seen.add((h, m, s))
    assert len(seen) == 24 * 60 * 60 == 86400


def test_exercise_solutions():
    assert last("exercises", "three_a.py") == "7"
    assert last("exercises", "name_age.py", typed("exercises", "name_age.py")).endswith(
        "Sami will be 12 next year."
    )
    assert last("exercises", "minutes.py", "135\n").endswith("2 hours and 15 minutes")
    assert last("exercises", "notebooks.py", "6\n").endswith("Price: 15.0 euros")
    code, _, err = run("exercises", "half_bug.py", "2.5\n")
    assert code == 1 and "ValueError" in err
    assert last("exercises", "half.py", "2.5\n").endswith("1.25")
    assert run("exercises", "count_me.py")[1].splitlines() == ["1 2", "12"]
    assert last("exercises", "dhms.py", "1000000\n").endswith("11 days, 13 h, 46 min, 40 s")
    assert last("exercises", "swap_bad.py") == "8 8"
    assert "5" * 3 == "555" and isinstance(4.0, float) and not isinstance(4.0, int)
