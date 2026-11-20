from gates import NOT
from ripple import add_bits, from_bits, to_bits


def sub_bits(a, b):
    """a - b with the same adder: a + (b with every bit flipped) + 1."""
    return add_bits(a, [NOT(bit) for bit in b], carry=1)


for x, y in [(100, 27), (27, 100), (5, 5)]:
    bits, carries = sub_bits(to_bits(x, 8), to_bits(y, 8))
    r = from_bits(bits)
    signed = r - 256 if bits[7] else r
    print(f"{x:3} - {y:3} -> {r:3} (as a signed byte {signed:4})"
          f"  carry out {carries[8]}")
