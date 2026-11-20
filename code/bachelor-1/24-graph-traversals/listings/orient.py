"""orient.py: every road made one-way so that every place still reaches every other:
tree edges of a depth-first search downwards, the other edges upwards."""

from bridges import bridges, undirected_roads
from graph import Graph
from kosaraju import kosaraju


def orient(g):
    """A strongly connected orientation of a connected graph without bridges."""
    disc, arcs = {}, Graph(directed=True)
    for v in g.vertices():
        arcs.add_vertex(v)

    def visit(u):
        disc[u] = len(disc)
        for v in g.adj[u]:
            if v not in disc:
                arcs.add_edge(u, v)  # tree edge: from parent to child
                visit(v)
            elif disc[v] < disc[u] and v not in arcs.adj[u] and u not in arcs.adj[v]:
                arcs.add_edge(u, v)  # back edge: from descendant up to ancestor

    visit(g.vertices()[0])
    return arcs


if __name__ == "__main__":
    g = undirected_roads()
    assert not bridges(g)
    o = orient(g)
    print(f"{len(o.edges())} one-way roads for {len(g.edges())} roads;"
          f" strongly connected components: {len(kosaraju(o))}")
    print("road 1 goes", "from 1 to 3, as now" if 3 in o.adj[1] else "from 3 to 1")
