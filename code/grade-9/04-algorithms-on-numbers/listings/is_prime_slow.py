def is_prime_slow(n):
    """True when n is prime; also the number of divisions tried."""
    divisions = 0
    for d in range(2, n):
        divisions = divisions + 1
        if n % d == 0:
            return False, divisions
    return n >= 2, divisions


for n in [91, 97, 1_000_003]:
    print(n, is_prime_slow(n))
