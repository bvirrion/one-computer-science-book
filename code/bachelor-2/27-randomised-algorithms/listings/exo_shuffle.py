"""exo_shuffle.py: every sequence of random choices of two shuffles of [0, 1, 2],
counted: position i swapped with any position, or with a position >= i."""
import itertools
from collections import Counter

n = 3
for name, ranges in [("swap with any position", [range(n)] * n),
                     ("Fisher-Yates          ", [range(i, n) for i in range(n)])]:
    outcomes = Counter()
    for choices in itertools.product(*ranges):
        a = list(range(n))
        for i, j in enumerate(choices):
            a[i], a[j] = a[j], a[i]
        outcomes[tuple(a)] += 1
    print(f"{name}: {sum(outcomes.values()):2} choices;",
          " ".join(f"{''.join(map(str, p))}:{c}" for p, c in sorted(outcomes.items())))
