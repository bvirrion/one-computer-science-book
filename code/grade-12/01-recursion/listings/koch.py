"""Points of the Koch curve: each segment is replaced by four, recursively."""
import math


def koch(p, q, depth, points):
    """Append to points the curve from p to q, without q itself."""
    if depth == 0:
        points.append(p)
        return
    (x1, y1), (x2, y2) = p, q
    dx, dy = (x2 - x1) / 3, (y2 - y1) / 3
    a, b = (x1 + dx, y1 + dy), (x1 + 2 * dx, y1 + 2 * dy)
    c, s = math.cos(math.pi / 3), math.sin(math.pi / 3)
    peak = (a[0] + dx * c - dy * s, a[1] + dx * s + dy * c)   # turned by 60 degrees
    for u, v in [(p, a), (a, peak), (peak, b), (b, q)]:
        koch(u, v, depth - 1, points)


def curve(depth):
    points = []
    koch((0.0, 0.0), (1.0, 0.0), depth, points)
    return points + [(1.0, 0.0)]
