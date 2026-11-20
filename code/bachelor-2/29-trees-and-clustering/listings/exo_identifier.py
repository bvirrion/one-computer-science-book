"""exo_identifier.py: the gain of a split with one branch per value, for each feature
and for the loan's number; then the gain ratio."""
import math
from collections import Counter, defaultdict

from dataset import loans
from id3 import entropy

data = loans(700, seed=1, noise=0.15)
train = [(dict(x, number=i), y) for i, (x, y) in enumerate(data)]  # a loan's number
h = entropy(Counter(y for _, y in train))
for f in ["days", "prior", "number"]:
    branches = defaultdict(Counter)
    for x, y in train:
        branches[x[f]][y] += 1
    sizes = Counter({v: sum(c.values()) for v, c in branches.items()})
    gain = h - sum(sizes[v] / len(train) * entropy(c) for v, c in branches.items())
    split_info = entropy(sizes)
    print(f"{f:7}: {len(branches):3} branches, gain {gain:.3f} bits,"
          f" split information {split_info:.3f}, gain ratio {gain / split_info:.3f}")
print(f"entropy of the labels: {h:.3f} bits; log2 700 = {math.log2(700):.3f}")
