"""lower_bound.py: ceil(lg n!), the fewest comparisons that can sort n keys in the worst
case, against the worst cases of insertion sort, merge sort and merge insertion."""

from math import ceil, factorial, log2


def merge_sort_worst(n):
    """Worst case of top-down merge sort: W(n) = W(floor) + W(ceil) + n - 1."""
    if n < 2:
        return 0
    return merge_sort_worst(n // 2) + merge_sort_worst(n - n // 2) + n - 1


def merge_insertion_worst(n):
    """The worst case of merge insertion: the sum of ceil(lg(3k/4)) for k = 1..n."""
    return sum(ceil(log2(3 * k / 4)) for k in range(1, n + 1))


def main():
    print(f"{'n':>2} {'lg n!':>7} {'bound':>5} {'insertion':>9} {'merge':>5} "
          f"{'merge insertion':>15}")
    for n in range(2, 17):
        lg = log2(factorial(n))
        print(f"{n:2} {lg:7.2f} {ceil(lg):5} {n * (n - 1) // 2:9} "
              f"{merge_sort_worst(n):5} {merge_insertion_worst(n):15}")


if __name__ == "__main__":
    main()
