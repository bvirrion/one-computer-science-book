"""fragment.py: cut a datagram's payload to fit a link's MTU (ex. 9)."""


def fragment(payload_len, mtu, header=20):
    """(offset in 8-byte units, data bytes, more-fragments flag) for each fragment."""
    per = (mtu - header) // 8 * 8              # all but the last: a multiple of 8
    out, start = [], 0
    while start < payload_len:
        size = min(per, payload_len - start)
        out.append((start // 8, size, start + size < payload_len))
        start += size
    return out


if __name__ == "__main__":
    for payload, mtu in [(4000, 1500), (4000, 576)]:
        print(f"payload {payload} bytes, MTU {mtu}:")
        for off, size, more in fragment(payload, mtu):
            mf = int(more)
            print(f"  offset {off:3} (byte {8 * off:4})  {size:4} bytes  MF={mf}")
