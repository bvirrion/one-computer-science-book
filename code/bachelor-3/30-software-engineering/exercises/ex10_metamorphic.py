"""Exercise 10: metamorphic tests for a sort, with no oracle. merge_sort has an
injected bug, which one of the three relations finds."""


def merge_sort(xs):
    if len(xs) <= 1:
        return list(xs)
    a, b = merge_sort(xs[: len(xs) // 2]), merge_sort(xs[len(xs) // 2 :])
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            out.append(a[i])
            i += 1
        elif b[j] < a[i]:
            out.append(b[j])
            j += 1
        else:  # the injected bug: equal heads are merged into one
            out.append(a[i])
            i, j = i + 1, j + 1
    return out + a[i:] + b[j:]


def permuted_input_same_output(sort, xs, perm):  # relation 1
    return sort([xs[p] for p in perm]) == sort(xs)


def doubled_input_doubled_output(sort, xs):  # relation 2
    return sort(xs + xs) == [x for x in sort(xs) for _ in range(2)]


def shifted_input_shifted_output(sort, xs, c):  # relation 3
    return sort([x + c for x in xs]) == [x + c for x in sort(xs)]
