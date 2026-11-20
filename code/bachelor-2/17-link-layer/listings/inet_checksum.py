"""inet_checksum.py: the Internet checksum, a one's complement sum of 16-bit words."""


def ones_sum(data):
    if len(data) % 2:
        data += b"\0"
    total = 0
    for i in range(0, len(data), 2):
        total += data[i] << 8 | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)   # add the carry back at the bottom
    return total


def checksum(data):
    return ~ones_sum(data) & 0xFFFF


if __name__ == "__main__":
    data = b"LAMP ON AT 20:00"
    c = checksum(data)
    print(f"checksum: {c:04x}")
    print(f"receiver's sum with it: {ones_sum(data + c.to_bytes(2, 'big')):04x}")
    swapped = data[2:4] + data[0:2] + data[4:]
    print(f"two words swapped:      {ones_sum(swapped + c.to_bytes(2, 'big')):04x}")
    flipped = bytes([data[0] ^ 1]) + data[1:]
    print(f"one bit flipped:        {ones_sum(flipped + c.to_bytes(2, 'big')):04x}")
