"""kdtree.py: a k-d tree of points in the plane, built by medians, and the search for
the nearest point that skips the subtrees too far away."""
import random


def build(points, depth=0):
    """A node is (point, axis, left, right): the points of the left subtree have their
    coordinate on the axis at most the node's, those of the right one at least."""
    if not points:
        return None
    axis = depth % 2
    points = sorted(points, key=lambda p: p[axis])
    m = len(points) // 2
    left, right = build(points[:m], depth + 1), build(points[m + 1:], depth + 1)
    return (points[m], axis, left, right)


def dist2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def nearest(node, q, best=None, visited=None):
    """(best point, its squared distance); visited[0] counts the nodes looked at."""
    if node is None:
        return best
    if visited is not None:
        visited[0] += 1
    p, axis, left, right = node
    if best is None or dist2(p, q) < best[1]:
        best = (p, dist2(p, q))
    near, far = (left, right) if q[axis] <= p[axis] else (right, left)
    best = nearest(near, q, best, visited)
    if (q[axis] - p[axis]) ** 2 < best[1]:  # the circle crosses the splitting line
        best = nearest(far, q, best, visited)
    return best


if __name__ == "__main__":
    rng = random.Random(7)
    print("      n  mean nodes visited  most visited  brute force")
    for n in [100, 1_000, 10_000, 100_000]:
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        tree = build(pts)
        counts = []
        for _ in range(200):
            q, visited = (rng.random(), rng.random()), [0]
            p, d = nearest(tree, q, visited=visited)
            assert d == min(dist2(x, q) for x in pts)
            counts.append(visited[0])
        print(f"{n:7} {sum(counts) / len(counts):19.1f} {max(counts):13} {n:12}")
