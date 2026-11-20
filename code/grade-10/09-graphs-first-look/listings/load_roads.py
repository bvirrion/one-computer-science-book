import csv


def load_roads(path):
    """Return the road graph: a dict place -> dict neighbour -> length in metres."""
    g = {}
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            a, b = int(row["from_place"]), int(row["to_place"])
            g.setdefault(a, {})[b] = int(row["length_m"])
            g.setdefault(b, {})
            if row["one_way"] == "0":  # a two-way road is two directed edges
                g[b][a] = int(row["length_m"])
    return g


if __name__ == "__main__":
    g = load_roads("roads.csv")
    print(len(g), "places,", sum(len(n) for n in g.values()), "directed edges")
    print("from 1 (Town Square):", g[1])
    print("from 3 (Library):    ", g[3])
