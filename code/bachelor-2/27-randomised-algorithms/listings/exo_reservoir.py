"""exo_reservoir.py: a uniform sample of k items from a stream of unknown length,
in one pass; checked exhaustively on a short stream."""
import itertools
import random
from collections import Counter


def reservoir(stream, k, choose):
    """Keep the first k items; item i (from 0) then replaces a random kept item with
    probability k/(i + 1). choose(i) returns a uniform number in 0..i."""
    sample = []
    for i, x in enumerate(stream):
        if i < k:
            sample.append(x)
        else:
            j = choose(i)
            if j < k:
                sample[j] = x
    return sample


n, k = 6, 2
counts = Counter()
for choices in itertools.product(*[range(i + 1) for i in range(k, n)]):
    it = iter(choices)
    counts[frozenset(reservoir(range(n), k, lambda i, it=it: next(it)))] += 1
print(f"{sum(counts.values())} choice sequences, {len(counts)} samples of {k} out of"
      f" {n}, each obtained {set(counts.values())} times")
rng = random.Random(3)
lines = [f"loan {i}" for i in range(10_000)]
print("5 lines out of 10,000:", reservoir(lines, 5, lambda i: rng.randrange(i + 1)))
