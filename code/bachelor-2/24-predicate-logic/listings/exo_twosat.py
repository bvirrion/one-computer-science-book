"""exo_twosat.py: the 2-CNF formula of exercise 4."""
from twosat import solve

BASE = [(1, 2), (-1, 3), (-2, -3), (-3, 1)]
for clauses in [BASE, BASE + [(-1, -3)], BASE + [(-1, -3), (1, 3)]]:
    found, bad = solve(3, clauses)
    print(clauses, "->", found if found else f"unsatisfiable, x{bad} with ~x{bad}")
