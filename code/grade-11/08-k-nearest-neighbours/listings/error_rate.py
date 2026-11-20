"""Errors on examples kept aside, for each k, with scaled features."""
from distance import distance
from knn import predict
from parcels import make_items, split
from scale import scaler


def error_rate(train, examples, k, dist):
    wrong = sum(predict(train, x, k, dist) != x[2] for x in examples)
    return wrong / len(examples)


train, validation, _ = split(make_items())
s = scaler(train)


def scaled(a, b):
    return distance(s(a), s(b))


if __name__ == "__main__":
    for k in range(1, 16):
        on_train = error_rate(train, train, k, scaled)
        on_validation = error_rate(train, validation, k, scaled)
        print(f"k = {k:2}: error on the training set {on_train:6.1%},"
              f" on the validation set {on_validation:6.1%}")
