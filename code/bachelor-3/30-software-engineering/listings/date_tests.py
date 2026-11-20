"""The town date library's tests: the first suite, then the two tests added after
the mutation analysis (their names start with test_new_)."""

from datetime import date

from towndate import day_number, days_between, days_in_month, is_leap, is_valid, weekday


def test_leap_years():
    assert is_leap(2024) and not is_leap(2026)


def test_month_lengths():
    assert days_in_month(2024, 2) == 29 and days_in_month(2026, 2) == 28
    assert days_in_month(2026, 1) == 31


def test_validity():
    assert is_valid(2026, 1, 31) and not is_valid(2026, 2, 30)
    assert not is_valid(2026, 13, 1)


def test_days_between():
    assert days_between((2026, 1, 1), (2026, 3, 1)) == 59
    assert days_between((2026, 3, 1), (2026, 1, 1)) == 59


def test_weekday():
    assert weekday((2026, 11, 20)) == "Friday"


def test_new_against_datetime():  # an oracle: Python's own calendar
    for year in (1, 100, 101, 400, 401, 1900, 2000, 2026):
        for month in range(1, 13):
            assert day_number(year, month, 1) == date(year, month, 1).toordinal()


def test_new_boundaries():
    assert is_valid(2026, 1, 1) and is_valid(2026, 12, 31)
    assert not is_valid(2026, 1, 0) and not is_valid(2026, 12, 32)
    assert not is_valid(2026, 2, 29)
