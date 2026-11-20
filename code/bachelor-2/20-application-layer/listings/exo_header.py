"""exo_header.py: the twelve bytes of a DNS header, field by field (exercise 1)."""
import struct

header = bytes.fromhex("2a 17 85 83 00 01 00 00 00 00 00 00")
ident, flags, qd, an, ns, ar = struct.unpack(">6H", header)
print(f"id {ident:#06x}")
for name, shift, width in (("QR", 15, 1), ("opcode", 11, 4), ("AA", 10, 1),
                           ("TC", 9, 1),
                           ("RD", 8, 1), ("RA", 7, 1), ("Z", 4, 3), ("RCODE", 0, 4)):
    print(f"{name:7}{(flags >> shift) & ((1 << width) - 1)}")
print(f"counts: {qd} question, {an} answers, {ns} authority, {ar} additional")
