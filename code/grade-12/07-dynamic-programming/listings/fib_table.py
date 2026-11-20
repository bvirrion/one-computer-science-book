"""Fibonacci bottom-up: fill the table from the small values upwards."""


def fib_table(n):
    table = [0] * (n + 1)
    if n >= 1:
        table[1] = 1
    for k in range(2, n + 1):           # table[k - 1] and table[k - 2] are ready
        table[k] = table[k - 1] + table[k - 2]
    return table


def fib_two(n):
    """The same, keeping only the last two values."""
    before, current = 0, 1
    for _ in range(n):
        before, current = current, before + current
    return before


if __name__ == "__main__":
    print(fib_table(12))
    print(fib_table(90)[90], fib_two(90))
    print("fib(1000) has", len(str(fib_two(1000))), "digits")
