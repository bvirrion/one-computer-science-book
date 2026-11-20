"""Exercise 10: naive Fibonacci makes 2 F(n+1) - 1 calls, with at most n frames alive."""


def fib_counted(n, depth, stats):
    stats["calls"] += 1
    stats["deepest"] = max(stats["deepest"], depth)
    if n < 2:
        return n
    return fib_counted(n - 1, depth + 1, stats) + fib_counted(n - 2, depth + 1, stats)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_calls_and_depth():
    for n in range(1, 22):
        stats = {"calls": 0, "deepest": 0}
        assert fib_counted(n, 1, stats) == fib(n)
        assert stats["calls"] == 2 * fib(n + 1) - 1
        assert stats["deepest"] == n
