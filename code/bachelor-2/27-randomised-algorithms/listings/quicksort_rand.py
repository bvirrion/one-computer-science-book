"""quicksort_rand.py: randomised quicksort on the sorted list, 1,000 seeds."""
import random
from fractions import Fraction

from quicksort import quicksort, random_pivot
from town import people

names = sorted(people())
n = len(names)
counts = []
for seed in range(1000):
    count = [0]
    quicksort(names, random_pivot(random.Random(seed)), count)
    counts.append(count[0])
H = sum(Fraction(1, k) for k in range(1, n + 1))
exact = 2 * (n + 1) * H - 4 * n
print(f"n = {n}: mean {sum(counts) / len(counts):.1f} comparisons over 1,000 runs;"
      f" 2(n+1)H_n - 4n = {float(exact):.1f}")
print(f"smallest {min(counts)}, largest {max(counts)}, worst case {n * (n - 1) // 2}")
over = sum(c > 1.5 * exact for c in counts)
print(f"runs above 1.5 x {float(exact):.1f}: {over}")
