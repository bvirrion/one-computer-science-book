def encode(x, n):
    """Return the n-bit two's complement pattern of x as an unsigned number.

    Precondition: -2**(n-1) <= x < 2**(n-1).
    """
    return x % 2**n


def decode(u, n):
    """Return the signed value of the n-bit pattern u, 0 <= u < 2**n."""
    if u >= 2 ** (n - 1):
        return u - 2**n
    return u


for u in range(16):
    print(f"{u:04b}  unsigned {u:2}  signed {decode(u, 4):3}")
print("encode(-3, 8) =", format(encode(-3, 8), "08b"))
