"""Exercise 7: a decoder that forgets the weight of the sign bit, and the fix."""


def decode_buggy(bits):
    """bits is a string of 0 and 1, the leftmost being the sign bit."""
    return int(bits, 2)


def decode(bits):
    n = len(bits)
    u = int(bits, 2)
    return u - 2**n if bits[0] == "1" else u
