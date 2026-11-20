"""stuffing.py: frames delimited by a flag byte, with byte stuffing."""
FLAG, ESC = 0x7E, 0x7D


def stuff(payload):
    out = bytearray([FLAG])
    for b in payload:
        if b in (FLAG, ESC):
            out += bytes([ESC, b ^ 0x20])     # never a flag inside the frame
        else:
            out.append(b)
    out.append(FLAG)
    return bytes(out)


def unstuff(frame):
    assert frame[0] == FLAG and frame[-1] == FLAG
    out, escaped = bytearray(), False
    for b in frame[1:-1]:
        if escaped:
            out.append(b ^ 0x20)
            escaped = False
        elif b == ESC:
            escaped = True
        else:
            out.append(b)
    return bytes(out)


def frames(stream):
    """Cut a stream of bytes into the payloads of its frames."""
    parts = stream.split(bytes([FLAG]))
    return [unstuff(bytes([FLAG]) + p + bytes([FLAG])) for p in parts if p]


if __name__ == "__main__":
    payload = bytes([0x41, 0x7E, 0x42, 0x7D, 0x43])
    wire = stuff(payload) + stuff(b"OK")
    print("payload:", payload.hex(" "))
    print("on the wire:", wire.hex(" "))
    print("frames found:", [p.hex(" ") for p in frames(wire)])
