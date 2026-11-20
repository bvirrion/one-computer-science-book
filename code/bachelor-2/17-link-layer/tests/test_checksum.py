"""The Internet checksum (RFC 1071's worked example), parity and the parity grid."""
import itertools

import inet_checksum
import parity2d
import stuffing


def test_rfc1071_example():
    data = bytes.fromhex("0001f203f4f5f6f7")
    assert inet_checksum.ones_sum(data) == 0xDDF2
    assert inet_checksum.checksum(data) == 0x220D


def test_receiver_gets_ffff():
    for data in [b"LAMP", b"LAMP ON AT 20:00", b"\xff\xff\xff\xff", b"odd"]:
        c = inet_checksum.checksum(data)
        padded = data + b"\0" * (len(data) % 2)
        assert inet_checksum.ones_sum(padded + c.to_bytes(2, "big")) == 0xFFFF


def test_grid_corrects_every_single_flip():
    data = b"LAMP"
    _, rows, col = parity2d.encode(data)
    for i, bit in itertools.product(range(4), range(8)):
        bad = bytearray(data)
        bad[i] ^= 1 << bit
        assert parity2d.correct(bytes(bad), rows, col) == data
    for i in range(4):                               # a row parity bit flipped
        r = rows[:]
        r[i] ^= 1
        assert parity2d.correct(data, r, col) == data
    for bit in range(8):                             # a column parity bit flipped
        assert parity2d.correct(data, rows, col ^ 1 << bit) == data
    bad = bytearray(data)
    bad[0] ^= 1
    bad[1] ^= 2
    assert parity2d.correct(bytes(bad), rows, col) is None


def test_stuffing_round_trip():
    for payload in [b"", b"\x7e", b"\x7d\x7e\x7d", bytes(range(256))]:
        wire = stuffing.stuff(payload)
        assert 0x7E not in wire[1:-1]
        assert stuffing.unstuff(wire) == payload
