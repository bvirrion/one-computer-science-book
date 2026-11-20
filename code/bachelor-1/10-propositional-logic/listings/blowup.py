"""blowup.py: (x1 & y1) | ... | (xn & yn) has a CNF of 2**n clauses."""

from functools import reduce

from formula import Var, size
from normal_forms import cnf, simplify


def pairs(n):
    terms = [Var(f"x{i}") & Var(f"y{i}") for i in range(1, n + 1)]
    return reduce(lambda a, b: a | b, terms)


if __name__ == "__main__":
    print("formula for n = 3:", pairs(3))
    print(" n  size  clauses  simplified")
    for n in range(1, 11):
        f = pairs(n)
        print(f"{n:2d} {size(f):5d} {len(cnf(f)):8d} {len(simplify(cnf(f))):11d}")
