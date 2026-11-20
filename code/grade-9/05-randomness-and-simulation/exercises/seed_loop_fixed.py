import random

random.seed(2026)                  # once, before the loop
throws = []
for _ in range(8):
    throws.append(random.randint(1, 6))
print(throws)
