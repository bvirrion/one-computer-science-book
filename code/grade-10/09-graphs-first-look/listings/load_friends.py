import csv


def load_friends(path, people=range(1, 41)):
    """Return the friendship graph: a dict person -> set of friends."""
    g = {p: set() for p in people}  # every person is a vertex, even without friends
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            a, b = int(row["person_a"]), int(row["person_b"])
            g[a].add(b)  # an undirected edge is stored
            g[b].add(a)  # at both of its ends
    return g


if __name__ == "__main__":
    g = load_friends("friendships.csv")
    print(len(g), "vertices")
    print("friends of 1:", sorted(g[1]), " friends of 28:", sorted(g[28]))
    print("without friends:", [p for p in g if not g[p]])
