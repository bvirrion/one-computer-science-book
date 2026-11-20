"""representations.py: what each representation stores, on the town's graphs."""

from graph import friendships, roads


def sizes(g):
    n = len(g.vertices())
    m = len(g.edges())
    entries = sum(len(g.adj[v]) for v in g.vertices())  # m, or 2m if undirected
    return n, m, n * n, n + entries, 2 * m


def main():
    print(f"{'graph':12} {'n':>3} {'m':>4} {'matrix cells':>12} {'list entries':>12}"
          f" {'edge list':>9}")
    for name, g in (("roads", roads()), ("friendships", friendships())):
        n, m, matrix, lists, edge_list = sizes(g)
        print(f"{name:12} {n:3} {m:4} {matrix:12} {lists:12} {edge_list:9}")


if __name__ == "__main__":
    main()
