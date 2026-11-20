"""ex9_overhead.py -- Amdahl's law with a cost per processor: normalised to T_1 = 1,
T(p) = f + (1 - f)/p + c p. The best p, and the speed-up it gives."""

from math import sqrt


def time(p, f, c):
    return f + (1 - f) / p + c * p


def best(f, c, pmax=10_000):
    return min(range(1, pmax + 1), key=lambda p: time(p, f, c))


if __name__ == "__main__":
    for f, c in ((0.05, 0.001), (0.05, 0.0001), (0.01, 0.001)):
        p = best(f, c)
        print(
            f"f = {f}, c = {c}: best p = {p} (root {sqrt((1 - f) / c):.1f}), "
            f"speed-up {1 / time(p, f, c):.2f}, against {1 / f:.0f} without the cost"
        )
