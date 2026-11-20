def insertion_sort(t):
    for i in range(1, len(t)):
        assert all(t[k] <= t[k + 1] for k in range(i - 1))   # outer: t[:i] is sorted
        x = t[i]
        j = i
        while j > 0 and t[j - 1] > x:
            # inner: t[j + 1:i + 1] holds elements larger than x, moved one place right
            t[j] = t[j - 1]
            j = j - 1
        t[j] = x
        print(f"turn {i}: {t[:i + 1]} | {t[i + 1:]}   ({x} went to place {j})")


insertion_sort([29, 12, 47, 3, 18, 12])
