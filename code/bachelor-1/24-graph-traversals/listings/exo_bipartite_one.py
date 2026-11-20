"""exo_bipartite_one.py: exercise 6, a bipartite test started from one vertex only."""

from collections import deque

from graph import Graph


def bipartite_from_first(g):
    first = g.vertices()[0]
    colour, queue = {first: 0}, deque([first])
    while queue:
        u = queue.popleft()
        for v in g.adj[u]:
            if v not in colour:
                colour[v] = 1 - colour[u]
                queue.append(v)
            elif colour[v] == colour[u]:
                return False
    return True


if __name__ == "__main__":
    g = Graph(directed=False)
    for u, v in [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 5)]:  # path, triangle
        g.add_edge(u, v)
    print("bipartite?", bipartite_from_first(g))
