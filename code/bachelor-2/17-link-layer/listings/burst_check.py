"""burst_check.py: flip every burst of up to 17 bits in one frame; count what passes."""
from crc import crc16_table

msg = b"LAMP"
word = msg + crc16_table(msg).to_bytes(2, "big")   # the frame with its 16 check bits
n = 8 * len(word)
c = int.from_bytes(word, "big")
assert crc16_table(word) == 0                      # the receiver's test passes


def bursts(length):
    """Every error pattern whose first and last flipped bits are `length` apart."""
    inner = range(1 << max(length - 2, 0))
    for start in range(n - length + 1):
        for mid in inner:
            e = 1 | (mid << 1) | (1 << (length - 1)) if length > 1 else 1
            yield e << start


print(f"frame of {n} bits; burst length, bursts tried, bursts undetected")
total = total_missed = 0
for length in range(1, 18):
    tried = missed = 0
    for e in bursts(length):
        tried += 1
        missed += crc16_table((c ^ e).to_bytes(len(word), "big")) == 0
    if length <= 16:
        total, total_missed = total + tried, total_missed + missed
    if length in (1, 2, 8, 15, 16, 17):
        print(f"{length:3} {tried:9} {missed:5}")
print(f"all bursts of 1 to 16 bits: {total} tried, {total_missed} undetected")
