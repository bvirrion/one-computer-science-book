"""bridges.py: the edges of an undirected graph whose removal disconnects it, by the low
points of a depth-first search."""

from graph import Graph, friendships, place_names, roads


def bridges(g):
    """low[v]: the smallest discovery time reachable from v's subtree by tree edges down
    and at most one other edge. A tree edge uv is a bridge iff low[v] > disc[u]."""
    disc, low, out = {}, {}, []
    clock = 0

    def visit(u, parent_edge):
        nonlocal clock
        clock += 1
        disc[u] = low[u] = clock
        for v in g.adj[u]:
            if (v, u) == parent_edge:  # do not go back along the tree edge itself
                parent_edge = None  # (only once: a parallel edge would count)
                continue
            if v in disc:
                low[u] = min(low[u], disc[v])
            else:
                visit(v, (u, v))
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    out.append((u, v))

    for s in g.vertices():
        if s not in disc:
            visit(s, None)
    return out


def undirected_roads():
    """The road network with every road two-way, as an undirected graph."""
    g, d = Graph(directed=False), roads()
    for v in d.vertices():
        g.add_vertex(v)
    for u, v in d.edges():
        if u < v or u not in d.adj[v]:
            g.add_edge(u, v)
    return g


if __name__ == "__main__":
    b = bridges(friendships())
    pairs = sorted((min(e), max(e)) for e in b)
    print(f"friendships: {len(b)} bridges")
    print("  " + " ".join(f"{u}-{v}" for u, v in pairs))
    names = place_names()
    print(f"roads: {len(bridges(undirected_roads()))} bridges"
          f" ({len(undirected_roads().edges())} roads between {len(names)} places)")
