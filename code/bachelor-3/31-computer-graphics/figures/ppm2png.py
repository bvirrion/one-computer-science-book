"""Convert the chapter's PPM images to PNG with nothing but zlib, for the book.

Usage: python ppm2png.py  (from any directory) converts figures/*.ppm to
images/book5/b3-31-<name>.png. A PNG is an 8-byte signature and chunks, each a
4-byte length, a 4-byte type, the data and a CRC-32 of type and data: IHDR (size,
bit depth 8, colour type 2 = RGB), IDAT (the rows, each led by a filter byte,
compressed with zlib) and IEND."""

import struct
import zlib
from pathlib import Path

SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_ppm(data):
    """(width, height, pixel bytes) of a binary P6 file with maxval 255."""
    fields, pos = [], 0
    while len(fields) < 4:
        while data[pos : pos + 1].isspace():
            pos += 1
        start = pos
        while not data[pos : pos + 1].isspace():
            pos += 1
        fields.append(data[start:pos])
    if fields[0] != b"P6" or fields[3] != b"255":
        raise ValueError("not a P6 file with maxval 255")
    w, h = int(fields[1]), int(fields[2])
    pixels = data[pos + 1 : pos + 1 + 3 * w * h]
    if len(pixels) != 3 * w * h:
        raise ValueError("truncated PPM")
    return w, h, pixels


def chunk(kind, body):
    crc = zlib.crc32(kind + body)
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", crc)


def png(w, h, pixels):
    rows = b"".join(b"\0" + pixels[3 * w * y : 3 * w * (y + 1)] for y in range(h))
    header = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (
        SIGNATURE
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    out = here.parents[3] / "images" / "book5"
    for ppm in sorted(here.glob("*.ppm")):
        target = out / f"b3-31-{ppm.stem}.png"
        target.write_bytes(png(*read_ppm(ppm.read_bytes())))
        print(target.relative_to(here.parents[3]))
