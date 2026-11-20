"""The PNG writer of figures/ppm2png.py, decoded back by a reader written here, and
the book's PNG images checked against the PPM files the C programs wrote."""

import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "figures"))

import ppm2png  # noqa: E402

IMAGES = HERE.parents[2] / "images" / "book5"


def decode(data):
    """(width, height, RGB bytes) of a PNG made of IHDR, IDAT chunks and IEND,
    colour type 2, filter 0 on every row; checks every CRC."""
    assert data[:8] == ppm2png.SIGNATURE
    pos, idat, size = 8, b"", None
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        kind, body = data[pos + 4 : pos + 8], data[pos + 8 : pos + 8 + length]
        (crc,) = struct.unpack(">I", data[pos + 8 + length : pos + 12 + length])
        assert crc == zlib.crc32(kind + body)
        if kind == b"IHDR":
            size = struct.unpack(">IIBBBBB", body)
            assert size[2:] == (8, 2, 0, 0, 0)
        elif kind == b"IDAT":
            idat += body
        pos += 12 + length
    w, h = size[0], size[1]
    raw = zlib.decompress(idat)
    rows = [raw[y * (3 * w + 1) : (y + 1) * (3 * w + 1)] for y in range(h)]
    assert all(row[0] == 0 for row in rows)
    return w, h, b"".join(row[1:] for row in rows)


def test_two_by_two():
    pixels = bytes([255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255])
    ppm = b"P6\n2 2\n255\n" + pixels
    data = ppm2png.png(*ppm2png.read_ppm(ppm))
    assert decode(data) == (2, 2, pixels)
    assert data[12:16] == b"IHDR" and data[-8:-4] == b"IEND"


def test_book_images_match_the_programs():
    names = sorted(p.stem for p in (HERE / "figures").glob("*.ppm"))
    assert names == ["raytrace", "reflect", "shade", "zbuffer"]
    for name in names:
        ppm = ppm2png.read_ppm((HERE / "figures" / f"{name}.ppm").read_bytes())
        assert decode((IMAGES / f"b3-31-{name}.png").read_bytes()) == ppm
