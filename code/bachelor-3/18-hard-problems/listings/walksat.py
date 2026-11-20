"""walksat.py -- local search for satisfiability: from a random assignment, pick an
unsatisfied clause and flip one of its variables, until every clause holds or the
budget runs out. It can find an assignment; it can never prove there is none."""
import random

from cdcl import CDCL
from sat_compare import random_3sat


def walksat(clauses, n, rng, noise=0.5, max_flips=20_000):
    value = {v: rng.random() < 0.5 for v in range(1, n + 1)}

    def sat(c):
        return any(value[abs(x)] == (x > 0) for x in c)

    def breaks(v):  # clauses satisfied now that flipping v would falsify
        value[v] = not value[v]
        count = sum(1 for c in clauses if v in map(abs, c) and not sat(c))
        value[v] = not value[v]
        return count
    for flips in range(max_flips):
        unsat = [c for c in clauses if not sat(c)]
        if not unsat:
            return value, flips
        c = rng.choice(unsat)
        if rng.random() < noise:
            v = abs(rng.choice(c))  # a random walk step
        else:
            v = min((abs(x) for x in c), key=breaks)  # the greedy step
        value[v] = not value[v]
    return None, max_flips


if __name__ == "__main__":
    rng = random.Random(18)
    print("  n   clauses   CDCL says   WalkSAT flips (5 seeded runs)")
    for n in (20, 40, 60, 80):
        clauses, _ = random_3sat(n, 4.0, rng)
        runs = [walksat(clauses, n, random.Random(s))[1] for s in range(5)]
        answer = "SAT" if CDCL(clauses, n).solve()[0] else "UNSAT"
        print(f"{n:>3}   {len(clauses):>7}   {answer:>9}   "
              + " ".join(f"{f:>6,}" for f in runs))
