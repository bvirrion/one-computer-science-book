"""CRCs: division, bitwise, table and zlib agree; bursts; CRC-8; the C program."""
import random
import zlib
from pathlib import Path

import burst_check
import crc
import crc8

OUT = Path(__file__).resolve().parent.parent / "outputs"


def test_crc32_three_ways():
    rng = random.Random(3)
    for n in [0, 1, 2, 3, 7, 64, 1000]:
        data = bytes(rng.randrange(256) for _ in range(n))
        assert crc.crc32_bitwise(data) == crc.crc32_table(data) == zlib.crc32(data)


def test_crc16_is_division():
    rng = random.Random(4)
    for n in range(1, 12):
        data = bytes(rng.randrange(256) for _ in range(n))
        m = int.from_bytes(data, "big")
        assert crc.crc16(data) == crc.crc16_table(data) == crc.remainder(m, 8 * n, 0x11021)


def test_codeword_divisible():
    for msg in [b"x", b"LAMP", b"LAMP ON AT 20:00"]:
        word = msg + crc.crc16(msg).to_bytes(2, "big")
        assert crc.crc16(word) == 0


def test_exercise_4_by_hand():
    # 1101 0011 with g = x^3 + x + 1: remainder 011 (solution of exercise 4)
    assert crc.remainder(0b11010011, 8, 0b1011) == 0b011


def test_bursts_and_sizes():
    lengths = list(range(1, 17))
    assert sum(sum(1 for _ in burst_check.bursts(b)) for b in lengths) == 1114111
    text = (OUT / "burst_check.txt").read_text()
    assert "1114111 tried, 0 undetected" in text
    assert " 17   1048576    32" in text            # 32 positions, one pattern each


def test_crc8_exercise():
    rng = random.Random(5)
    for n in range(0, 40):
        data = bytes(rng.randrange(256) for _ in range(n))
        assert crc8.crc8_bitwise(data) == crc8.crc8_table(data)
        m = int.from_bytes(data, "big") if data else 0
        assert crc8.crc8_bitwise(data) == crc.remainder(m, 8 * n, 0x107)


def test_c_matches_zlib():
    for line in (OUT / "crc32.txt").read_text().splitlines()[1:]:
        value, text = line.split("  ")
        assert int(value, 16) == zlib.crc32(text.strip('"').encode())
