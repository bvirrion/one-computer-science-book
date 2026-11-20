def to_binary(n):
    """The binary writing of a whole number n >= 0, by repeated division by 2."""
    if n == 0:
        return "0"
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n = n // 2
    return bits


print(to_binary(13), to_binary(0), to_binary(255))
