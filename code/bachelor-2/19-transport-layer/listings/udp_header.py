"""udp_header.py: UDP's 8 bytes: two ports, a length, a checksum."""
import struct

msg = b"who 7"
header = struct.pack("!HHHH", 44191, 44190, 8 + len(msg), 0)   # checksum filled later
print("header:", header.hex(" "), " message:", msg.hex(" "))
src, dst, length, _ = struct.unpack("!HHHH", header)
print(f"source port {src}, destination port {dst}, length {length} = 8 + {len(msg)}")
