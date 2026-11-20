"""selinger.py -- choose a join order by dynamic programming over sets of relations:
left-deep plans, no cross products, costs in page I/O. Each join is a hash join,
3(L + P), or a sort-merge join, which sorts both inputs (the left one only if it is
not already sorted on the join column) and then reads both."""

import math
import random
from itertools import combinations

from sort_ext import formula as sort_cost


def pages(tuples):
    return max(1, math.ceil(tuples / 10))


def methods(left_pages, right_pages, left_order, col, B):
    """(name, cost, order of the output) of each way to join."""
    sort_left = 0 if left_order == col else sort_cost(left_pages, B)
    merge = sort_left + sort_cost(right_pages, B) + left_pages + right_pages
    return [("hash", 3 * (left_pages + right_pages), None), ("merge", merge, col)]


def best_plan(sizes, preds, B=10):
    """sizes: {relation: tuples}; preds: {frozenset({x, y}): (column, selectivity)}.
    Returns (cost, estimated tuples, plan) and the number of plans costed."""
    best, costed = {}, 0
    for r, t in sizes.items():
        best[frozenset([r])] = (0, t, r, None)
    for k in range(2, len(sizes) + 1):
        for S in map(frozenset, combinations(sorted(sizes), k)):
            for r in sorted(S):
                left = S - {r}
                ps = [preds[p] for p in preds if r in p and p - {r} <= left]
                if left not in best or not ps:
                    continue  # no cross products
                cost, t, plan, order = best[left]
                out = t * sizes[r] * math.prod(sel for _, sel in ps)
                for name, c, new_order in methods(
                    pages(t), pages(sizes[r]), order, ps[0][0], B
                ):
                    costed += 1
                    if S not in best or cost + c < best[S][0]:
                        best[S] = (cost + c, out, f"({plan} {name} {r})", new_order)
    cost, t, plan, _ = best[frozenset(sizes)]
    return (cost, t, plan), costed


def random_query(n, shape, rng):
    names = [f"R{i}" for i in range(1, n + 1)]
    sizes = {r: rng.choice([100, 1000, 10_000, 100_000]) for r in names}
    pairs = (
        zip(names, names[1:])
        if shape == "chain"
        else ((names[0], r) for r in names[1:])
    )
    preds = {
        frozenset(p): (f"{p[0]}.{p[1]}", 1 / max(sizes[p[0]], sizes[p[1]]))
        for p in pairs
    }
    return sizes, preds


if __name__ == "__main__":
    rng = random.Random(22)
    for n in (4, 5, 6):
        for shape in ("chain", "star"):
            sizes, preds = random_query(n, shape, rng)
            (cost, t, plan), costed = best_plan(sizes, preds)
            print(
                f"{shape} of {n}: {math.factorial(n)} orders, {costed} plans costed, "
                f"best {cost:,} page I/O"
            )
            print(f"  {plan}")
