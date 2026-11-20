"""Exercise 12: decode UTF-8 by hand, with bit operations."""


def utf8_decode(data):
    """Return the list of code points of the valid UTF-8 bytes data."""
    points = []
    i = 0
    while i < len(data):
        b = data[i]
        if b < 0x80:
            n, cp = 1, b
        elif b >> 5 == 0b110:
            n, cp = 2, b & 0x1F
        elif b >> 4 == 0b1110:
            n, cp = 3, b & 0x0F
        else:
            n, cp = 4, b & 0x07
        for k in range(1, n):
            cp = cp << 6 | data[i + k] & 0x3F
        points.append(cp)
        i += n
    return points
