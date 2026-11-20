def divisors(n):
    """The divisors of n, from 1 to n."""
    found = []
    for d in range(1, n + 1):
        if n % d == 0:
            found.append(d)
    return found


print(divisors(36))
print(divisors(37))
