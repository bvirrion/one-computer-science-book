from itertools import permutations

from dijkstra import dijkstra

g = {"S": {"A": 1, "B": 3}, "A": {}, "B": {"A": -3}}   # B -> A costs -3


def brute_force(g, s, t):
    """Try every simple path from s to t: possible only on tiny graphs."""
    best = None
    others = [v for v in g if v not in (s, t)]
    for k in range(len(others) + 1):
        for middle in permutations(others, k):
            path = [s, *middle, t]
            if all(b in g[a] for a, b in zip(path, path[1:])):
                cost = sum(g[a][b] for a, b in zip(path, path[1:]))
                best = cost if best is None else min(best, cost)
    return best


print("Dijkstra: S to A =", dijkstra(g, "S")[0]["A"])
print("all paths: S to A =", brute_force(g, "S", "A"))
