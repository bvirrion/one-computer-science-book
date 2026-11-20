"""exo_hdrsum.py: a checksum recomputed without clearing its field (ex. 6)."""
from ipv4_header import header, ones_sum

h = bytearray(header("198.51.100.3", "203.0.113.10", payload_len=12))
h[8] -= 1                                      # one hop: the time to live goes down
h[10:12] = (~ones_sum(h) & 0xFFFF).to_bytes(2, "big")    # old checksum summed too
print(f"checksum written {h[10:12].hex()}, receiver's sum {ones_sum(h):04x}")
