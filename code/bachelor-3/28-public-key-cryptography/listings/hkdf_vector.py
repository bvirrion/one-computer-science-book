"""hkdf_vector.py -- test case 1 of RFC 5869, with the HKDF of exercise 12."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from ex12_hkdf import expand, extract  # noqa: E402

prk = extract(bytes(range(13)), bytes([0x0B]) * 22)
okm = expand(prk, bytes(range(0xF0, 0xFA)), 42)
print("PRK", prk.hex())
print("OKM", okm.hex())
print(
    "as in RFC 5869:",
    okm.hex() == "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c"
    "5db02d56ecc4c5bf34007208d5b887185865",
)
