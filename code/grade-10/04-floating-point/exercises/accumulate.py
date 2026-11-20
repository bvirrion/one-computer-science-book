"""Exercise 10: times of a timer that ticks every 0.1 s."""


def times_accumulated(n):
    t = 0.0
    out = []
    for _ in range(n):
        t += 0.1
        out.append(t)
    return out


def times_multiplied(n):
    return [k * 0.1 for k in range(1, n + 1)]


def times_exact(n):
    return [k / 10 for k in range(1, n + 1)]
