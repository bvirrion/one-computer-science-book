"""exo_unstuff.py: a decoder that drops the escape byte and stops there (exercise 6)."""
from stuffing import stuff


def unstuff_wrong(frame):
    return bytes(b for b in frame[1:-1] if b != 0x7D)


payload = bytes([0x41, 0x7E, 0x42, 0x7D, 0x43])
print("sent:   ", payload.hex(" "))
print("decoded:", unstuff_wrong(stuff(payload)).hex(" "))
