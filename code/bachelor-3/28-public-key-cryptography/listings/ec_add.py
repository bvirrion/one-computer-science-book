"""ec_add.py -- the group law of the elliptic curve y^2 = x^3 + a x + b: the chord
through P and Q meets the curve in a third point, and P + Q is its mirror image.
Over the rationals for the figure, then over the field of 97 elements."""

from fractions import Fraction as F


def add(P, Q, a, mod=None):
    """P + Q on y^2 = x^3 + a x + b; None is the point at infinity, the neutral one."""
    if P is None or Q is None:
        return P or Q
    (x1, y1), (x2, y2) = P, Q
    inv = (lambda z: pow(z, -1, mod)) if mod else (lambda z: 1 / F(z))
    if x1 == x2 and (y1 + y2 == 0 or (mod and (y1 + y2) % mod == 0)):
        return None  # vertical line: P + (-P) = O
    if P == Q:
        slope = (3 * x1 * x1 + a) * inv(2 * y1)  # the tangent
    else:
        slope = (y2 - y1) * inv(x2 - x1)  # the chord
    x3 = slope * slope - x1 - x2
    y3 = slope * (x1 - x3) - y1
    return (x3 % mod, y3 % mod) if mod else (x3, y3)


P, Q = (F(0), F(1)), (F(3), F(5))  # on y^2 = x^3 - x + 1
S = add(P, Q, -1)
print(
    "P + Q =", f"({S[0]}, {S[1]})", " third point on the chord:", f"({S[0]}, {-S[1]})"
)
print("on the curve:", S[1] ** 2 == S[0] ** 3 - S[0] + 1)

p, a, b = 97, 2, 3
points = [
    (x, y) for x in range(p) for y in range(p) if (y * y - x**3 - a * x - b) % p == 0
]
n = len(points) + 1  # with the point at infinity
print(f"y^2 = x^3 + 2x + 3 mod 97: {n} points")
print(f"Hasse: |{n} - {p + 1}| <= 2 sqrt(p) = {2 * p**0.5:.1f}")
G, k, R = points[0], 1, points[0]
while R is not None:
    R, k = add(R, G, a, p), k + 1
print(f"G = {G} has order {k}, which divides {n}: {n % k == 0}")
