"""crc_poly.py -- a CRC as polynomial division over GF(2). A bit string is a polynomial,
bit i the coefficient of x^i; subtraction is XOR. The generator x^8 + x^2 + x + 1 has
degree r = 8, so every burst of at most 8 bits is detected; longer ones are counted."""
G, R = 0b1_0000_0111, 8


def remainder(a, g=G):
    """a mod g over GF(2): cancel the leading term with a shifted g, until
    deg a < deg g."""
    while a.bit_length() >= g.bit_length():
        a ^= g << (a.bit_length() - g.bit_length())
    return a


def encode(message):
    """Append r check bits so that the codeword is a multiple of g."""
    shifted = message << R
    return shifted | remainder(shifted)


def bursts(length, width):
    """Every error pattern whose 1s span exactly `length` positions, inside `width`
    bits."""
    for inner in range(1 << max(length - 2, 0)):
        b = 1 if length == 1 else (1 << (length - 1)) | (inner << 1) | 1
        for shift in range(width - length + 1):
            yield b << shift


if __name__ == "__main__":
    m = int.from_bytes(b"Lib", "big")
    c = encode(m)
    print(f"message {m:024b}\ncodeword {c:032b}, remainder {remainder(c)}")
    print("burst length   patterns   undetected   fraction")
    for length in range(1, 13):
        patterns = list(bursts(length, 32))
        missed = sum(remainder(c ^ e) == 0 for e in patterns)
        fraction = missed / len(patterns)
        print(f"{length:>12}   {len(patterns):>8,}   {missed:>10}   {fraction:.5f}")
