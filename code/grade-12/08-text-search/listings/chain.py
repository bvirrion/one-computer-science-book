"""A million letters from A, C, G, T: how much of it does each search read?"""
import random

from horspool import horspool
from naive import search_naive
from shift_table import shift_table

rng = random.Random(2026)
n = 1_000_000
text = "".join(rng.choice("ACGT") for _ in range(n))
print("first letters:", text[:40])
for m in [4, 8, 16, 32]:
    naive_total = hors_total = jump_total = 0
    for _ in range(5):                       # five patterns cut from the text
        start = rng.randrange(n - m)
        p = text[start:start + m]
        found, naive_c = search_naive(text, p)
        found_h, hors_c = horspool(text, p)
        assert found == found_h
        naive_total += naive_c
        hors_total += hors_c
        table = shift_table(p)
        jump_total += sum(table.get(c, m) for c in "ACGT") / 4
    print(f"m = {m:2}: naive {naive_total / 5 / n:.3f} per letter,"
          f" Horspool {hors_total / 5 / n:.3f}, ratio {naive_total / hors_total:.1f},"
          f" mean jump {jump_total / 5:.2f}")
