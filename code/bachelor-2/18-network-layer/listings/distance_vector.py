"""distance_vector.py: synchronous distance vector (distributed Bellman-Ford)."""
INF = 16                                       # RIP's infinity


def dv_round(graph, tables, inf=INF, poison=False):
    """Every router rebuilds its table from its neighbours' tables of the last round."""
    new = {}
    for u in sorted(graph):
        t = {u: (0, u)}
        for v in sorted(graph[u]):
            for d, (dist, hop) in sorted(tables[v].items()):
                if poison and hop == u and d != v:
                    dist = inf                 # poisoned reverse: "not via me"
                cand = min(dist + graph[u][v], inf)
                if d not in t or cand < t[d][0]:
                    t[d] = (cand, v)
        new[u] = t
    return new


def converge(graph, tables=None, inf=INF, poison=False, limit=100):
    """Run rounds until nothing changes; return the tables and the changing rounds."""
    tables = tables or {u: {u: (0, u)} for u in graph}
    for rounds in range(limit):
        new = dv_round(graph, tables, inf, poison)
        if new == tables:
            return tables, rounds
        tables = new
    return tables, limit


def show(tables):
    return "  ".join(
        u + ": " + " ".join(f"{d}{tables[u][d][0]}" for d in sorted(tables[u]))
        for u in sorted(tables))


def link(graph, a, b, cost):
    graph.setdefault(a, {})[b] = cost
    graph.setdefault(b, {})[a] = cost


if __name__ == "__main__":
    g = {}
    for a, b, c in [("A", "B", 1), ("B", "C", 2), ("A", "C", 4), ("C", "D", 1)]:
        link(g, a, b, c)
    tables = {u: {u: (0, u)} for u in g}
    for r in range(1, 5):
        tables = dv_round(g, tables)
        print(f"round {r}  {show(tables)}")

    line = {}
    link(line, "A", "B", 1)
    link(line, "B", "C", 1)
    tables, _ = converge(line)
    del line["B"]["C"], line["C"]["B"]         # the link from B to C fails
    print("line A-B-C (costs 1), link B-C fails; distances to C:")
    for r in range(1, 20):
        tables = dv_round(line, tables)
        (a, via_a), (b, via_b) = tables["A"]["C"], tables["B"]["C"]
        print(f"round {r:2}  A {a:2} via {via_a}  B {b:2} via {via_b}")
        if a == b == INF:
            break
