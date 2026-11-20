"""The exact quicksort average, five keys in seven comparisons, the loans sorted twice."""

import sys
from fractions import Fraction
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

from loans_by_member import by_member_then_date, loans  # noqa: E402
from lower_bound import merge_insertion_worst, merge_sort_worst  # noqa: E402
from qs_average import exact_average, formula  # noqa: E402
from sort5 import insertion_sort, merge_insertion5, merge_sort, survey  # noqa: E402


def test_quicksort_average():
    for n in range(1, 8):
        assert exact_average(n) == formula(n)
    assert formula(3) == Fraction(8, 3)


def test_five_keys():
    assert max(survey(lambda ks: merge_insertion5(*ks))) == 7
    assert max(survey(insertion_sort)) == 10 and max(survey(merge_sort)) == 8


def test_worst_cases():
    assert [merge_sort_worst(n) for n in (5, 8, 16)] == [8, 17, 49]
    assert merge_insertion_worst(5) == 7 and merge_insertion_worst(12) == 30


def test_loans_twice():
    rows = loans()
    assert by_member_then_date(rows) == sorted(rows, key=lambda r: (r[0], r[1]))
