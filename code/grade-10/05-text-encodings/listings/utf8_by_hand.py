def utf8_encode(cp):
    """Return the UTF-8 bytes of the code point cp, 0 <= cp <= 0x10FFFF."""
    if cp < 0x80:
        return bytes([cp])
    if cp < 0x800:
        return bytes([0b110_00000 | cp >> 6, 0b10_000000 | cp & 0x3F])
    if cp < 0x10000:
        return bytes([0b1110_0000 | cp >> 12,
                      0b10_000000 | (cp >> 6) & 0x3F,
                      0b10_000000 | cp & 0x3F])
    return bytes([0b11110_000 | cp >> 18,
                  0b10_000000 | (cp >> 12) & 0x3F,
                  0b10_000000 | (cp >> 6) & 0x3F,
                  0b10_000000 | cp & 0x3F])


for cp in (0x41, 0xE9, 0x20AC, 0x1F600):
    mine = utf8_encode(cp)
    print(f"U+{cp:04X}  {mine.hex(' '):12}  same as Python: {mine == chr(cp).encode()}")
