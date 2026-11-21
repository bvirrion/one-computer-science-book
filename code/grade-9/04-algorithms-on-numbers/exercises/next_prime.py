from is_prime import is_prime


def next_prime(n):
    """The smallest prime above n, and the divisions tried to find it."""
    candidate = n + 1
    prime, divisions = is_prime(candidate)
    while not prime:
        candidate = candidate + 1
        prime, tried = is_prime(candidate)
        divisions = divisions + tried
    return candidate, divisions


if __name__ == "__main__":
    n = int(input("A whole number: "))
    print(next_prime(n))
