"""id3.py: decision trees grown by ID3 with binary splits on numeric features."""
import math
from collections import Counter

from dataset import FEATURES, loans


def entropy(counts):
    """The entropy in bits of a distribution given by counts, a Counter."""
    n = sum(counts.values())
    return -sum(c / n * math.log2(c / n) for c in counts.values() if c)


def best_split(data):
    """The (gain, feature, threshold) of largest information gain, or None."""
    labels = Counter(y for _, y in data)
    h, n, best = entropy(labels), len(data), None
    for f in FEATURES:
        pairs = sorted((x[f], y) for x, y in data)
        left, right = Counter(), Counter(labels)
        for i in range(n - 1):
            v, y = pairs[i]
            left[y] += 1
            right[y] -= 1
            if v == pairs[i + 1][0]:
                continue  # a threshold must separate distinct values
            k = i + 1  # examples on the left
            gain = h - k / n * entropy(left) - (n - k) / n * entropy(right)
            if gain > 1e-12 and (best is None or gain > best[0] + 1e-12):
                best = (gain, f, (v + pairs[i + 1][0]) / 2)
    return best


def id3(data, max_depth=99):
    """A tree: ("leaf", label, counts) or ("split", feature, threshold, left, right),
    the left branch for the values at most the threshold."""
    counts = Counter(y for _, y in data)
    split = best_split(data) if max_depth > 0 else None
    if split is None:  # pure, or no split gains anything, or the depth is reached
        return ("leaf", int(counts[1] > counts[0]), (counts[0], counts[1]))
    _, f, t = split
    left = [(x, y) for x, y in data if x[f] <= t]
    right = [(x, y) for x, y in data if x[f] > t]
    return ("split", f, t, id3(left, max_depth - 1), id3(right, max_depth - 1))


def predict(tree, x):
    while tree[0] == "split":
        _, f, t, left, right = tree
        tree = left if x[f] <= t else right
    return tree[1]


def accuracy(tree, data):
    return sum(predict(tree, x) == y for x, y in data) / len(data)


def show(tree, indent=""):
    if tree[0] == "leaf":
        word = "late" if tree[1] else "on time"
        print(f"{indent}-> {word} (on time {tree[2][0]}, late {tree[2][1]})")
        return
    _, f, t, left, right = tree
    print(f"{indent}{f} <= {t:g}")
    show(left, indent + "    ")
    print(f"{indent}{f} > {t:g}")
    show(right, indent + "    ")


def depth(tree):
    return 0 if tree[0] == "leaf" else 1 + max(depth(tree[3]), depth(tree[4]))


if __name__ == "__main__":
    train, test = loans(700, seed=1), loans(300, seed=2)
    tree = id3(train)
    show(tree)
    print(f"depth {depth(tree)}; test accuracy {accuracy(tree, test):.3f}")
