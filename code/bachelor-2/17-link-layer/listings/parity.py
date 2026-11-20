"""parity.py: one parity bit per byte, and a parity grid that locates a flip."""


def parity(byte):
    return bin(byte).count("1") % 2           # even parity: makes the count of 1s even


def checks(data):
    return [parity(b) for b in data]


def flip(data, i, bit):
    out = bytearray(data)
    out[i] ^= 1 << bit
    return bytes(out)


def column_parity(data):
    col = 0
    for b in data:
        col ^= b                              # bit k of col: parity of column k
    return col


data = b"LAMP"
sent = checks(data)
print("bytes:", data.hex(" "), " parity bits:", sent)
one = flip(data, 2, 3)
print("one flip in byte 2: ", checks(one), "-> byte 2 fails")
two = flip(one, 2, 6)
print("two flips in byte 2:", checks(two), "-> nothing seen")
assert checks(one) != sent and checks(two) == sent

row = [i for i in range(4) if checks(one)[i] != sent[i]]
col = (column_parity(one) ^ column_parity(data)).bit_length() - 1
print(f"grid: row {row[0]} and column {col} disagree: flip bit {col} of byte {row[0]}")
print("corrected:", flip(one, row[0], col) == data)
