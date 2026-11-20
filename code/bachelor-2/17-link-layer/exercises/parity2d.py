"""parity2d.py: a parity grid that corrects any single flipped bit (exercise 3)."""


def parity(byte):
    return bin(byte).count("1") % 2


def encode(data):
    """The data, one parity bit per byte (rows), and one parity byte (columns)."""
    col = 0
    for b in data:
        col ^= b
    return bytes(data), [parity(b) for b in data], col


def correct(data, rows, col):
    """Return the data with at most one flipped data bit corrected, or None."""
    bad_rows = [i for i, b in enumerate(data) if parity(b) != rows[i]]
    now = 0
    for b in data:
        now ^= b
    diff = now ^ col                          # columns whose parity is wrong
    if not bad_rows and diff == 0:
        return bytes(data)
    if len(bad_rows) == 1 and diff and diff & (diff - 1) == 0:
        out = bytearray(data)
        out[bad_rows[0]] ^= diff              # the one bit at the crossing
        return bytes(out)
    if len(bad_rows) == 1 and diff == 0:      # the row's own parity bit flipped
        return bytes(data)
    if not bad_rows and diff & (diff - 1) == 0:   # one bit of the parity byte
        return bytes(data)
    return None                               # more than one flip: give up
