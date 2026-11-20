"""rk_demo.py: spurious hits for two moduli, on the town archive."""
from rabin_karp import rabin_karp
from text_gen import archive

text = archive()
for pattern in ["Riverside", "borrowed Seven Forest", "Hilltop, -2.3"]:
    for q in [97, 1_000_003]:
        found, spurious = rabin_karp(text, pattern, q)
        expected = (len(text) - len(pattern) + 1) / q
        print(f"{pattern!r:24} q = {q:9}: {len(found):3} occurrences,",
              f"{spurious:4} spurious (estimate {expected:5.1f})")
