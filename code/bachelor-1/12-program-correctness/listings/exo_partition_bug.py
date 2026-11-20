"""exo_partition_bug.py: exercise 6, a partition that copies instead of swapping."""


def partition_bug(a, lo, hi):
    p = a[hi - 1]
    k = lo
    for j in range(lo, hi - 1):
        if a[j] < p:
            a[k] = a[j]
            k += 1
    a[k], a[hi - 1] = a[hi - 1], a[k]
    return k


a = [7, 2, 9, 4, 1, 8, 5]
k = partition_bug(a, 0, len(a))
print(a, "pivot at", k)
print("sorted:", sorted(a), "instead of", sorted([7, 2, 9, 4, 1, 8, 5]))
