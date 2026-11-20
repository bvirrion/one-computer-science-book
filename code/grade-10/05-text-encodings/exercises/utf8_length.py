"""Exercise 7: how many bytes UTF-8 uses for a code point."""


def utf8_length(cp):
    """Return 1, 2, 3 or 4, the number of UTF-8 bytes of the code point cp."""
    if cp < 0x80:
        return 1
    if cp < 0x800:
        return 2
    if cp < 0x10000:
        return 3
    return 4
