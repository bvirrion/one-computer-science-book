from fraction import Fraction

half = Fraction(1, 2)
half._num = 2                       # reaching inside: the invariant is broken
print(half, "| equal to 1?", half == Fraction(1, 1))
print("half + half =", half + half)
