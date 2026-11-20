from full_adder import full_adder


def to_bits(x, n):
    """The n bits of x, least significant first."""
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits):
    return sum(bit << i for i, bit in enumerate(bits))


def add_bits(a, b, carry=0):
    """Ripple-carry addition: one full adder per column, the carry passed along."""
    out = []
    carries = [carry]
    for x, y in zip(a, b):
        s, carry = full_adder(x, y, carry)
        out.append(s)
        carries.append(carry)
    return out, carries


if __name__ == "__main__":
    for x, y in [(100, 27), (200, 100), (100, 100)]:
        bits, carries = add_bits(to_bits(x, 8), to_bits(y, 8))
        result = from_bits(bits)
        overflow = carries[7] != carries[8]   # carry into bit 7 differs from carry out
        print(f"{x:3} + {y:3} = {result:3}  carry out {carries[8]}"
              f"  signed overflow {int(overflow)}  carries {carries[::-1]}")
