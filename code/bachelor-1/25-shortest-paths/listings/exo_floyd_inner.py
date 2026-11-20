"""exo_floyd_inner.py: exercise 6, the triple loop with k innermost."""

from floyd import floyd_warshall
from wgraph import roads

INF = float("inf")


def floyd_k_inner(adj):
    order = list(adj)
    index = {v: i for i, v in enumerate(order)}
    n = len(order)
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u in adj:
        for v, w in adj[u]:
            d[index[u]][index[v]] = min(d[index[u]][index[v]], w)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


if __name__ == "__main__":
    adj = roads()
    good, bad = floyd_warshall(adj)[1], floyd_k_inner(adj)
    wrong = sum(good[i][j] != bad[i][j] for i in range(30) for j in range(30))
    print(f"wrong entries: {wrong} of 900")
