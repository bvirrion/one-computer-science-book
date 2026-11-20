import random

from merge_sort import merge_sort

rng = random.Random(1)
print(f"{'n':>5} {'h':>3} {'sorted input':>13} {'random input':>13}"
      f" {'n*h':>6} {'n*n/2':>9}")
for h in range(1, 11):
    n = 2 ** h
    t = list(range(n))
    shuffled = rng.sample(t, n)
    print(f"{n:5} {h:3} {merge_sort(t)[1]:13} {merge_sort(shuffled)[1]:13}"
          f" {n * h:6} {n * n // 2:9}")
