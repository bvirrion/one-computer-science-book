"""sat_compare.py -- plain DPLL (chapter 17) against CDCL, in decisions and conflicts:
pigeonhole formulas (n + 1 pigeons, n holes: unsatisfiable) and random 3-SAT at 4.26
clauses per variable. Seeded, so the counts are the same on every run."""
import random
import sys
from pathlib import Path

CH17 = Path(__file__).resolve().parents[2] / "17-np-completeness" / "listings"
sys.path.insert(0, str(CH17))
import dpll  # noqa: E402
from cdcl import CDCL  # noqa: E402

sys.setrecursionlimit(10_000)


def pigeonhole(n):
    """Variable p(i, j): pigeon i in hole j. Every pigeon somewhere, no hole shared."""
    def p(i, j):
        return i * n + j + 1
    clauses = [[p(i, j) for j in range(n)] for i in range(n + 1)]
    clauses += [[-p(i, j), -p(k, j)] for j in range(n)
                for i in range(n + 1) for k in range(i + 1, n + 1)]
    return clauses, (n + 1) * n


def random_3sat(n, ratio, rng):
    return [[rng.choice((1, -1)) * v for v in rng.sample(range(1, n + 1), 3)]
            for _ in range(round(ratio * n))], n


def run_both(clauses, n):
    dpll.stats.update(decisions=0, conflicts=0)
    a = dpll.dpll(clauses)
    b, st = CDCL(clauses, n).solve()
    assert (a is None) == (b is None)
    return ("SAT" if b else "UNSAT", dpll.stats["decisions"], dpll.stats["conflicts"],
            st["decisions"], st["conflicts"])


if __name__ == "__main__":
    print("instance           answer   DPLL dec.  DPLL confl.   CDCL dec.  CDCL confl.")
    for n in (4, 5, 6, 7):
        row = run_both(*pigeonhole(n))
        counts = "".join(f"{x:>12,}" for x in row[1:])
        print(f"pigeonhole {n + 1} in {n}  {row[0]:>6}{counts}")
    rng = random.Random(18)
    for n in (30, 50, 70):
        row = run_both(*random_3sat(n, 4.26, rng))
        counts = "".join(f"{x:>12,}" for x in row[1:])
        print(f"random n = {n:<6}  {row[0]:>6}{counts}")
