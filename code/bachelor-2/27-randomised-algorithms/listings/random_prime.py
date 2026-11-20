"""random_prime.py: random odd numbers of 256 bits tried until one passes 40 rounds of
Miller-Rabin; the number of trials counted."""
import math
import random

from primality import is_probable_prime

rng = random.Random(11)
BITS = 256
trials = []
for _ in range(200):
    count = 0
    while True:
        count += 1
        n = rng.getrandbits(BITS) | (1 << (BITS - 1)) | 1  # 256 bits, odd
        if is_probable_prime(n, 40, rng):
            break
    trials.append(count)
print(f"last prime found: {n:x}"[:60] + "...")
print(f"mean trials over 200 primes: {sum(trials) / len(trials):.1f};"
      f" (ln 2^256) / 2 = {BITS * math.log(2) / 2:.1f}")
print(f"fewest {min(trials)}, most {max(trials)}")
