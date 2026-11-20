# capture: exit
walls = {(0, 1): "wall", (2, 3): "door"}
print(walls[(2, 3)])
print((0, 1) in walls, (1, 0) in walls)

walls[[4, 4]] = "window"
