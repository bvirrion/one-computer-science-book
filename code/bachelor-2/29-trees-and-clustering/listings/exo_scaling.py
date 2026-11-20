"""exo_scaling.py: k-nearest neighbours on the raw features, then scaled."""
from dataset import loans
from knn import evaluate

train, test = loans(700, seed=1, noise=0.15), loans(300, seed=2, noise=0.15)
for k in [5, 9]:
    print(f"k = {k}: raw features {evaluate(train, test, k, scale=False):.3f},"
          f" scaled {evaluate(train, test, k):.3f}")
lo = {f: min(x[f] for x, _ in train) for f in train[0][0]}
hi = {f: max(x[f] for x, _ in train) for f in train[0][0]}
print("ranges:", ", ".join(f"{f} {lo[f]}-{hi[f]}" for f in lo))
