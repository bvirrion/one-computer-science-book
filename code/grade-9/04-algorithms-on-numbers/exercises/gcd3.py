def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def gcd3(a, b, c):
    """The greatest common divisor of three numbers."""
    return gcd(gcd(a, b), c)


print(gcd3(84, 126, 210))
