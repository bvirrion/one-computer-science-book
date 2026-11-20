"""lzw.py: Lempel-Ziv-Welch coding; the dictionary starts with the 256 bytes."""


def encode(data, log=None):
    """A list of codes: each one is the longest word of the dictionary that starts here;
    that word plus the next byte becomes a new entry (appended to log if given)."""
    table = {bytes([b]): b for b in range(256)}
    codes, w = [], b""
    for b in data:
        wb = w + bytes([b])
        if wb in table:
            w = wb
        else:
            codes.append(table[w])
            table[wb] = len(table)
            if log is not None:
                log.append((len(table) - 1, wb))
            w = bytes([b])
    if w:
        codes.append(table[w])
    return codes


def decode(codes):
    """Rebuild the encoder's dictionary one step late."""
    table = [bytes([b]) for b in range(256)]
    out, prev = [], None
    for code in codes:
        if code < len(table):
            word = table[code]
        elif code == len(table) and prev is not None:  # not yet in the table:
            word = prev + prev[:1]  # it can only be prev followed by its first byte
        else:
            raise ValueError(f"bad code {code}")
        out.append(word)
        if prev is not None:
            table.append(prev + word[:1])
        prev = word
    return b"".join(out)
