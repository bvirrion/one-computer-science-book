"""Dijkstra's algorithm, picking the closest unfinished vertex by a scan."""


def dijkstra(g, source, show=False):
    dist, parent, done = {source: 0}, {source: None}, set()
    while True:
        waiting = [v for v in dist if v not in done]
        if not waiting:
            return dist, parent
        u = min(waiting, key=lambda v: dist[v])     # its distance is now final
        done.add(u)
        for v, w in g[u].items():
            if v not in done and (v not in dist or dist[u] + w < dist[v]):
                dist[v] = dist[u] + w                # a shorter way to v, through u
                parent[v] = u
        if show:
            row = "  ".join(f"{v}:{dist[v]:>2}" if v in dist else f"{v}: -" for v in g)
            print(f"finish {u}   {row}")


W = {"S": {"A": 4, "B": 1}, "A": {"S": 4, "B": 2, "C": 5},
     "B": {"S": 1, "A": 2, "D": 8}, "C": {"A": 5, "D": 1, "T": 3},
     "D": {"B": 8, "C": 1, "T": 6}, "T": {"C": 3, "D": 6}}

if __name__ == "__main__":
    dist, parent = dijkstra(W, "S", show=True)
    path, v = [], "T"
    while v is not None:
        path, v = [v] + path, parent[v]
    print("distance S to T:", dist["T"], "| path:", " ".join(path))
