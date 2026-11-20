calls = 0


def fib(n):
    """fib(0) = 0, fib(1) = 1, then each is the sum of the two before."""
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


for n in [5, 10, 15, 20, 25]:
    calls = 0
    value = fib(n)
    print(f"fib({n:2}) = {value:6}   calls: {calls:7}")
