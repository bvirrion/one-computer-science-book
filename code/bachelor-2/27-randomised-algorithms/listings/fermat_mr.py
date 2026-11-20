"""fermat_mr.py: 561 = 3 x 11 x 17 against the two tests, every base tried."""
from math import gcd

from primality import fermat_passes, miller_rabin_passes

for n in [561, 1105, 1729, 1009]:
    bases = range(2, n - 1)
    coprime = [a for a in bases if gcd(a, n) == 1]
    fermat = sum(fermat_passes(n, a) for a in coprime)
    strong = sum(miller_rabin_passes(n, a) for a in bases)
    print(f"n = {n:4}: Fermat passes {fermat:4} of {len(coprime):4} coprime bases;"
          f" Miller-Rabin passes {strong:4} of {len(bases)} bases")
