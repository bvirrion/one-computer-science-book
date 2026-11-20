"""ecb_pattern.py -- a generated 96 x 64 picture, one byte per pixel, encrypted with
AES in ECB and in CBC mode. Writes the three pictures as a grid for the figure and
counts the blocks that repeat."""

import random
from pathlib import Path

from modes import cbc_encrypt, ecb_encrypt

W, H = 96, 64


def picture():
    """White background, a black ring and a grey bar: no logo, only shapes."""
    img = bytearray()
    for y in range(H):
        for x in range(W):
            r2 = (x - 30) ** 2 + (y - 32) ** 2
            if 14**2 <= r2 <= 24**2:
                img.append(0)
            elif 58 <= x <= 86 and 14 <= y <= 50:
                img.append(128)
            else:
                img.append(255)
    return bytes(img)


rng = random.Random(27)
key, iv = rng.randbytes(16), rng.randbytes(16)
plain = picture()
ecb, cbc = ecb_encrypt(key, plain), cbc_encrypt(key, iv, plain)
out = Path(__file__).resolve().parents[1] / "figures" / "ecb.dat"
out.parent.mkdir(exist_ok=True)
with open(out, "w") as f:
    f.write("x y plain ecb cbc\n")
    for y in range(H):
        for x in range(W):
            i = y * W + x
            f.write(f"{x} {H - 1 - y} {plain[i]} {ecb[i]} {cbc[i]}\n")
for name, data in (("plain", plain), ("ECB", ecb), ("CBC", cbc)):
    bl = [data[i : i + 16] for i in range(0, len(data), 16)]
    print(f"{name:<5} {len(bl)} blocks, {len(set(bl))} different")
