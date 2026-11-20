"""karatsuba.py: three half-size products instead of four."""

import digits
from digits import from_digits, normalise, school, to_digits


def difference(x, y):
    """(|x - y|, sign of x - y) for digit lists x, y of one length."""
    sign = 1
    for u, v in zip(reversed(x), reversed(y)):  # compare from the top digit
        if u != v:
            sign = 1 if u > v else -1
            break
    if sign < 0:
        x, y = y, x
    return normalise([u - v for u, v in zip(x, y)]), sign


def karatsuba(a, b, cutoff=1):
    """Product of two digit lists of one length n, a power of 2; 2n digits."""
    n = len(a)
    if n <= cutoff:
        return school(a, b)
    m = n // 2
    a0, a1, b0, b1 = a[:m], a[m:], b[:m], b[m:]  # a = a1 * 10^m + a0
    z0 = karatsuba(a0, b0, cutoff)
    z2 = karatsuba(a1, b1, cutoff)
    da, sa = difference(a1, a0)
    db, sb = difference(b1, b0)
    z1 = karatsuba(da, db, cutoff)  # (a1 - a0)(b1 - b0) = sa * sb * z1
    r = [0] * (2 * n)
    for i in range(2 * m):  # a1 b0 + a0 b1 = z2 + z0 - (a1 - a0)(b1 - b0)
        r[i] += z0[i]
        r[i + m] += z0[i] + z2[i] - sa * sb * z1[i]
        r[i + 2 * m] += z2[i]
    return normalise(r)


def multiply(x, y, method="karatsuba", cutoff=1):
    """x * y for x, y >= 0, through digit lists padded to a power of 2."""
    n = 1
    while 10**n <= max(x, y, 1):
        n *= 2
    a, b = to_digits(x, n), to_digits(y, n)
    if method == "school":
        return from_digits(school(a, b))
    return from_digits(karatsuba(a, b, cutoff))


def main():
    x, y = 1234, 5678
    for method in ("school", "karatsuba"):
        digits.products = 0
        print(f"{method:9}: {x} x {y} = {multiply(x, y, method)},"
              f" {digits.products} digit products")
    print(f"{'n':>5} {'school':>8} {'karatsuba':>9} {'3^k':>7}")
    for k in range(11):
        n = 2**k
        a = to_digits(10**n - 1, n)  # n nines
        counts = []
        for method in ("school", "karatsuba"):
            digits.products = 0
            r = school(a, a) if method == "school" else karatsuba(a, a)
            assert from_digits(r) == (10**n - 1) ** 2
            counts.append(digits.products)
        print(f"{n:5} {counts[0]:8} {counts[1]:9} {3**k:7}")


if __name__ == "__main__":
    main()
