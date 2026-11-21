"""The functions of grade 6/7, chapter 1 (grade 7), imported and called."""

import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(HERE / folder))
    try:
        with redirect_stdout(io.StringIO()):
            spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(HERE / folder))
    return module


def out(folder, name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=HERE / folder, capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr


def test_area_and_largest():
    area = load("listings", "area").area
    assert area(3, 4) == 12 and area(3.5, 4) == 14.0
    m = load("listings", "largest")
    for a in range(-3, 4):
        for b in range(-3, 4):
            assert m.largest2(a, b) == max(a, b)
            for c in range(-3, 4):
                assert m.largest3(a, b, c) == max(a, b, c)
    assert load("listings", "guarded").area(2, 5) == 10


def test_staged_errors():
    code, lines, err = out("listings", "print_not_return")
    assert code == 1 and lines == ["12"] and "NoneType" in err
    code, lines, err = out("listings", "local")
    assert code == 1 and lines == ["12"] and "NameError" in err


def test_receipt_and_examples():
    code, lines, _ = out("listings", "receipt")
    assert code == 0 and lines[-1].split() == ["TOTAL", "9.60"]
    m = load("listings", "receipt")
    assert abs(m.line_total(0.45, 6) - 2.70) < 1e-9
    code, lines, _ = out("listings", "check_examples")
    for line in lines:
        expected, got = line.removeprefix("expected ").split(", got ")
        assert expected == got


def test_barcode():
    m = load("listings", "barcode")
    assert m.weighted_sum(5901234123457) % 10 == 0
    assert m.check_digit(590123412345) == 7
    assert m.is_valid(5901234123457) and not m.is_valid(5901234123458)
    for first12 in [590123412345, 400638133393, 100000000000, 999999999999]:
        code = first12 * 10 + m.check_digit(first12)
        assert m.is_valid(code)
        assert sum(m.is_valid(first12 * 10 + d) for d in range(10)) == 1
    assert out("listings", "one_digit")[1] == ["117 caught out of 117"]
    lines = out("listings", "swaps")[1]
    assert lines[-1] == "80 caught out of 90"
    missed = [line.split()[1:] for line in lines[:-1]]
    assert len(missed) == 10 and all(abs(int(a) - int(b)) == 5 for a, b in missed)


def test_exercise_solutions():
    assert out("exercises", "two_calls")[1] == ["Hello!", "between", "Bye!"]
    assert out("exercises", "f_sum")[1] == ["12"]
    assert out("exercises", "print_and_return")[1] == ["doubling 5", "11"]
    assert out("exercises", "perimeter")[1] == ["14", "21.0"]
    assert out("exercises", "is_even")[1] == ["True False True"]
    assert out("exercises", "minutes_to_hours")[1] == ["1.5", "1.0"]
    lines = out("exercises", "loop_calls")[1]
    assert lines == [f"computing {i}" for i in range(1, 5)] + ["30"]
    assert out("exercises", "price")[1] == ["11 5", "12 9", "64 9", "65 6"]
    for line in out("exercises", "digit_sum")[1]:
        expected, got = line.removeprefix("expected ").split(", got ")
        assert expected == got
