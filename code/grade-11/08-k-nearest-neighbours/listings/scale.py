"""Millimetres against grams: rescale each feature to the range 0 to 1."""
from distance import distance
from knn import neighbours, predict
from parcels import make_items, split


def scaler(train):
    """Min-max scaling, computed on the training set only."""
    lo = [min(e[i] for e in train) for i in (0, 1)]
    hi = [max(e[i] for e in train) for i in (0, 1)]
    return lambda e: tuple((e[i] - lo[i]) / (hi[i] - lo[i]) for i in (0, 1)) + (e[2],)


if __name__ == "__main__":
    train, _, _ = split(make_items())
    s = scaler(train)
    new = (12.0, 150, "?")
    print("scaled new item:", tuple(round(v, 3) for v in s(new)[:2]))

    def scaled(a, b):
        return distance(s(a), s(b))

    for e in neighbours(train, new, 7, dist=scaled):
        print(f"  {e[0]:5} mm {e[1]:5} g  {e[2]:7} at {scaled(e, new):.3f}")
    print("k = 7, scaled:", predict(train, new, 7, dist=scaled))
