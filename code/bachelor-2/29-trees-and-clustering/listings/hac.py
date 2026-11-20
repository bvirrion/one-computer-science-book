"""hac.py: hierarchical agglomerative clustering of twelve points, A to L, with three
linkages; then single linkage against the minimum spanning tree."""
import math
from itertools import combinations

from dataset import small_points

PTS = small_points()
NAMES = "ABCDEFGHIJKL"
LINKS = {"single": min, "complete": max,
         "average": lambda ds: sum(ds) / len(ds)}


def hac(points, link):
    """The merges, in order, as (cluster, cluster, height); clusters are tuples."""
    clusters = [(i,) for i in range(len(points))]
    merges = []
    while len(clusters) > 1:
        def gap(pair, link=link):
            a, b = pair
            return link([math.dist(points[i], points[j]) for i in a for j in b])

        a, b = min(combinations(clusters, 2), key=gap)
        merges.append((a, b, gap((a, b))))
        clusters = [c for c in clusters if c not in (a, b)] + [tuple(sorted(a + b))]
    return merges


def cut(merges, n, k):
    """The k clusters left after the first n - k merges."""
    clusters = {(i,) for i in range(n)}
    for a, b, _ in merges[:n - k]:
        clusters -= {a, b}
        clusters.add(tuple(sorted(a + b)))
    return sorted(clusters)


def kruskal_forest(points, k):
    """Kruskal's algorithm stopped at k components: the spanning tree minus its k - 1
    heaviest edges."""
    parent = list(range(len(points)))

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i

    edges = sorted(combinations(range(len(points)), 2),
                   key=lambda e: math.dist(points[e[0]], points[e[1]]))
    components = len(points)
    for i, j in edges:
        if components == k:
            break
        if find(i) != find(j):
            parent[find(i)] = find(j)
            components -= 1
    groups = {}
    for i in range(len(points)):
        groups.setdefault(find(i), []).append(i)
    return sorted(tuple(g) for g in groups.values())


def word(c):
    return "".join(NAMES[i] for i in c)


if __name__ == "__main__":
    for name, link in LINKS.items():
        m = hac(PTS, link)
        print(f"{name:8}: merge heights", " ".join(f"{h:.2f}" for _, _, h in m))
        print("          three clusters:", " ".join(word(c) for c in cut(m, 12, 3)))
    single = hac(PTS, min)
    same = all(cut(single, 12, k) == kruskal_forest(PTS, k) for k in range(1, 13))
    print("single linkage = spanning tree cut, for every k:", same)
