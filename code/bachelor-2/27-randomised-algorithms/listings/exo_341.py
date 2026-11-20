"""exo_341.py: 341 = 11 x 31 and the Fermat test."""
from math import gcd

from primality import fermat_passes, miller_rabin_passes

n = 341
coprime = [a for a in range(2, n - 1) if gcd(a, n) == 1]
liars = [a for a in coprime if fermat_passes(n, a)]
print(f"{len(coprime)} coprime bases in 2..{n - 2}; Fermat liars: {len(liars)},"
      f" the first ones {liars[:8]}")
print(f"2^340 mod 341 = {pow(2, 340, n)}; 3^340 mod 341 = {pow(3, 340, n)}")
print(f"2^85 mod 341 = {pow(2, 85, n)}, 2^170 mod 341 = {pow(2, 170, n)};"
      f" Miller-Rabin with base 2 passes: {miller_rabin_passes(n, 2)}")
