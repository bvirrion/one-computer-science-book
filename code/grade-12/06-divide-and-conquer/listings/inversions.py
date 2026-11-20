"""How far apart are two rankings? Count the pairs they put in opposite orders."""
import random

from merge import merge


def inversions_brute(t):
    n = len(t)
    return sum(1 for i in range(n) for j in range(i + 1, n) if t[i] > t[j])


def sort_count(t):
    """Return t sorted and its number of inversions, by merge sort."""
    if len(t) <= 1:
        return list(t), 0
    mid = len(t) // 2
    left, x = sort_count(t[:mid])
    right, y = sort_count(t[mid:])
    across, i = 0, 0
    for b in right:                      # pairs (a in left, b in right) with a > b
        while i < len(left) and left[i] <= b:
            i += 1
        across += len(left) - i          # every a from left[i] on is larger than b
    return merge(left, right)[0], x + y + across


def ranking(n, seed):
    items = list(range(n))
    random.Random(seed).shuffle(items)
    return items


def compare(first, second):
    """Inversions of second, written in the positions of first."""
    place = {item: k for k, item in enumerate(first)}
    return [place[item] for item in second]


if __name__ == "__main__":
    judge_a = ["Ada", "Ben", "Cleo", "Dev", "Eli"]
    judge_b = ["Ben", "Ada", "Eli", "Cleo", "Dev"]
    t = compare(judge_a, judge_b)
    print(t, "brute force:", inversions_brute(t), "| by merging:", sort_count(t)[1])
    n = 100_000
    t = compare(ranking(n, 1), ranking(n, 2))
    count = sort_count(t)[1]
    print(f"n = {n}: {count} inversions out of {n * (n - 1) // 2} pairs,"
          f" {count / (n * (n - 1) / 2):.4f} of them")
