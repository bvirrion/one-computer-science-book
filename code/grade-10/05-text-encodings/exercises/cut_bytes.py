"""Exercise 11: cutting a UTF-8 text to at most n bytes without breaking a character."""


def cut_buggy(text, n):
    return text.encode("utf-8")[:n].decode("utf-8")


def char_length(first):
    """Number of bytes of the character whose first UTF-8 byte is `first`."""
    if first < 0x80:
        return 1
    if first >> 5 == 0b110:
        return 2
    if first >> 4 == 0b1110:
        return 3
    return 4


def cut(text, n):
    """Return the longest start of text whose UTF-8 encoding has at most n bytes."""
    data = text.encode("utf-8")[:n]
    j = len(data) - 1
    while j >= 0 and data[j] & 0b1100_0000 == 0b1000_0000:
        j -= 1  # walk back over continuation bytes to the last first byte
    if j >= 0 and j + char_length(data[j]) > len(data):
        data = data[:j]  # the last character was cut: drop it
    return data.decode("utf-8")
