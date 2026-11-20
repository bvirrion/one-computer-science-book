import unittest

VALUES = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
          (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
          (5, "V"), (4, "IV"), (1, "I")]


def roman(n):
    """Return the Roman numeral of n.

    Precondition: n is a whole number from 1 to 3999.
    """
    assert 1 <= n <= 3999, "roman numerals here go from 1 to 3999"
    text = ""
    for value, letters in VALUES:
        while n >= value:
            text = text + letters
            n = n - value
    return text


class RomanTests(unittest.TestCase):
    def test_smallest(self):
        self.assertEqual(roman(1), "I")

    def test_subtractive(self):
        self.assertEqual(roman(4), "IV")
        self.assertEqual(roman(9), "IX")
        self.assertEqual(roman(40), "XL")
        self.assertEqual(roman(900), "CM")

    def test_ordinary(self):
        self.assertEqual(roman(2026), "MMXXVI")

    def test_largest(self):
        self.assertEqual(roman(3999), "MMMCMXCIX")

    def test_out_of_range(self):
        with self.assertRaises(AssertionError):
            roman(0)
        with self.assertRaises(AssertionError):
            roman(4000)


if __name__ == "__main__":
    unittest.main()
