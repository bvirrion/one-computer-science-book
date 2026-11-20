def divisor_sum(n):
    """The sum of the divisors of n that are smaller than n."""
    total = 0
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            total = total + d
    return total


for n in range(2, 1000):
    if divisor_sum(n) == n:
        print(n)
