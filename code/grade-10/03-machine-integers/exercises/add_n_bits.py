"""Exercise 15: an n-bit adder with its carry and overflow flags."""


def add_n_bits(a, b, n):
    """a and b are n-bit patterns (0 <= a, b < 2**n).

    Return (result, carry, overflow): the n-bit result; whether the unsigned sum
    needed n + 1 bits; whether the signed sum is wrong (both operands of one sign,
    the result of the other).
    """
    total = a + b
    result = total % 2**n
    carry = total >= 2**n
    sign = 2 ** (n - 1)
    overflow = (a & sign) == (b & sign) and (result & sign) != (a & sign)
    return result, carry, overflow
