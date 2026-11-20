"""The tests of the interface: python dateset_tests.py list|set|sorted."""
import importlib
import sys
import unittest
from datetime import date

name = sys.argv.pop(1) if len(sys.argv) > 1 else "list"
ds = importlib.import_module("dateset_" + name)
NEW_YEAR, LABOUR_DAY = date(2026, 1, 1), date(2026, 5, 1)


class DatesetTests(unittest.TestCase):
    def test_empty(self):
        s = ds.empty()
        self.assertEqual(ds.size(s), 0)
        self.assertFalse(ds.contains(s, NEW_YEAR))

    def test_add_twice(self):
        s = ds.empty()
        ds.add(s, NEW_YEAR)
        ds.add(s, NEW_YEAR)
        self.assertEqual(ds.size(s), 1)

    def test_contains(self):
        s = ds.from_dates([LABOUR_DAY, NEW_YEAR, LABOUR_DAY])
        self.assertTrue(ds.contains(s, NEW_YEAR))
        self.assertFalse(ds.contains(s, date(2026, 1, 2)))
        self.assertEqual(ds.size(s), 2)


if __name__ == "__main__":
    print("implementation:", ds.__name__, flush=True)
    unittest.main(verbosity=2)
