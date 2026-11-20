"""merge.py: merging two sorted lists, by recursion on len(xs) + len(ys)."""


def merge(xs, ys):
    if not xs:
        return ys
    if not ys:
        return xs
    if xs[0] <= ys[0]:
        return [xs[0]] + merge(xs[1:], ys)  # the variant drops by one
    return [ys[0]] + merge(xs, ys[1:])  # here too


if __name__ == "__main__":
    print(merge([1, 4, 4, 9], [2, 3, 4, 10, 11]))
    print(merge([], [5, 6]), merge([7], []))
