"""uf_naive.py: two naive disjoint-set structures, one with a label per element, one
with parent pointers and no balancing; the work counted on a worst case."""


class Labels:
    """find reads a label: O(1); union relabels the whole second set: O(n)."""

    def __init__(self, items):
        self.label = {x: x for x in items}
        self.work = 0

    def find(self, x):
        return self.label[x]

    def union(self, x, y):
        a, b = self.label[x], self.label[y]
        for z in self.label:  # every element looked at
            self.work += 1
            if self.label[z] == b:
                self.label[z] = a


class Pointers:
    """union links one root under the other: O(1) after the finds; find climbs."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.work = 0

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
            self.work += 1
        return x

    def union(self, x, y):
        self.parent[self.find(y)] = self.find(x)


if __name__ == "__main__":
    for n in (100, 1000):
        for kind in (Labels, Pointers):
            s = kind(range(n))
            for i in range(1, n):  # chain: each new element joins, then one find
                s.union(i, 0)
                s.find(0)
            print(f"n = {n:4}: {kind.__name__:8} {s.work:7} steps")
