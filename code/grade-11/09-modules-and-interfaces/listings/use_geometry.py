import geometry
from geometry import perimeter

square = [(0, 0), (3, 0), (3, 3), (0, 3)]
print(geometry.distance((0, 0), (3, 4)))
print(perimeter(square))
print("module:", geometry.__name__, "| this program:", __name__)
print("names in geometry:", [n for n in dir(geometry) if not n.startswith("__")])
