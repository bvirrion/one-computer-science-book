def is_prime(n):
    """True when n is prime; also the number of divisions tried."""
    if n < 2:
        return False, 0
    divisions = 0
    d = 2
    while d * d <= n:                  # stop at the square root of n
        divisions = divisions + 1
        if n % d == 0:
            return False, divisions
        d = d + 1
    return True, divisions


if __name__ == "__main__":
    for n in [91, 97, 1_000_003]:
        print(n, is_prime(n))
