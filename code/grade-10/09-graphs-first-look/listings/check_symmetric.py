from load_friends import load_friends
from load_roads import load_roads


def one_way_edges(g):
    """Return the edges (a, b) of g whose reverse (b, a) is missing."""
    return [(a, b) for a in g for b in g[a] if a not in g[b]]


print("friendships:", one_way_edges(load_friends("friendships.csv")))
print("roads:      ", one_way_edges(load_roads("roads.csv")))
