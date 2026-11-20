"""The heights of search trees built from 1000 random orders of 1..1023."""
import random
from collections import Counter

from bst import build
from node import height


def heights(n=1023, trials=1000, seed=2026):
    rng = random.Random(seed)
    keys = list(range(1, n + 1))
    out = []
    for _ in range(trials):
        rng.shuffle(keys)
        out.append(height(build(keys)))
    return out


if __name__ == "__main__":
    h = heights()
    print("smallest", min(h), "| largest", max(h), "| mean", round(sum(h) / len(h), 2))
    counts = Counter(h)
    print(" ".join(f"{k}:{counts[k]}" for k in sorted(counts)))
