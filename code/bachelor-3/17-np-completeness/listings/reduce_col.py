"""reduce_col.py -- 3-SAT to 3-colouring. A palette triangle T, F, B names the colours;
each variable is a pair x, not x joined to B, so one is T and the other F; each clause
is two OR gadgets in a chain whose output is forced to T."""
import random

from cnf import brute_force, is_colourable, random_3cnf

T, F, B = 0, 1, 2


def to_colouring(clauses, n):
    edges = [(T, F), (F, B), (B, T)]
    def lit(x):  # the vertex of literal x: 3, 4 for x_1, not x_1; 5, 6 for x_2 ...
        return 3 + 2 * (abs(x) - 1) + (x < 0)
    for i in range(1, n + 1):
        edges += [(lit(i), lit(-i)), (lit(i), B), (lit(-i), B)]
    size = 3 + 2 * n

    def gadget(a, b):  # OR gadget: a triangle u, v, out with u - a and v - b
        nonlocal size
        u, v, out = size, size + 1, size + 2
        size += 3
        edges.extend([(u, a), (v, b), (u, v), (v, out), (out, u)])
        return out
    for a, b, c in clauses:
        out = gadget(gadget(lit(a), lit(b)), lit(c))
        edges.extend([(out, F), (out, B)])  # the clause's output must be T
    return size, edges


if __name__ == "__main__":
    formula = [[1, -2, 3], [-1, 2, -3]]
    size, edges = to_colouring(formula, 3)
    n, m = 3, len(formula)
    print(f"n = {n} variables, m = {m} clauses: {size} vertices, {len(edges)} edges")
    print(f"  2n + 6m + 3 = {2 * n + 6 * m + 3}, 3n + 12m + 3 = {3 * n + 12 * m + 3}")
    rng, agree, unsat = random.Random(17), 0, 0
    for _ in range(30):
        f = random_3cnf(3, rng.randrange(1, 9), rng)
        size, edges = to_colouring(f, 3)
        unsat += brute_force(f) is None
        agree += (brute_force(f) is not None) == is_colourable(size, edges, 3)
    print(f"satisfiable = 3-colourable: {agree} of 30 random formulas "
          f"({unsat} unsatisfiable)")
    every = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    size, edges = to_colouring(every, 3)  # each clause forbids one assignment
    print(f"all 8 clauses on x1, x2, x3: satisfiable {brute_force(every) is not None}, "
          f"3-colourable {is_colourable(size, edges, 3)}")
