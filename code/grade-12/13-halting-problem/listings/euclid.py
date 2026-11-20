"""Euclid's algorithm: the greatest common divisor of a and b."""


def gcd(a, b):
    while b > 0:
        a, b = b, a % b                          # the remainder replaces the pair
    return a


print(gcd(252, 198))
