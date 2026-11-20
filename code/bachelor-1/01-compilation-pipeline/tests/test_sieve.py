from b1load import load

sieve = load(__file__, "pysieve")


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


def test_sieve_matches_trial_division():
    for n in (0, 1, 2, 3, 10, 100, 1000, 5000):
        assert sieve.count_primes(n) == sum(is_prime(k) for k in range(n))


def test_known_count():
    assert sieve.count_primes(10**6) == 78498
