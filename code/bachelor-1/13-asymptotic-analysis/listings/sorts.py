"""sorts.py: merge sort, and the maximum, both counting their comparisons."""


def merge_sort(a, counter):
    """Returns a sorted copy of a; counter[0] counts the comparisons."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid], counter), merge_sort(a[mid:], counter)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def maximum(a, counter):
    m = a[0]
    for x in a[1:]:
        counter[0] += 1
        m = max(m, x)
    return m
