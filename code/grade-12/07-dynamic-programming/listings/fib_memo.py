"""Fibonacci again: the naive recursion, then the same with a notebook of results."""
calls = 0


def fib_naive(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, memo=None):
    global calls
    calls += 1
    if memo is None:
        memo = {}
    if n in memo:                       # already computed: look it up
        return memo[n]
    value = n if n < 2 else fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    memo[n] = value                     # write it down before returning
    return value


if __name__ == "__main__":
    for n in [10, 20, 30]:
        calls = 0
        value = fib_naive(n)
        naive_calls = calls
        calls = 0
        fib_memo(n)
        print(f"fib({n}) = {value:6}   naive calls: {naive_calls:7}"
              f"   memo calls: {calls}")
    calls = 0
    print("fib(90) =", fib_memo(90), "  memo calls:", calls)
