import sys
import unittest

if len(sys.argv) > 1 and sys.argv[1] == "fixed":
    from leap_fixed import leap_year
else:
    from leap import leap_year


class LeapYearTests(unittest.TestCase):
    def test_ordinary_leap(self):
        self.assertTrue(leap_year(2024))

    def test_ordinary_common(self):
        self.assertFalse(leap_year(2023))

    def test_century_common(self):
        self.assertFalse(leap_year(1900))

    def test_four_hundred(self):
        self.assertTrue(leap_year(2000))

    def test_first_year(self):
        self.assertFalse(leap_year(1583))


unittest.main(argv=sys.argv[:1], verbosity=2)
