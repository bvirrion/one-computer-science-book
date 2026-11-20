"""fib_memo.py: Fibonacci numbers, naively and with memoisation, counting the calls."""

calls = 0


def fib_naive(n):
    global calls
    calls += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, memo=None):
    global calls
    calls += 1
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:  # each subproblem is solved once, then read from the table
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_table(n):
    """Bottom-up: the table filled in increasing order, two cells kept."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    global calls
    print(f"{'n':>3} {'F(n)':>7} {'naive calls':>12} {'memoised calls':>15}")
    for n in (5, 10, 15, 20, 25):
        calls = 0
        value = fib_naive(n)
        naive = calls
        calls = 0
        assert fib_memo(n) == value == fib_table(n)
        print(f"{n:3} {value:7} {naive:12} {calls:15}")


if __name__ == "__main__":
    main()
