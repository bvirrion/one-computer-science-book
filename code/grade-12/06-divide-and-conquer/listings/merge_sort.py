import random

from merge import merge


def merge_sort(t):
    """Return t sorted, and the number of comparisons made."""
    if len(t) <= 1:
        return list(t), 0
    mid = len(t) // 2
    left, c1 = merge_sort(t[:mid])           # divide, and solve each half
    right, c2 = merge_sort(t[mid:])
    merged, c3 = merge(left, right)          # combine
    return merged, c1 + c2 + c3


if __name__ == "__main__":
    print(merge_sort([38, 27, 43, 3, 9, 82, 10, 5]))
    rng = random.Random(6)
    t = [rng.randint(0, 999) for _ in range(1000)]
    s, c = merge_sort(t)
    print("1000 numbers:", s == sorted(t), "| comparisons:", c)
