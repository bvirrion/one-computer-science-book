import random

throws = []
for _ in range(8):
    random.seed(2026)
    throws.append(random.randint(1, 6))
print(throws)
