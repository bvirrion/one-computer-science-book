"""matching.py: maximum bipartite matching by augmenting paths."""


def augmenting_path(u, adj, match, seen):
    """Try to match left vertex u: take a free neighbour, or one whose partner can be
    moved to another neighbour. Returns True if the matching grew."""
    for v in adj[u]:
        if v in seen:
            continue
        seen.add(v)
        if v not in match or augmenting_path(match[v], adj, match, seen):
            match[v] = u  # flip the alternating path
            return True
    return False


def max_matching(adj, log=None):
    """adj: left vertex -> its right neighbours. Returns {right: left}."""
    match = {}
    for u in adj:
        before = dict(match)
        if augmenting_path(u, adj, match, set()) and log is not None:
            log.append((u, {v: w for v, w in match.items() if before.get(v) != w}))
    return match
