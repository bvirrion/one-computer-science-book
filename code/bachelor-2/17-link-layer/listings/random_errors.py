"""random_errors.py: random error patterns on a 48-bit frame; how many pass CRC-16?"""
import random

from crc import crc16_table

random.seed(17)
trials = 1 << 24
passed = {0: 0, 1: 0}                         # by the parity of the number of flips
for _ in range(trials):
    e = random.getrandbits(48)
    if e and crc16_table(e.to_bytes(6, "big")) == 0:
        passed[e.bit_count() % 2] += 1
print(f"random error patterns: {trials}")
print(f"undetected: {passed[0] + passed[1]}, expected about {trials / 2**16:.0f}")
print(f"  with an even number of flips: {passed[0]}; with an odd number: {passed[1]}")
