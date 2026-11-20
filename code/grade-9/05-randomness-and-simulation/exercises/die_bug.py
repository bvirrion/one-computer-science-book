import random

random.seed(3)
counts = [0, 0, 0, 0, 0, 0, 0]
for _ in range(70_000):
    face = random.randint(0, 6)
    counts[face] = counts[face] + 1
print(counts)
