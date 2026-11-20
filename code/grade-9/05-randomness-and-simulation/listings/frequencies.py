import random

random.seed(3)
print("throws    sixes  frequency")
for throws in [10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
               10_000, 20_000, 50_000, 100_000]:
    sixes = 0
    for _ in range(throws):
        if random.randint(1, 6) == 6:
            sixes = sixes + 1
    print(f"{throws:>7} {sixes:>7}  {sixes / throws:.4f}")
print(f"1/6 is {1 / 6:.4f}")
