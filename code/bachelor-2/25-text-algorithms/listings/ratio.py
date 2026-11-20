"""ratio.py: the town archive compressed: Huffman on bytes, LZW with growing code
widths, and zlib for reference."""
import heapq
import zlib
from collections import Counter

from lzw import decode, encode
from text_gen import archive


def huffman_bits(data):
    """The size in bits of the Huffman coding of data, byte by byte, table apart."""
    heap = list(Counter(data).values())
    heapq.heapify(heap)
    bits = 0
    while len(heap) > 1:  # each merge adds one bit to every byte below it
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        bits += a + b
        heapq.heappush(heap, a + b)
    return bits


def lzw_bits(codes):
    """The k-th code is written on as many bits as the largest code then, 255 + k."""
    return sum((255 + k).bit_length() for k in range(len(codes)))


data = archive().encode()
codes = encode(data)
assert decode(codes) == data
print(f"archive: {len(data)} bytes, {len(set(data))} distinct")
for name, bits in [("Huffman", huffman_bits(data)), ("LZW", lzw_bits(codes)),
                   ("zlib -9", 8 * len(zlib.compress(data, 9)))]:
    print(f"{name:8} {bits // 8:6} bytes   ratio {8 * len(data) / bits:4.2f}")
print(f"LZW: {len(codes)} codes, {len(data) / len(codes):.1f} bytes a code")
