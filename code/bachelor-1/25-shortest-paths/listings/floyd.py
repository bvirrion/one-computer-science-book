"""floyd.py: all shortest travel times in town, by Floyd--Warshall on the matrix."""

from dijkstra import dijkstra, path
from wgraph import names, roads

INF = float("inf")


def floyd_warshall(adj):
    """(order, d, nxt): d[i][j] is the distance from order[i] to order[j], nxt[i][j]
    the index of the vertex after order[i] on a shortest path to order[j]."""
    order = list(adj)
    index = {v: i for i, v in enumerate(order)}
    n = len(order)
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    nxt = [[j if i == j else None for j in range(n)] for i in range(n)]
    for u in adj:
        for v, w in adj[u]:
            if w < d[index[u]][index[v]]:
                d[index[u]][index[v]], nxt[index[u]][index[v]] = w, index[v]
    for k in range(n):  # now paths may go through vertices 0..k
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    nxt[i][j] = nxt[i][k]
    return order, d, nxt


def route(order, nxt, a, b):
    i, j = order.index(a), order.index(b)
    out = [a]
    while i != j:
        i = nxt[i][j]
        out.append(order[i])
    return out


def main():
    adj, name = roads(), names()
    order, d, nxt = floyd_warshall(adj)
    n = len(order)
    agree = all(dijkstra(adj, a)[0][b] == d[i][j]
                for i, a in enumerate(order) for j, b in enumerate(order))
    print(f"{n} x {n} table, {n ** 3} steps of the triple loop;"
          f" equal to {n} runs of Dijkstra: {agree}")
    for a, b in ((1, 8), (8, 1), (1, 3), (3, 1)):
        r = route(order, nxt, a, b)
        k = len(r) - 1
        print(f"{name[a]} -> {name[b]}: {d[order.index(a)][order.index(b)]} s,"
              f" {k} road{'s' if k > 1 else ''}, same route as Dijkstra:"
              f" {r == path(dijkstra(adj, a)[1], b)}")


if __name__ == "__main__":
    main()
