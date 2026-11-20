DIGITS = "0123456789ABCDEF"


def to_hex(bits):
    """Hexadecimal digits of a string of bits whose length is a multiple of 4."""
    result = ""
    for i in range(0, len(bits), 4):
        group = bits[i:i + 4]
        result = result + DIGITS[int(group, 2)]
    return result


for bits in ["10101000", "11111111", "0010110000001111"]:
    print(bits, "->", to_hex(bits))
