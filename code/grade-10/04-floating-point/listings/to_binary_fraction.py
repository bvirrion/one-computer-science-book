from fractions import Fraction


def binary_fraction(x, n):
    """Return the first n binary digits after the point of x, a Fraction, 0 <= x < 1."""
    digits = ""
    for _ in range(n):
        x = 2 * x
        if x >= 1:
            digits += "1"
            x = x - 1
        else:
            digits += "0"
    return digits


print("0.375 = 0." + binary_fraction(Fraction(3, 8), 8))
print("0.1   = 0." + binary_fraction(Fraction(1, 10), 30))
print("1/3   = 0." + binary_fraction(Fraction(1, 3), 30))
