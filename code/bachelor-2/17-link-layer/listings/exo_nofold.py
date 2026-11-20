"""exo_nofold.py: an Internet checksum that drops its carries (exercise 2)."""
from inet_checksum import checksum


def checksum_nofold(data):
    total = 0
    for i in range(0, len(data), 2):
        total += data[i] << 8 | data[i + 1]
    return ~total & 0xFFFF


for data in [b"LAMP", b"\xff\xf0\x00\x20"]:
    right, wrong = checksum(data), checksum_nofold(data)
    print(data.hex(" "), f" right {right:04x}  without folding {wrong:04x}")
