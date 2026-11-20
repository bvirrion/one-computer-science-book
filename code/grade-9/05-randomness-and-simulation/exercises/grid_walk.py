import random

random.seed(6)
x = 0
y = 0
for _ in range(100):
    move = random.choice(["up", "down", "left", "right"])
    if move == "up":
        y = y + 1
    elif move == "down":
        y = y - 1
    elif move == "left":
        x = x - 1
    else:
        x = x + 1
print("end:", x, y, " steps back home along the grid:", abs(x) + abs(y))
