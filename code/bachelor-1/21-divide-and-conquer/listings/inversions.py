"""inversions.py: counting inversions by merge sort: divide, solve, combine."""


def sort_count(a):
    """(sorted copy of a, number of pairs i < j with a[i] > a[j])."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, x = sort_count(a[:mid])  # divide, and solve each half
    right, y = sort_count(a[mid:])
    merged, z, i = [], 0, 0  # combine: merge, counting the pairs split by mid
    for r in right:
        while i < len(left) and left[i] <= r:
            merged.append(left[i])
            i += 1
        z += len(left) - i  # r is smaller than every key left in `left`
        merged.append(r)
    merged += left[i:]
    return merged, x + y + z


if __name__ == "__main__":
    print(sort_count([3, 1, 4, 1, 5, 9, 2, 6]))
