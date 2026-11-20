from collections import Counter

from distance import distance
from parcels import make_items, split


def neighbours(train, x, k, dist=distance):
    return sorted(train, key=lambda e: dist(e, x))[:k]


def vote(near):
    """The most common class; a tie goes to the class of the nearest among them."""
    count = Counter(label for _, _, label in near)
    best = max(count.values())
    return next(label for _, _, label in near if count[label] == best)


def predict(train, x, k, dist=distance):
    return vote(neighbours(train, x, k, dist))


if __name__ == "__main__":
    train, _, _ = split(make_items())
    new = (12.0, 150, "?")                      # 12 mm, 150 g: which class?
    for e in neighbours(train, new, 7):
        print(f"  {e[0]:5} mm {e[1]:5} g  {e[2]:7} at {distance(e, new):6.1f}")
    for k in [1, 3, 7]:
        near = neighbours(train, new, k)
        print(f"k = {k}: {predict(train, new, k)}",
              dict(Counter(label for _, _, label in near)))
