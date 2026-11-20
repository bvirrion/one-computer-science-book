from fraction import Fraction

a, b = Fraction(6, 8), Fraction(1, -3)
print(a, b, repr(a))
print(a + b, a * b, a + b == Fraction(5, 12))
print(sorted([Fraction(2, 3), Fraction(1, 2), Fraction(3, 5)]))
print(float(Fraction(1, 3)), Fraction(10, 5))
try:
    Fraction(1, 0)
except ZeroDivisionError as error:
    print("ZeroDivisionError:", error)
