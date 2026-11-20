import math


class Shape:
    def area(self):
        raise NotImplementedError("each kind of shape gives its own area")

    def describe(self):                   # inherited by every subclass
        return f"{type(self).__name__} of area {self.area():.2f}"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):                       # overrides Shape.area
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)      # the constructor of Rectangle


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


for shape in [Rectangle(3, 2), Square(4), Circle(1)]:
    print(shape.describe(), "| a Rectangle?", isinstance(shape, Rectangle))
