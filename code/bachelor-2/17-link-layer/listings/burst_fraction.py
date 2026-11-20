"""burst_fraction.py: bursts reduced to their pattern B; how many does CRC-16 miss?"""
from crc import remainder

g = 0x11021                                    # x^16 + x^12 + x^5 + 1
for length in (2, 16, 17, 18):
    patterns = [1 | m << 1 | 1 << (length - 1) for m in range(1 << (length - 2))]
    missed = sum(remainder(b, length, g) == 0 for b in patterns)
    print(f"length {length:2}: {len(patterns):6} patterns, {missed} divisible by g")
