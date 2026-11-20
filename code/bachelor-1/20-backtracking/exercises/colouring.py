"""colouring.py: a 3-colouring by backtracking, vertices in decreasing degree."""


def colour(vertices, edges, k=3):
    """A dict vertex -> colour in range(k) with no edge inside one colour, or None."""
    neighbours = {v: set() for v in vertices}
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    order = sorted(vertices, key=lambda v: -len(neighbours[v]))  # most neighbours first
    colours = {}

    def visit(i):
        if i == len(order):
            return True
        v = order[i]
        used = {colours[u] for u in neighbours[v] if u in colours}
        for c in range(k):
            if c not in used:
                colours[v] = c
                if visit(i + 1):
                    return True
                del colours[v]
        return False

    return dict(colours) if visit(0) else None
