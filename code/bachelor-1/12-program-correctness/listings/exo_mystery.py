"""exo_mystery.py: exercise 11, a loop to understand."""


def mystery(x, n):
    """Precondition: n >= 0."""
    acc, base, e = 1, x, n
    while e > 0:
        if e % 2 == 1:
            acc = acc * base
        base = base * base
        e = e // 2
    return acc


print(mystery(3, 13), mystery(2, 10), mystery(7, 0))
