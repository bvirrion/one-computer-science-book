def merge(a, b):
    """Merge two sorted lists into one sorted list; also count the comparisons."""
    out, i, j, comparisons = [], 0, 0, 0
    while i < len(a) and j < len(b):     # invariant: out is sorted, and holds the
        comparisons += 1                 # i smallest of a and j smallest of b
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out += a[i:] + b[j:]                 # one of the two is empty: no comparison
    return out, comparisons


if __name__ == "__main__":
    print(merge([3, 8, 12, 20], [1, 9, 10, 25, 30]))
    print(merge([1, 2, 3], [4, 5, 6]), merge([], [7, 8]))
