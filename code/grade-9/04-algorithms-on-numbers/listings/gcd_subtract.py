def gcd_subtract(a, b):
    """Euclid's algorithm by subtraction: take the smaller from the larger."""
    while a != b:
        print(a, b)
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


print("gcd:", gcd_subtract(84, 30))
