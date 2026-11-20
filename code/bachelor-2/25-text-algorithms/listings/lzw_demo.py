"""lzw_demo.py: LZW on two short texts, with the entries added to the dictionary."""
from lzw import decode, encode


def word(w):
    return w.decode().replace(" ", "_")


for text in [b"banana bandana", b"abababa"]:
    log = []
    codes = encode(text, log)
    print(f"{word(text)}: {len(text)} bytes -> {len(codes)} codes:",
          " ".join(word(bytes([c])) if c < 256 else str(c) for c in codes))
    print("   new entries:", ", ".join(f"{code}={word(w)}" for code, w in log))
    print("   decoded back:", decode(codes) == text)
