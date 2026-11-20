"""The weekend problem: k-NN against a baseline, unscaled and scaled."""
from collections import Counter

from distance import distance
from error_rate import error_rate, scaled
from parcels import make_items, split

train, validation, test = split(make_items())
common = Counter(label for _, _, label in train).most_common(1)[0][0]
for name, examples in [("validation", validation), ("test", test)]:
    wrong = sum(x[2] != common for x in examples) / len(examples)
    print(f"baseline, always '{common}', on the {name} set: {wrong:.1%}")
print(" k   unscaled   scaled   (validation set)")
best = None
for k in range(1, 16):
    raw, sc = (error_rate(train, validation, k, d) for d in (distance, scaled))
    print(f"{k:2} {raw:9.1%} {sc:8.1%}")
    if best is None or sc < best[1]:
        best = (k, sc)
k = best[0]
print(f"chosen k = {k}; final error on the untouched test set:",
      f"{error_rate(train, test, k, scaled):.1%}")
