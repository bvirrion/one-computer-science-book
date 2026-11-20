"""inversions.py: the average number of comparisons of insertion sort, exactly."""

from fractions import Fraction
from itertools import permutations
from math import factorial

from count_ops import insertion_sort


def harmonic(n):
    return sum(Fraction(1, k) for k in range(1, n + 1))


print(f"{'n':>2} {'orders':>6} {'average':>9} {'n(n-1)/4 + n - H_n':>19}")
for n in range(1, 9):
    total = sum(insertion_sort(list(p)) for p in permutations(range(n)))
    average = Fraction(total, factorial(n))
    formula = Fraction(n * (n - 1), 4) + n - harmonic(n)
    assert average == formula
    print(f"{n:2d} {factorial(n):6d} {str(average):>9} {str(formula):>19}")
