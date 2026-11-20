"""knn.py: the k-nearest-neighbour classifier on the noisy loans, every feature scaled
to [0, 1] by its range on the training set."""
from collections import Counter

from dataset import FEATURES, loans


def scaler(train, features=FEATURES):
    lo = {f: min(x[f] for x, _ in train) for f in features}
    hi = {f: max(x[f] for x, _ in train) for f in features}
    return lambda x: [(x[f] - lo[f]) / (hi[f] - lo[f]) for f in features]


def knn_classify(train_vectors, query, k):
    """The majority label among the k training vectors closest to query; a tie goes
    to the label of the nearest of them. Cost: one distance per training example."""
    def d2(vy):
        return sum((a - b) ** 2 for a, b in zip(vy[0], query))

    near = sorted(train_vectors, key=d2)[:k]
    counts = Counter(y for _, y in near).most_common()
    if len(counts) > 1 and counts[0][1] == counts[1][1]:
        return near[0][1]
    return counts[0][0]


def evaluate(train, test, k, features=FEATURES, scale=True):
    s = scaler(train, features) if scale else (lambda x: [x[f] for f in features])
    tv = [(s(x), y) for x, y in train]
    return sum(knn_classify(tv, s(x), k) == y for x, y in test) / len(test)


if __name__ == "__main__":
    train, test = loans(700, seed=1, noise=0.15), loans(300, seed=2, noise=0.15)
    for k in [1, 3, 5, 9, 15, 25]:
        both = evaluate(train, test, k, ["prior", "distance"])
        print(f"k = {k:2}: test accuracy {evaluate(train, test, k):.3f}",
              f"| prior and distance only: {both:.3f}")
    print(f"each answer computed {len(train)} distances in {len(FEATURES)} dimensions")
