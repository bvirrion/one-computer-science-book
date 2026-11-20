import calendar
import doctest
import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        try:
            spec.loader.exec_module(module)
        except (IndexError, AssertionError):
            pass  # staged errors at the end of a listing
    return module


def test_faulty_leap_year_is_wrong_only_on_centuries():
    faulty = load("listings", "leap").leap_year
    wrong = [y for y in range(1583, 2401) if faulty(y) != calendar.isleap(y)]
    assert wrong == [y for y in range(1583, 2401) if y % 100 == 0 and y % 400]


def test_fixed_leap_year_matches_calendar():
    fixed = load("listings", "leap_fixed").leap_year
    assert all(fixed(y) == calendar.isleap(y) for y in range(1583, 3001))


def test_guard_and_average():
    guard = load("listings", "guard")
    assert guard.starts_with([3, 1], 3) and not guard.starts_with([], 3)
    with pytest.raises(IndexError):
        guard.starts_with_unguarded([], 3)
    average = load("listings", "average").average
    assert average([12, 15, 9]) == 12
    with pytest.raises(AssertionError):
        average([])


def test_mean_doctests_pass():
    mean = load("listings", "mean")
    assert doctest.testmod(mean).failed == 0


def test_staged_bugs_show_their_symptom():
    side = load("listings", "side_effect")
    t = [1, 5, 3, 4]
    assert side.largest_three(t) == [5, 4, 3] and t == [5, 4, 3, 1]
    grade = load("listings", "missing_branch").grade
    assert grade(15) is None and grade(16) == "merit"


def test_days_in_month():
    days = load("exercises", "days_in_month").days_in_month
    rng = random.Random(1)
    for year in [1900, 2000, 2023, 2024] + [rng.randint(1583, 2400) for _ in range(50)]:
        for month in range(1, 13):
            assert days(month, year) == calendar.monthrange(year, month)[1]


def test_percent_and_sign():
    percent = load("exercises", "percent").percent
    assert percent(1, 4) == 25
    for bad in [(1, 0), (-1, 4), (5, 4)]:
        with pytest.raises(AssertionError):
            percent(*bad)
    sign = load("exercises", "sign").sign
    assert [sign(x) for x in (-3, 0, 2.5)] == [-1, 0, 1]


def test_roman():
    roman = load("exercises", "roman").roman
    assert roman(1994) == "MCMXCIV" and roman(3999) == "MMMCMXCIX"
    seen = {roman(n) for n in range(1, 4000)}
    assert len(seen) == 3999


def test_remove_negatives_and_tenths():
    rn = load("exercises", "remove_negatives")
    assert rn.remove_negatives_buggy([-1, -2, 3]) == [-2, 3]
    t = [-1, -2, 3]
    assert rn.remove_negatives(t) == [3] and t == [-1, -2, 3]
    assert load("exercises", "count_up").count_tenths() == 10


def test_mutant_counts():
    m = load("exercises", "mutants")
    out = io.StringIO()
    with redirect_stdout(out):
        m.main()
    text = out.getvalue()
    assert "mutants: 14" in text
    assert "boundary suite (4 years) kills 14" in text
    assert "random suite (100 years) kills 7" in text
