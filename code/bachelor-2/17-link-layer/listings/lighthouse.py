"""lighthouse.py: a frame crosses a noisy link and one bit flips. Who notices?"""
import zlib

frame = b"LAMP ON AT 20:00"
check = zlib.crc32(frame)                    # computed by the sender, sent along

received = bytearray(frame)
received[12] ^= 0b00000001                   # the noise flips the lowest bit of byte 12
received = bytes(received)

print("sent:     ", frame.decode(), f"  check {check:08x}")
print("received: ", received.decode(), f"  check {check:08x}")
print("recomputed check of what arrived:", f"{zlib.crc32(received):08x}")
print("frame accepted" if zlib.crc32(received) == check else "frame dropped")
