import math


class Point:
    """A point of the plane."""

    def __init__(self, x, y):          # the constructor: sets the attributes
        self.x = x
        self.y = y

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


a, b = Point(0, 0), Point(3, 4)
print(a.distance_to(b))                # Point.distance_to(a, b)
c = b
c.move(1, 1)                           # c and b are the same object
print(b.x, b.y, "| same object:", b is c)
d = Point(4, 5)
print("equal coordinates:", d.x == b.x and d.y == b.y, "| same object:", d is b)
print(type(a).__name__, isinstance(a, Point))
