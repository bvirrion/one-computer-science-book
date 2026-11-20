"""exo_kd_worst.py: points on a circle, the query at its centre: the search for the
nearest point visits every node."""
from kdtree import build, nearest

pts = [(x, y) for x in range(-25, 26) for y in range(-25, 26) if x * x + y * y == 625]
for q in [(0, 0), (1, 0)]:
    visited = [0]
    p, d = nearest(build(pts), q, visited=visited)
    print(f"{len(pts)} points, query {q}: nearest {p} at squared distance {d},"
          f" {visited[0]} nodes visited")
