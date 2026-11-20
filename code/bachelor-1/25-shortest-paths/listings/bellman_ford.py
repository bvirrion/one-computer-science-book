"""bellman_ford.py: shortest paths with any weights, by rounds of relaxation of every
arc; a round that still improves after n - 1 rounds reveals a negative cycle."""

from wgraph import roads

INF = float("inf")


def bellman_ford(adj, s):
    """(dist, parent, rounds), or None if a negative cycle is reachable from s."""
    dist, parent = {v: INF for v in adj}, {s: None}
    dist[s] = 0
    for rounds in range(1, len(adj) + 1):
        changed = False
        for u in adj:
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v], parent[v] = dist[u] + w, u
                    changed = True
        if not changed:
            return dist, parent, rounds  # a round without change: nothing will change
    return None  # still changing at round n: a negative cycle


def main():
    adj = roads()
    dist, _, rounds = bellman_ford(adj, 1)
    print(f"roads in seconds: stable after {rounds} rounds out of at most {len(adj)},"
          f" Hospital at {dist[8]} s")
    neg = {"s": [("a", 2), ("b", 3)], "a": [("t", 1)], "b": [("a", -2)], "t": []}
    print("the negative arc:", bellman_ford(neg, "s")[0])
    neg["t"].append(("b", 0))  # a cycle b -> a -> t -> b of weight -1
    print("with the arc t -> b:", bellman_ford(neg, "s"))


if __name__ == "__main__":
    main()
