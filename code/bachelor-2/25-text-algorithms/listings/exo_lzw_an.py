"""exo_lzw_an.py: LZW on a^n, against the formula."""
from math import isqrt

from lzw import encode


def formula(n):  # the least c with c(c + 1)/2 >= n
    c = (isqrt(8 * n + 1) - 1) // 2
    return c if c * (c + 1) // 2 >= n else c + 1


print(" ".join(str(len(encode(b"a" * n))) for n in range(1, 22)))
assert all(len(encode(b"a" * n)) == formula(n) for n in range(1, 3001))
print("n = 1..3000: the number of codes equals the formula")
