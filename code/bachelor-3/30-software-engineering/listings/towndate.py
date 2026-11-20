"""The town's date library: dates of the proleptic Gregorian calendar as
(year, month, day) triples, as the town hall's programs have used them for years."""

MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year, month):
    if month == 2 and is_leap(year):
        return 29
    return MONTH_DAYS[month - 1]


def is_valid(year, month, day):
    return 1 <= month <= 12 and 1 <= day <= days_in_month(year, month)


def day_number(year, month, day):
    """Days since 31 December of year 0: 1 January of year 1 is day 1."""
    y = year - 1
    n = 365 * y + y // 4 - y // 100 + y // 400
    for m in range(1, month):
        n += days_in_month(year, m)
    return n + day


def days_between(a, b):
    """The number of days between dates a and b, in either order."""
    n = day_number(*b) - day_number(*a)
    return n if n >= 0 else -n


def weekday(date):
    return WEEKDAYS[(day_number(*date) - 1) % 7]  # 1 January of year 1 was a Monday
