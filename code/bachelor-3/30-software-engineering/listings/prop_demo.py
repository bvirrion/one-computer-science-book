"""A property-based test finds the bug of an older day_number, which treated every
fourth year as a leap year, then shrinks the failing example to a minimal one."""

from datetime import date

from hypothesis import Phase, given, settings
from hypothesis import strategies as st


MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def old_day_number(year, month, day):  # the bug: no exception for years like 1900
    y = year - 1
    n = 365 * y + y // 4
    for m in range(1, month):
        n += 29 if m == 2 and year % 4 == 0 else MONTH_DAYS[m - 1]
    return n + day


dates = st.builds(date, st.integers(1, 9999), st.integers(1, 12), st.integers(1, 28))
tried = []


def same_as_the_calendar(a, b):  # the property: the oracle is Python's own calendar
    tried.append((a, b))
    found = old_day_number(b.year, b.month, b.day) - old_day_number(
        a.year, a.month, a.day
    )
    assert found == (b - a).days


for label, phases in [("as found", [Phase.generate]), ("after shrinking", None)]:
    tried.clear()
    test = settings(derandomize=True, database=None, phases=phases or list(Phase))(
        given(dates, dates)(same_as_the_calendar)
    )
    try:
        test()
    except AssertionError:
        a, b = tried[-1]
        print(f"{label:16} a = {a}, b = {b}, after {len(tried)} examples")
