def sieve(n):
    """The prime numbers below n, by crossing out multiples."""
    prime = [True] * n
    prime[0] = False
    prime[1] = False
    for p in range(2, n):
        if prime[p]:
            for multiple in range(p * p, n, p):
                prime[multiple] = False
    primes = []
    for k in range(n):
        if prime[k]:
            primes.append(k)
    return primes


if __name__ == "__main__":
    print(sieve(50))
    print(len(sieve(100_000)), "primes below 100,000")
