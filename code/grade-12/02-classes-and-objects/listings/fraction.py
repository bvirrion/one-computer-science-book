"""Exact fractions, always reduced, with a positive denominator."""
import math


class Fraction:
    def __init__(self, num, den=1):
        if den == 0:
            raise ZeroDivisionError("a fraction with denominator 0")
        g = math.gcd(num, den)
        if den < 0:                     # the sign goes to the numerator
            g = -g
        self._num = num // g            # invariant: gcd(num, den) = 1 and den > 0
        self._den = den // g

    def numerator(self):
        return self._num

    def denominator(self):
        return self._den

    def __repr__(self):
        return f"Fraction({self._num}, {self._den})"

    def __str__(self):
        return str(self._num) if self._den == 1 else f"{self._num}/{self._den}"

    def __eq__(self, other):
        return self._num == other._num and self._den == other._den

    def __lt__(self, other):
        return self._num * other._den < other._num * self._den

    def __add__(self, other):
        return Fraction(self._num * other._den + other._num * self._den,
                        self._den * other._den)

    def __mul__(self, other):
        return Fraction(self._num * other._num, self._den * other._den)

    def __float__(self):
        return self._num / self._den
