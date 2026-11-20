"""Grade 7, chapter 5: the staged bugs fail as printed, and the fixes work."""

import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))  # check_grader imports grader_v2 to v4


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def run(folder, name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=HERE / folder, capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr


def test_staged_errors(tmp_path):
    bad = tmp_path / "missing_colon.py"
    bad.write_text((HERE / "listings" / "missing_colon.txt").read_text())
    r = subprocess.run([sys.executable, str(bad)], capture_output=True, text=True)
    assert r.returncode == 1 and "SyntaxError: expected ':'" in r.stderr
    code, _, err = run("listings", "zero_division")
    assert code == 1 and err.strip().endswith("ZeroDivisionError: division by zero")
    code, out, err = run("listings", "two_calls")
    assert code == 1 and out == ["Leo average: 10.6"] and "in report" in err and "in average" in err
    code, _, err = run("listings", "last_item")
    assert code == 1 and "IndexError" in err


def test_average():
    assert run("listings", "average_bug")[1] == ["13.25"]
    assert run("listings", "average_fixed")[1] == ["10.6"]
    out = run("listings", "average_trace")[1]
    assert out[-1] == "13.25" and sum(line.startswith("  trace:") for line in out) == 6


def test_first_word():
    assert run("listings", "first_word_bug")[1] == ["[The]", "[Hello]", "[Sto]", "[]"]
    assert run("listings", "first_word_fixed")[1] == ["[The]", "[Hello]", "[Stop]", "[a]"]


def test_grader():
    bad = (HERE / "listings" / "grader.txt").read_text()
    with_colon = bad.replace("def comment(score)\n", "def comment(score):\n")
    v1 = (HERE / "listings" / "grader_v1.py").read_text()
    assert with_colon.replace("# grader.py", "# grader_v1.py") == v1
    assert len(bad.splitlines()) <= 28
    code, out, err = run("listings", "grader_v1")
    assert code == 1 and len(out) == 4 and "IndexError" in err
    expected = load("listings", "check_grader").expected
    counts = []
    for v in ["grader_v2", "grader_v3", "grader_v4"]:
        m = load("listings", v)
        counts.append(sum(m.grade(s) != expected(s) for s in range(100)))
    assert counts == [66, 1, 0]
    v2, v4 = load("listings", "grader_v2"), load("listings", "grader_v4")
    wrong = [s for s in range(100) if v2.comment(s) != v4.comment(s)]
    assert wrong[0] == 5
    # fixing the letter first leaves the count at 66: input 90 is also wrong in its comment
    assert v2.comment(90) != v4.comment(90)


def test_exercises():
    assert run("exercises", "first_five")[1] == ["total of the first five marks: 67"]
    assert run("listings", "count_above_trace")[1] == ["  trace: value 3 count 0", "0"]
    assert run("exercises", "count_above_fixed")[1] == ["2"]
    assert run("exercises", "is_sorted_bug")[1] == ["True False False"]
    assert run("exercises", "is_sorted_fixed")[1] == ["True False", "True True"]
    assert load("exercises", "is_sorted_bug").is_sorted([1, 1]) is False
    assert run("exercises", "average_guard")[1] == ["10.6 0"]
    assert run("exercises", "evens_bug")[1][0].endswith(": 25")
    assert run("exercises", "evens_fixed")[1][0].endswith(": 30")
    assert run("exercises", "largest_bug")[1] == ["9 4 0"]
    assert run("exercises", "largest_fixed")[1] == ["9 9 5"]
