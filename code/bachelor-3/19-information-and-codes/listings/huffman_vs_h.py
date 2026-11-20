"""huffman_vs_h.py -- Huffman codes for the catalogue's letters, taken one, two and
three at a time, as a memoryless source with the catalogue's letter frequencies: the
length per letter against the entropy H."""
import heapq
import itertools
import math

from entropy import entropy, frequencies
from source import catalogue_text


def huffman_lengths(probabilities):
    """Codeword length of each symbol: merge the two least likely, again and again."""
    heap = [(p, i, [s]) for i, (s, p) in enumerate(probabilities.items())]
    heapq.heapify(heap)
    depth = dict.fromkeys(probabilities, 0)
    count = len(heap)
    while len(heap) > 1:
        p1, _, a = heapq.heappop(heap)
        p2, _, b = heapq.heappop(heap)
        for s in a + b:
            depth[s] += 1  # every symbol under the merged node gets one bit longer
        heapq.heappush(heap, (p1 + p2, count, a + b))
        count += 1
    return depth


def blocks(f, k):
    """The probabilities of blocks of k independent letters."""
    return {"".join(b): math.prod(f[c] for c in b)
            for b in itertools.product(f, repeat=k)}


if __name__ == "__main__":
    f = frequencies(catalogue_text())
    h = entropy(f.values())
    print(f"H = {h:.4f} bits per letter")
    print("block  symbols  Huffman bits per letter  excess over H  bound 1/k")
    for k in (1, 2, 3):
        p = blocks(f, k)
        lengths = huffman_lengths(p)
        per_letter = sum(p[s] * lengths[s] for s in p) / k
        print(f"{k:>5}  {len(p):>7,}  {per_letter:>23.4f}  {per_letter - h:>13.4f}"
              f"  {1 / k:>9.3f}")
