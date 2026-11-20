"""geometry.perimeter rewritten without indices (exercise 8); same interface."""
import math


def distance(p, q):
    """Return the distance between the points p and q."""
    return math.hypot(p[0] - q[0], p[1] - q[1])


def perimeter(points):
    """Return the length of the closed path through points, in order."""
    return sum(distance(p, q) for p, q in zip(points, points[1:] + points[:1]))
