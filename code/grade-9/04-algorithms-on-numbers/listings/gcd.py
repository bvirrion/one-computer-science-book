def gcd(a, b):
    """Euclid's algorithm by division; also the number of division steps."""
    steps = 0
    while b != 0:
        a, b = b, a % b
        steps = steps + 1
    return a, steps


if __name__ == "__main__":
    for a, b in [[84, 30], [1071, 462], [1_000_000, 999_999]]:
        print(a, b, "->", gcd(a, b))
