"""exo_range.py: the points of a k-d tree inside a rectangle, and the nodes visited."""
import random

from kdtree import build


def in_range(node, lo, hi, found, visited):
    """Append to found the points p with lo <= p <= hi on both axes."""
    if node is None:
        return
    visited[0] += 1
    p, axis, left, right = node
    if all(lo[i] <= p[i] <= hi[i] for i in (0, 1)):
        found.append(p)
    if lo[axis] <= p[axis]:  # the left subtree holds coordinates <= p[axis]
        in_range(left, lo, hi, found, visited)
    if hi[axis] >= p[axis]:
        in_range(right, lo, hi, found, visited)


rng = random.Random(8)
pts = [(rng.random(), rng.random()) for _ in range(10_000)]
tree = build(pts)
boxes = [((0.2, 0.2), (0.3, 0.3)), ((0.0, 0.4), (1.0, 0.45)), ((0.5, 0.5), (0.5, 0.5))]
for lo, hi in boxes:
    found, visited = [], [0]
    in_range(tree, lo, hi, found, visited)
    brute = sorted(p for p in pts if all(lo[i] <= p[i] <= hi[i] for i in (0, 1)))
    assert sorted(found) == brute
    print(f"rectangle {lo} to {hi}: {len(found)} points, {visited[0]} nodes visited")
