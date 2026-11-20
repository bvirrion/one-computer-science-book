"""Dates of the calendar, always valid."""


def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year, month):
    if month == 2:
        return 29 if is_leap(year) else 28
    return 30 if month in (4, 6, 9, 11) else 31


class Date:
    def __init__(self, year, month, day):
        if not (1 <= month <= 12 and 1 <= day <= days_in_month(year, month)):
            raise ValueError(f"no such date: {year}-{month}-{day}")
        self._ymd = (year, month, day)          # invariant: a real date

    def __str__(self):
        return "{:04}-{:02}-{:02}".format(*self._ymd)

    def __eq__(self, other):
        return self._ymd == other._ymd

    def __lt__(self, other):
        return self._ymd < other._ymd           # tuples compare year first

    def next_day(self):
        year, month, day = self._ymd
        if day < days_in_month(year, month):
            return Date(year, month, day + 1)
        if month < 12:
            return Date(year, month + 1, 1)
        return Date(year + 1, 1, 1)
