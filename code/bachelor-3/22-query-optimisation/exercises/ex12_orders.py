"""ex12_orders.py -- Selinger's dynamic programming with interesting orders: for each
set of relations keep the cheapest plan for every order of its output, not only the
cheapest plan, so that a sorted result can save a later sort."""

import math
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from selinger import methods, pages  # noqa: E402


def best_plan_orders(sizes, preds, B=10):
    best, costed = {}, 0  # (set, order) -> (cost, tuples, plan)
    for r, t in sizes.items():
        best[(frozenset([r]), None)] = (0, t, r)
    for k in range(2, len(sizes) + 1):
        for S in map(frozenset, combinations(sorted(sizes), k)):
            for r in sorted(S):
                left = S - {r}
                ps = [preds[p] for p in preds if r in p and p - {r} <= left]
                if not ps:
                    continue
                for (L, order), (cost, t, plan) in list(best.items()):
                    if L != left:
                        continue
                    out = t * sizes[r] * math.prod(sel for _, sel in ps)
                    for name, c, new_order in methods(
                        pages(t), pages(sizes[r]), order, ps[0][0], B
                    ):
                        costed += 1
                        key = (S, new_order)
                        if key not in best or cost + c < best[key][0]:
                            best[key] = (cost + c, out, f"({plan} {name} {r})")
    final = [v for (S, _), v in best.items() if S == frozenset(sizes)]
    return min(final), costed


QUERY = (  # four relations of 50 tuples (5 pages) joined in a chain on one column k
    {"R1": 50, "R2": 50, "R3": 50, "R4": 50},
    {
        frozenset({"R1", "R2"}): ("k", 1 / 50),
        frozenset({"R2", "R3"}): ("k", 1 / 50),
        frozenset({"R3", "R4"}): ("k", 1 / 50),
    },
)

if __name__ == "__main__":
    from selinger import best_plan

    for name, f in (
        ("best plan only", best_plan),
        ("interesting orders", best_plan_orders),
    ):
        (cost, t, plan), costed = f(*QUERY)
        print(f"{name}: {cost:,} page I/O, {costed} plans costed\n  {plan}")
