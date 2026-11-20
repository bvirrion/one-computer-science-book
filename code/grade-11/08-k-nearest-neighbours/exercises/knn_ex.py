"""Exercises of the chapter on k nearest neighbours."""
import math
from collections import Counter


def distance(a, b):                                # exercise 5: any number of features
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a[:-1], b[:-1])))


def knn_predict(train, x, k):                      # exercise 7
    near = sorted(train, key=lambda e: distance(e, x))[:k]
    count = Counter(e[-1] for e in near)
    best = max(count.values())
    return next(e[-1] for e in near if count[e[-1]] == best)


def minmax(train):                                 # exercise 11
    d = len(train[0]) - 1
    lo = [min(e[i] for e in train) for i in range(d)]
    hi = [max(e[i] for e in train) for i in range(d)]
    def scale(e):
        return tuple((e[i] - lo[i]) / (hi[i] - lo[i]) for i in range(d)) + (e[-1],)
    return scale


def loo_error_buggy(items, k):                     # exercise 6: the item votes too
    return sum(knn_predict(items, x, k) != x[-1] for x in items) / len(items)


def loo_error(items, k):                           # exercise 13: leave one out
    wrong = 0
    for i, x in enumerate(items):
        others = items[:i] + items[i + 1:]
        wrong += knn_predict(others, x, k) != x[-1]
    return wrong / len(items)


def weighted_predict(train, x, k):                 # exercise 15: weights 1/distance
    score = Counter()
    for e in sorted(train, key=lambda e: distance(e, x))[:k]:
        score[e[-1]] += 1 / (distance(e, x) + 1e-9)
    return score.most_common(1)[0][0]


TINY = [(1, 1, "A"), (2, 1, "A"), (4, 3, "B"), (5, 4, "B"), (3, 2, "A")]

if __name__ == "__main__":
    print(distance((0, 0, "?"), (3, 4, "?")), knn_predict(TINY, (4, 4, "?"), 3))
    print([e[:2] for e in sorted(TINY, key=lambda e: distance(e, (3.5, 3, "?")))])
    print(loo_error_buggy(TINY, 1), loo_error(TINY, 1))
