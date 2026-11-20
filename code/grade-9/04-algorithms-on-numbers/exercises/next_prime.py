def next_prime(n):
    """The smallest prime above n, and the divisions tried to find it."""
    divisions = 0
    candidate = n + 1
    while True:
        if candidate >= 2:
            d = 2
            prime = True
            while d * d <= candidate:
                divisions = divisions + 1
                if candidate % d == 0:
                    prime = False
                    break
                d = d + 1
            if prime:
                return candidate, divisions
        candidate = candidate + 1


if __name__ == "__main__":
    n = int(input("A whole number: "))
    print(next_prime(n))
