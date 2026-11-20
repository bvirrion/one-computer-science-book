"""ipv4_header.py: an IPv4 header built field by field, checked, then forwarded."""
from cidr import dotted, parse


def ones_sum(data):
    total = 0
    for i in range(0, len(data), 2):
        total += data[i] << 8 | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)
    return total


def header(src, dst, payload_len, ttl=64, proto=17, ident=1, df=True):
    h = bytearray(20)
    h[0] = 4 << 4 | 5                          # version 4, header of 5 words of 32 bits
    h[2:4] = (20 + payload_len).to_bytes(2, "big")         # total length
    h[4:6] = ident.to_bytes(2, "big")
    h[6:8] = ((1 << 14) if df else 0).to_bytes(2, "big")   # flags and fragment offset
    h[8], h[9] = ttl, proto                    # protocol 17: UDP
    h[12:16] = parse(src)[0].to_bytes(4, "big")
    h[16:20] = parse(dst)[0].to_bytes(4, "big")
    h[10:12] = (~ones_sum(h) & 0xFFFF).to_bytes(2, "big")  # field still 0 here
    return bytes(h)


def forward(h):
    """What a router does: check, take one off the time to live, fix the checksum."""
    assert ones_sum(h) == 0xFFFF, "damaged header: drop it"
    h = bytearray(h)
    h[8] -= 1
    h[10:12] = b"\0\0"
    h[10:12] = (~ones_sum(h) & 0xFFFF).to_bytes(2, "big")
    return bytes(h)


if __name__ == "__main__":
    h = header("198.51.100.3", "203.0.113.10", payload_len=12)
    print("header:", h.hex(" "))
    total = int.from_bytes(h[2:4])
    print(f"version {h[0] >> 4}, length {h[0] & 15} words, total {total} bytes,"
          f" ttl {h[8]}, protocol {h[9]}, checksum {h[10:12].hex()}")
    src, dst = int.from_bytes(h[12:16]), int.from_bytes(h[16:20])
    print("from", dotted(src), "to", dotted(dst))
    h2 = forward(h)
    print(f"after one router: ttl {h2[8]}, checksum {h2[10:12].hex()}, "
          f"sum {ones_sum(h2):04x}")
