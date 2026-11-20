import time

from is_prime import is_prime
from sieve import sieve

start = time.perf_counter()
count = 0
for n in range(100_000):
    if is_prime(n)[0]:
        count = count + 1
middle = time.perf_counter()
by_sieve = len(sieve(100_000))
end = time.perf_counter()
print(f"trial division: {count} primes in {middle - start:.3f} s")
print(f"sieve:          {by_sieve} primes in {end - middle:.3f} s")
