"""exo_complete.py: the merges of complete linkage on the twelve points, by name."""
from hac import PTS, hac, word

for a, b, h in hac(PTS, max):
    print(f"{word(a):>5} + {word(b):<5} at {h:.2f}")
