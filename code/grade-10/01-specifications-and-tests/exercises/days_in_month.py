import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from leap_fixed import leap_year  # noqa: E402


def days_in_month(month, year):
    """Return the number of days of month (1 to 12) in year (1583 or later)."""
    if month == 2:
        return 29 if leap_year(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


class DaysInMonthTests(unittest.TestCase):
    def test_long_month(self):
        self.assertEqual(days_in_month(1, 2025), 31)

    def test_last_month(self):
        self.assertEqual(days_in_month(12, 2025), 31)

    def test_short_month(self):
        self.assertEqual(days_in_month(4, 2025), 30)

    def test_february_common(self):
        self.assertEqual(days_in_month(2, 2025), 28)

    def test_february_leap(self):
        self.assertEqual(days_in_month(2, 2024), 29)

    def test_february_century(self):
        self.assertEqual(days_in_month(2, 1900), 28)

    def test_february_four_hundred(self):
        self.assertEqual(days_in_month(2, 2000), 29)


if __name__ == "__main__":
    unittest.main()
