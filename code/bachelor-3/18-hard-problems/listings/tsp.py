"""tsp.py -- the travelling salesman problem on points of the plane: the exact Held-Karp
dynamic program, tree doubling (a 2-approximation), and 2-opt local search. Distances
are Euclidean, so they form a metric."""
import csv
import math
from pathlib import Path

PLACES = Path(__file__).resolve().parents[4] / "data" / "town" / "places.csv"


def town_places():
    """(name, x, y) for the town's 30 places, coordinates in metres."""
    rows = csv.DictReader(open(PLACES))
    return [(r["name"], int(r["x_m"]), int(r["y_m"])) for r in rows]


def dist(p, q):
    return math.hypot(p[1] - q[1], p[2] - q[2])


def length(points, tour):
    return sum(dist(points[a], points[b]) for a, b in zip(tour, tour[1:] + tour[:1]))


def held_karp(points):
    """Exact: best[(S, j)] = shortest path from 0 through the set S, ending at j."""
    n = len(points)
    d = [[dist(p, q) for q in points] for p in points]
    best = {(1 << j, j): (d[0][j], 0) for j in range(1, n)}
    for size in range(2, n):
        for s in range(1 << n):
            if s & 1 or bin(s).count("1") != size:
                continue
            for j in range(1, n):
                if s >> j & 1:
                    rest = s & ~(1 << j)
                    best[(s, j)] = min((best[(rest, k)][0] + d[k][j], k)
                                       for k in range(1, n) if rest >> k & 1)
    full = (1 << n) - 2
    _, j = min((best[(full, j)][0] + d[j][0], j) for j in range(1, n))
    tour, s = [], full
    while j:
        tour.append(j)
        s, j = s & ~(1 << j), best[(s, j)][1]
    return [0] + tour[::-1]


def minimum_spanning_tree(points):
    """Prim: the children of each vertex in the tree rooted at 0."""
    n = len(points)
    parent, key, done = [0] * n, [math.inf] * n, [False] * n
    key[0] = 0
    for _ in range(n):
        u = min((v for v in range(n) if not done[v]), key=lambda v: key[v])
        done[u] = True
        for v in range(n):
            if not done[v] and dist(points[u], points[v]) < key[v]:
                key[v], parent[v] = dist(points[u], points[v]), u
    children = {v: [] for v in range(n)}
    for v in range(1, n):
        children[parent[v]].append(v)
    return children


def tree_doubling(points):
    """Walk round the minimum spanning tree, skipping the vertices already visited:
    the preorder of the tree."""
    children, tour, stack = minimum_spanning_tree(points), [], [0]
    while stack:
        v = stack.pop()
        tour.append(v)
        stack.extend(reversed(children[v]))
    return tour


def two_opt(points, tour):
    """Reverse a segment whenever that shortens the tour, until no reversal does."""
    tour, improved = list(tour), True
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                a, b = points[tour[i - 1]], points[tour[i]]
                c, e = points[tour[j]], points[tour[(j + 1) % len(tour)]]
                if dist(a, c) + dist(b, e) < dist(a, b) + dist(c, e) - 1e-9:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
    return tour
