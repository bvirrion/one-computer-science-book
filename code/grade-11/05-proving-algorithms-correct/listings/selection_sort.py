def check(t, i):
    """The invariant: t[:i] is sorted, and nothing in t[:i] is larger than t[i:]."""
    assert all(t[k] <= t[k + 1] for k in range(i - 1))
    assert i == 0 or i == len(t) or t[i - 1] <= min(t[i:])


def selection_sort(t):
    for i in range(len(t)):
        check(t, i)
        m = i                       # find the index m of a smallest element of t[i:]
        for j in range(i + 1, len(t)):
            if t[j] < t[m]:
                m = j
        t[i], t[m] = t[m], t[i]     # move it to place i
        print(f"turn {i}: {t[:i + 1]} | {t[i + 1:]}")
    check(t, len(t))


selection_sort([29, 12, 47, 3, 18, 12])
