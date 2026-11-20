"""Points of the plane as pairs (x, y): distances and perimeters."""
import math


def _square(v):
    return v * v


def distance(p, q):
    """Return the distance between the points p and q."""
    return math.sqrt(_square(p[0] - q[0]) + _square(p[1] - q[1]))


def perimeter(points):
    """Return the length of the closed path through points, in order.

    points is a list of at least two pairs (x, y); the path goes back
    from the last point to the first.
    """
    total = 0.0
    for i in range(len(points)):
        total += distance(points[i], points[(i + 1) % len(points)])
    return total
