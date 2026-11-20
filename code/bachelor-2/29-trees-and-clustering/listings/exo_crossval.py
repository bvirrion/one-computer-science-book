"""exo_crossval.py: 5-fold cross-validation of the tree's depth on the noisy loans."""
from dataset import loans
from id3 import accuracy, id3

data = loans(700, seed=1, noise=0.15)
folds = [data[i::5] for i in range(5)]
for d in [0, 1, 2, 3, 4, 6, 8, 12]:
    scores = []
    for i in range(5):
        rest = [e for j in range(5) if j != i for e in folds[j]]
        scores.append(accuracy(id3(rest, d), folds[i]))
    print(f"depth {d:2}: mean {sum(scores) / 5:.3f}, folds",
          " ".join(f"{s:.3f}" for s in scores))
