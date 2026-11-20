"""partition.py: Lomuto's partition of a[lo:hi] around the pivot a[hi - 1]."""


def partition(a, lo, hi, trace=False):
    """Precondition: lo < hi. Rearranges a[lo:hi] and returns k with
    a[lo:k] < p, a[k] == p, a[k+1:hi] >= p, where p is the pivot a[hi - 1]."""
    p = a[hi - 1]
    k = lo
    for j in range(lo, hi - 1):
        # invariant: a[lo:k] < p and a[k:j] >= p; a[j:hi-1] not yet seen
        if trace:
            print(f"j={j} k={k} {a[lo:k]} | {a[k:j]} | {a[j:hi - 1]} pivot {p}")
        if a[j] < p:
            a[k], a[j] = a[j], a[k]
            k += 1
    a[k], a[hi - 1] = a[hi - 1], a[k]  # the pivot between the two regions
    return k


if __name__ == "__main__":
    a = [7, 2, 9, 4, 1, 8, 5]
    k = partition(a, 0, len(a), trace=True)
    print("result", a, "pivot at", k)
