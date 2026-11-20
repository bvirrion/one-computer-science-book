"""twosat_demo.py: six talks in two rooms, as a 2-CNF formula."""
import itertools

from twosat import solve

# x_k: talk k is in the big room. Pairs that share a speaker are in different rooms;
# talk 1 needs the big room's screen; talks 2 and 5 cannot both be in the small one.
clauses = [(1, 1), (1, 2), (-1, -2), (2, 3), (-2, -3), (3, 4), (-3, -4), (2, 5)]
for extra, name in [([], "as planned"), ([(4, 6), (-4, -6), (-6, -1)], "with talk 6")]:
    found, bad = solve(6, clauses + extra)
    if found:
        rooms = " ".join(f"{k}:{'big' if v else 'small'}" for k, v in found.items())
        print(f"{name}: {rooms}")
    else:
        print(f"{name}: no plan: x{bad}, ~x{bad} in one strongly connected component")

    def true(lit, a):
        return a[abs(lit) - 1] == (lit > 0)

    every = itertools.product([False, True], repeat=6)
    sat = [a for a in every
           if all(true(x, a) or true(y, a) for x, y in clauses + extra)]
    print(f"   by trying all 64 assignments: {len(sat)} satisfy it")
