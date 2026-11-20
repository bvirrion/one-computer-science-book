"""dns_message.py: DNS messages in the wire format, with name compression."""
import ipaddress
import struct

TYPES = {"A": 1, "NS": 2, "CNAME": 5, "MX": 15, "TXT": 16, "AAAA": 28}
NAMES = {v: k for k, v in TYPES.items()}
IN = 1                                           # the Internet class


def encode_name(name, out, table):
    """Append name to out, ending with a pointer to a suffix already written."""
    labels = name.rstrip(".").split(".") if name.strip(".") else []
    for i in range(len(labels)):
        suffix = ".".join(labels[i:]).lower()
        if suffix in table:                      # written before: point to it
            out += struct.pack(">H", 0xC000 | table[suffix])
            return
        if len(out) < 0x4000:                    # a pointer holds 14 bits
            table[suffix] = len(out)
        label = labels[i].encode()
        assert 0 < len(label) <= 63, "a label has 1 to 63 bytes"
        out += bytes([len(label)]) + label
    out += b"\0"                                 # the root: an empty label


def read_name(buf, pos):
    """Return (name, position after it); pointers must point backwards."""
    labels, end, start = [], None, pos
    while True:
        n = buf[pos]
        if n >= 0xC0:                            # 11xxxxxx: a pointer
            target = struct.unpack_from(">H", buf, pos)[0] & 0x3FFF
            if target >= start:
                raise ValueError(f"pointer at {pos} to {target}, not before {start}")
            end = pos + 2 if end is None else end
            pos = start = target
        elif n == 0:
            return ".".join(labels), (pos + 1 if end is None else end)
        else:
            labels.append(buf[pos + 1:pos + 1 + n].decode())
            pos += 1 + n


def encode_rdata(rtype, data, out, table):
    start = len(out)
    out += b"\0\0"                               # length, filled in below
    if rtype == "A":
        out += ipaddress.IPv4Address(data).packed
    elif rtype == "AAAA":
        out += ipaddress.IPv6Address(data).packed
    elif rtype in ("NS", "CNAME"):
        encode_name(data, out, table)
    elif rtype == "MX":
        out += struct.pack(">H", data[0])
        encode_name(data[1], out, table)
    elif rtype == "TXT":
        out += bytes([len(data.encode())]) + data.encode()
    struct.pack_into(">H", out, start, len(out) - start - 2)


def decode_rdata(rtype, buf, pos, length):
    if rtype == "A":
        return str(ipaddress.IPv4Address(buf[pos:pos + 4]))
    if rtype == "AAAA":
        return str(ipaddress.IPv6Address(buf[pos:pos + 16]))
    if rtype in ("NS", "CNAME"):
        return read_name(buf, pos)[0]
    if rtype == "MX":
        return struct.unpack_from(">H", buf, pos)[0], read_name(buf, pos + 2)[0]
    if rtype == "TXT":
        return buf[pos + 1:pos + 1 + buf[pos]].decode()
    return buf[pos:pos + length]


def encode(msg, compress=True):
    """msg: dict with id, flags, question [(name, type)], and lists of records
    (name, type, ttl, data) under answer, authority, additional."""
    sections = ("answer", "authority", "additional")
    out = bytearray(struct.pack(">6H", msg["id"], msg["flags"], len(msg["question"]),
                                *(len(msg.get(s, [])) for s in sections)))
    table = {}
    for name, rtype in msg["question"]:
        encode_name(name, out, table if compress else {})
        out += struct.pack(">HH", TYPES[rtype], IN)
    for s in sections:
        for name, rtype, ttl, data in msg.get(s, []):
            encode_name(name, out, table if compress else {})
            out += struct.pack(">HHI", TYPES[rtype], IN, ttl)
            encode_rdata(rtype, data, out, table if compress else {})
    return bytes(out)


def decode(buf):
    ident, flags, qd, an, ns, ar = struct.unpack_from(">6H", buf, 0)
    msg, pos = {"id": ident, "flags": flags, "question": []}, 12
    for _ in range(qd):
        name, pos = read_name(buf, pos)
        rtype = struct.unpack_from(">H", buf, pos)[0]
        msg["question"].append((name, NAMES.get(rtype, rtype)))
        pos += 4
    for s, count in (("answer", an), ("authority", ns), ("additional", ar)):
        msg[s] = []
        for _ in range(count):
            name, pos = read_name(buf, pos)
            rtype, _, ttl, length = struct.unpack_from(">HHIH", buf, pos)
            rtype = NAMES.get(rtype, rtype)
            data = decode_rdata(rtype, buf, pos + 10, length)
            msg[s].append((name, rtype, ttl, data))
            pos += 10 + length
    return msg


QR, AA, RD, RA = 0x8000, 0x0400, 0x0100, 0x0080  # flag bits; rcode is the low 4


def query(ident, name, rtype, recurse=False):
    return encode({"id": ident, "flags": RD if recurse else 0,
                   "question": [(name, rtype)]})


if __name__ == "__main__":
    q = query(0x2a17, "www.brenmoor.test", "A")
    print(f"query of {len(q)} bytes")
    print("  header:  ", q[:12].hex(" "))
    print("  question:", q[12:].hex(" "))
    answer = {"id": 0x2a17, "flags": QR | AA, "question": [("www.brenmoor.test", "A")],
              "answer": [("www.brenmoor.test", "A", 3600, "127.0.0.1")],
              "authority": [("brenmoor.test", "NS", 86400, "ns.brenmoor.test")],
              "additional": [("ns.brenmoor.test", "A", 86400, "203.0.113.53")]}
    r = encode(answer)
    print("response:", len(r), "bytes; without compression:",
          len(encode(answer, compress=False)), "bytes")
    for section in ("answer", "authority", "additional"):
        for record in decode(r)[section]:
            print(f"  {section:10}", *record)
