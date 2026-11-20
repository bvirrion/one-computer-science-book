"""exo_monte_carlo.py: what k rounds of Miller-Rabin report for 1729 = 7 x 13 x 19."""
import random

from primality import is_probable_prime

rng = random.Random(8)
liars = 160 / 1726  # the fraction of bases 2..1727 that 1729 passes (fermat_mr.py)
for k in [1, 2, 3, 5]:
    wrong = sum(is_probable_prime(1729, k, rng) for _ in range(100_000))
    print(f"k = {k}: 'prime' in {wrong:6} of 100,000 runs;"
          f" ({liars:.4f})^k x 100,000 = {liars ** k * 100_000:8.1f}")
