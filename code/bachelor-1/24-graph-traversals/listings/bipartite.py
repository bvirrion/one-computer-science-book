"""bipartite.py: two-colouring a graph by BFS, or an odd cycle proving it impossible."""

from collections import deque

from graph import friendships


def two_colour(g):
    """(colour, None) if g is bipartite, else (None, an odd cycle as a vertex list)."""
    colour, parent = {}, {}
    for s in g.vertices():  # every component
        if s in colour:
            continue
        colour[s], parent[s] = 0, None
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in g.adj[u]:
                if v not in colour:
                    colour[v], parent[v] = 1 - colour[u], u
                    queue.append(v)
                elif colour[v] == colour[u]:  # an edge inside one colour
                    return None, odd_cycle(parent, u, v)
    return colour, None


def odd_cycle(parent, u, v):
    """The two tree paths from u and v up to their common ancestor, plus the edge uv."""
    up_u, up_v = [u], [v]
    while up_u[-1] is not None:
        up_u.append(parent[up_u[-1]])
    while up_v[-1] is not None:
        up_v.append(parent[up_v[-1]])
    ancestors = set(up_v)
    top = next(x for x in up_u if x in ancestors)
    return up_u[:up_u.index(top) + 1] + up_v[:up_v.index(top)][::-1]


if __name__ == "__main__":
    colour, cycle = two_colour(friendships())
    if cycle:
        print(f"not bipartite: odd cycle of length {len(cycle)}:",
              " - ".join(map(str, cycle)))
