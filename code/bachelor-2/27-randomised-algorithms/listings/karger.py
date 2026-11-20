"""karger.py: Karger's contraction algorithm for a minimum cut of a multigraph."""


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def contract(vertices, edges, rng, log=None):
    """Contract random edges until two super-vertices remain. Taking the edges in a
    random order and skipping those inside a super-vertex picks each contraction
    uniformly among the edges left. Returns the cut: the edges between the two."""
    parent = {v: v for v in vertices}
    left = len(vertices)
    order = list(edges)
    rng.shuffle(order)
    for u, v in order:
        if left == 2:
            break
        ru, rv = find(parent, u), find(parent, v)
        if ru != rv:  # an edge inside a super-vertex would be a self-loop
            parent[ru] = rv
            left -= 1
            if log is not None:
                log.append((u, v))
    side = {v for v in vertices if find(parent, v) == find(parent, vertices[0])}
    return [(u, v) for u, v in edges if (u in side) != (v in side)], side


def karger(vertices, edges, runs, rng):
    """The smallest cut found in independent runs."""
    return min((contract(vertices, edges, rng) for _ in range(runs)),
               key=lambda r: len(r[0]))
