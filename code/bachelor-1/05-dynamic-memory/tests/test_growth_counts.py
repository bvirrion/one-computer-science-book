"""Exercises 9, 10 and 12: copies and peak memory of growth by +k and by doubling."""


def copies_plus_k(n, k):
    copies, cap = 0, k
    while cap < n:
        copies += cap
        cap += k
    return copies


def copies_doubling(n):
    copies, cap = 0, 1
    while cap < n:
        copies += cap
        cap *= 2
    return copies


def test_plus_k_is_quadratic():
    assert copies_plus_k(1000, 16) == 31248  # the +16 row of policies.txt
    for n in (100, 1000, 5000):
        for k in (1, 4, 16):
            m = (n - 1) // k
            assert copies_plus_k(n, k) == k * m * (m + 1) // 2


def test_doubling_below_2n_and_peak_below_3n():
    for n in range(1, 5000):
        assert copies_doubling(n) < 2 * n
        cap = 1
        while cap < n:
            cap *= 2
        last_old = cap // 2 if cap > 1 else 0
        assert last_old + cap <= 3 * n  # old block + new block during the last move
