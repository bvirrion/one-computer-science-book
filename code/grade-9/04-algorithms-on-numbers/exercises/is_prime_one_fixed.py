def is_prime(n):
    if n < 2:                  # 0 and 1 are not prime
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 1
    return True
