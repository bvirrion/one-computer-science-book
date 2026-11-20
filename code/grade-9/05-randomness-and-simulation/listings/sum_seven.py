import random

random.seed(4)
throws = 100_000
sevens = 0
for _ in range(throws):
    if random.randint(1, 6) + random.randint(1, 6) == 7:
        sevens = sevens + 1
print(f"simulated: {sevens} sevens in {throws} throws, {sevens / throws:.4f}")

ways = 0
for a in range(1, 7):
    for b in range(1, 7):
        if a + b == 7:
            ways = ways + 1
print(f"exact: {ways} ways out of 36, {ways / 36:.4f}")
