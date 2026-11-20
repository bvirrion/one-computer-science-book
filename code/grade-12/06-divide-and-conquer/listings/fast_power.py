def power(x, n):
    """x to the power n, by squaring; returns (value, multiplications)."""
    if n == 0:
        return 1, 0
    if n == 1:
        return x, 0
    half, m = power(x, n // 2)          # one smaller problem, used twice
    if n % 2 == 0:
        return half * half, m + 1
    return half * half * x, m + 2


def power_loop(x, n):
    """The same, reading the binary digits of n from the right."""
    result, square = 1, x
    while n > 0:
        if n % 2 == 1:
            result *= square
        square *= square
        n //= 2
    return result


def power_mod(x, n, m):
    """x to the power n, modulo m: every intermediate value stays below m."""
    result, square = 1, x % m
    while n > 0:
        if n % 2 == 1:
            result = result * square % m
        square = square * square % m
        n //= 2
    return result


if __name__ == "__main__":
    for n in [10, 13, 64, 100, 1000]:
        value, m = power(3, n)
        print(f"3^{n:<4}: {m:2} multiplications instead of {n - 1:3};"
              f" same as the loop: {value == power_loop(3, n)}")
    print(power_mod(7, 10**18, 1_000_003), pow(7, 10**18, 1_000_003))
