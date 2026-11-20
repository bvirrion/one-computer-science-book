"""primrec.py -- primitive recursive functions, built only from zero, successor and
projections by composition and primitive recursion; and Ackermann's function, which
needs more."""
from functools import cache


def zero(*xs):
    return 0


def succ(x):
    return x + 1


def proj(i):  # proj(i)(x0, x1, ...) = xi
    return lambda *xs: xs[i]


def compose(f, *gs):  # x -> f(g1(x), ..., gk(x))
    return lambda *xs: f(*(g(*xs) for g in gs))


def primrec(base, step):
    """h(0, ys) = base(ys); h(n + 1, ys) = step(n, h(n, ys), ys)."""
    def h(n, *ys):
        acc = base(*ys)
        for k in range(n):  # the loop runs exactly n times: no unbounded search
            acc = step(k, acc, *ys)
        return acc
    return h


add = primrec(proj(0), compose(succ, proj(1)))  # add(n, y) = n + y
mul = primrec(zero, compose(add, proj(1), proj(2)))  # mul(n, y) = n * y
power = primrec(compose(succ, zero), compose(mul, proj(1), proj(2)))  # y ** n


def mu(p):
    """Minimisation: the least n with p(n, ys) = 0. It may search for ever."""
    def f(*ys):
        n = 0
        while p(n, *ys) != 0:
            n += 1
        return n
    return f


@cache
def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


if __name__ == "__main__":
    print("add(3, 4) =", add(3, 4), " mul(3, 4) =", mul(3, 4), " power(3, 2) = 2^3 =",
          power(3, 2))
    isqrt = mu(lambda r, x: 0 if (r + 1) ** 2 > x else 1)  # least r with (r+1)^2 > x
    print("isqrt(50) by minimisation =", isqrt(50))
    for m in range(4):
        print(f"A({m}, n) for n = 0..5:", [ackermann(m, n) for n in range(6)])
