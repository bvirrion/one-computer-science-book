"""Exercise 12: pairs p <= q of valid pointers into an array of n elements."""


def test_pairs():
    for n in range(0, 30):
        positions = range(n + 1)  # a + 0, ..., a + n (one past the end)
        pairs = sum(1 for p in positions for q in positions if p <= q)
        assert pairs == (n + 1) * (n + 2) // 2
