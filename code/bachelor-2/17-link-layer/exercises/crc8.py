"""crc8.py: a CRC with g = x^8 + x^2 + x + 1, bit by bit and by table (exercise 7)."""
G = 0x07                                      # g without its x^8 term


def crc8_bitwise(data):
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc << 1) ^ G) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
    return crc


TABLE = [crc8_bitwise(bytes([b])) for b in range(256)]


def crc8_table(data):
    crc = 0
    for byte in data:
        crc = TABLE[crc ^ byte]               # the whole state is one byte
    return crc
