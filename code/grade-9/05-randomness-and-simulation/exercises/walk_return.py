import random

random.seed(20)
walks = 100_000
home = 0
for _ in range(walks):
    position = 0
    for _ in range(20):
        position = position + random.choice([-1, 1])
    if position == 0:
        home = home + 1
print(f"simulated: {home / walks:.4f}")

ways = {0: 1}                          # position: number of paths that reach it
for _ in range(20):
    new = {}
    for position in ways:
        for move in [-1, 1]:
            new[position + move] = new.get(position + move, 0) + ways[position]
    ways = new
print(f"exact: {ways[0]} paths of {2 ** 20}, {ways[0] / 2 ** 20:.4f}")
