"""exo_lzw.py: LZW on she_sells_sea_shells."""
from lzw import encode

text = b"she sells sea shells"
log = []
codes = encode(text, log)
print(" ".join(chr(c).replace(" ", "_") if c < 256 else str(c) for c in codes))
print(", ".join(f"{code}={w.decode().replace(' ', '_')}" for code, w in log))
