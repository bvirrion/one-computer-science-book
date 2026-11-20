"""Exercises of the chapter on classes and objects."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from date_class import Date, days_in_month  # noqa: E402
from fraction import Fraction  # noqa: E402


class Tally:                                       # exercise 3
    def __init__(self):
        self._count = 0

    def add(self, k=1):
        self._count += k

    def value(self):
        return self._count


def sub(a, b):                                     # exercise 6: Fraction a - b
    return Fraction(a.numerator() * b.denominator() - b.numerator() * a.denominator(),
                    a.denominator() * b.denominator())


def previous_day(d):                               # exercise 9
    year, month, day = d._ymd
    if day > 1:
        return Date(year, month, day - 1)
    if month > 1:
        return Date(year, month - 1, days_in_month(year, month - 1))
    return Date(year - 1, 12, 31)


def sum_even_squares(t):                           # exercise 11
    return sum(map(lambda x: x * x, filter(lambda x: x % 2 == 0, t)))


class Stack:                                       # exercise 12
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        return self._items == []

    def __len__(self):
        return len(self._items)


class Basket:                                      # exercise 14: the staged fault
    items = []                                     # one list, shared by every basket

    def add(self, x):
        self.items.append(x)


class BasketFixed:
    def __init__(self):
        self.items = []                            # one list per basket

    def add(self, x):
        self.items.append(x)


class Polynomial:                                  # exercise 15
    def __init__(self, coefficients):              # [a0, a1, a2, ...]
        c = list(coefficients)
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c = c

    def __add__(self, other):
        n = max(len(self.c), len(other.c))
        a = self.c + [0] * (n - len(self.c))
        b = other.c + [0] * (n - len(other.c))
        return Polynomial([x + y for x, y in zip(a, b)])

    def __mul__(self, other):
        out = [0] * (len(self.c) + len(other.c) - 1)
        for i, x in enumerate(self.c):
            for j, y in enumerate(other.c):
                out[i + j] += x * y
        return Polynomial(out)

    def __call__(self, x):
        result = 0
        for a in reversed(self.c):                  # Horner's scheme
            result = result * x + a
        return result

    def __repr__(self):
        return f"Polynomial({self.c})"


if __name__ == "__main__":
    a, b = Basket(), Basket()
    a.add("pear")
    print(b.items, sub(Fraction(1, 2), Fraction(1, 3)), previous_day(Date(2028, 3, 1)))
    p = Polynomial([1, 1]) * Polynomial([1, 1])
    print(p, p(2), sum_even_squares(range(7)))
