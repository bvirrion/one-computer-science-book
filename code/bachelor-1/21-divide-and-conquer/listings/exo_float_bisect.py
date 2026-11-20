"""exo_float_bisect.py: exercise 6, a dichotomy on reals with an absolute tolerance."""


def cube_root(y, tolerance=1e-12, limit=2000):
    lo, hi = 0.0, max(1.0, y)
    steps = 0
    while hi - lo > tolerance:
        mid = (lo + hi) / 2
        if mid**3 < y:
            lo = mid
        else:
            hi = mid
        steps += 1
        if steps == limit:  # a guard, so that the demonstration stops
            print(f"y = {y:g}: stuck after {steps} steps, lo = {lo!r}, hi = {hi!r},"
                  f" mid == hi: {mid == hi}")
            return None
    return lo


if __name__ == "__main__":
    for y in (2.0, 1e6, 1e15):
        r = cube_root(y)
        if r is not None:
            print(f"y = {y:g}: {r!r} after the loop")
