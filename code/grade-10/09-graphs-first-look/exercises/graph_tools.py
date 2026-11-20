"""Exercises 5, 6, 7, 10 and 14: small functions on a graph stored as a dict of sets."""


def degree(g, v):
    return len(g[v])


def add_friendship_buggy(g, a, b):
    g.setdefault(a, set()).add(b)          # only one end learns of the edge


def add_friendship(g, a, b):
    g.setdefault(a, set()).add(b)
    g.setdefault(b, set()).add(a)


def is_path(g, seq):
    """True if seq is a non-empty sequence of vertices, each joined to the next."""
    if not seq or seq[0] not in g:
        return False
    return all(seq[i + 1] in g[seq[i]] for i in range(len(seq) - 1))


def edges_from_dict(g):
    """The set of the edges of an undirected graph, each once as (small, big)."""
    return {(min(a, b), max(a, b)) for a in g for b in g[a]}


def common_friends(g, a, b):
    return g[a] & g[b]


def triangles(g):
    """The number of sets of three people who are all friends with one another."""
    count = 0
    for a, b in edges_from_dict(g):
        count += len(common_friends(g, a, b))
    return count // 3                     # each triangle has three edges
