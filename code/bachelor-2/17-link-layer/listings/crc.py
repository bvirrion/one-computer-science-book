"""crc.py: cyclic redundancy codes as division of 0/1 polynomials, then CRC-32."""
import zlib


def remainder(message, n, g):
    """Remainder of message(x) * x^r divided by g(x): message has n bits, g degree r."""
    r = g.bit_length() - 1
    value = message << r
    for i in range(n + r - 1, r - 1, -1):     # from the top bit down to bit r
        if value >> i & 1:
            value ^= g << (i - r)             # subtract g, written under bit i
    return value


def crc16(data):
    """CRC with x^16 + x^12 + x^5 + 1, most significant bit first, start 0."""
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = (crc << 1) ^ 0x11021 if crc & 0x8000 else crc << 1
    return crc


T16 = [crc16(bytes([b])) for b in range(256)]


def crc16_table(data):
    crc = 0
    for byte in data:
        crc = (crc << 8 & 0xFFFF) ^ T16[crc >> 8 ^ byte]
    return crc


def crc32_bitwise(data):
    """CRC-32 of zlib: bits taken lowest first, so the generator is reversed."""
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xEDB88320 if crc & 1 else crc >> 1
    return crc ^ 0xFFFFFFFF


def _step8(b):
    for _ in range(8):
        b = (b >> 1) ^ 0xEDB88320 if b & 1 else b >> 1
    return b


TABLE = [_step8(b) for b in range(256)]      # the eight steps of each byte value


def crc32_table(data):
    crc = 0xFFFFFFFF
    for byte in data:
        crc = TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


if __name__ == "__main__":
    print("0x04c11db7 reversed:", hex(int(f"{0x04C11DB7:032b}"[::-1], 2)))
    print(f"{'input':18} {'bitwise':>8} {'table':>8} {'zlib':>8}")
    for data in [b"", b"a", b"123456789", b"LAMP ON AT 20:00", bytes(range(256)) * 4]:
        label = data.decode() if len(data) < 20 else f"{len(data)} bytes"
        row = [crc32_bitwise(data), crc32_table(data), zlib.crc32(data)]
        print(f"{label!r:18}", " ".join(f"{v:08x}" for v in row))
    msg = b"LAMP"
    m = int.from_bytes(msg, "big")
    by_division = remainder(m, 32, 0x11021)
    print(f"crc16(LAMP) = {crc16(msg):04x}, by division: {by_division:04x}")
