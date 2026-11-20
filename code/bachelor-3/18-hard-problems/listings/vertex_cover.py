"""vertex_cover.py -- take both ends of every edge of a maximal matching: a vertex cover
at most twice the smallest. Compared with the exact minimum on random graphs."""
import itertools
import random


def matching_cover(edges):
    cover = set()
    for u, v in edges:  # an edge with no end covered yet joins the matching
        if u not in cover and v not in cover:
            cover |= {u, v}
    return cover


def minimum_cover(n, edges):
    for k in range(n + 1):
        for c in itertools.combinations(range(n), k):
            if all(u in c or v in c for u, v in edges):
                return set(c)


if __name__ == "__main__":
    rng = random.Random(18)
    print(" n   edges   matching cover   minimum   ratio")
    for n in (8, 10, 12, 14):
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.3]
        a, b = len(matching_cover(edges)), len(minimum_cover(n, edges))
        print(f"{n:>2}   {len(edges):>5}   {a:>14}   {b:>7}   {a / b:.2f}")
    k = 5  # five disjoint edges: the matching takes 10 vertices, 5 suffice
    edges = [(2 * i, 2 * i + 1) for i in range(k)]
    print(f"{k} disjoint edges: matching cover {len(matching_cover(edges))}, "
          f"minimum {len(minimum_cover(2 * k, edges))}")
