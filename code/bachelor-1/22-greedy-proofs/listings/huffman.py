"""huffman.py: a Huffman code for the letters of the library's 80 titles."""

import csv
import heapq
from collections import Counter
from math import ceil, log2
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def catalogue():
    """The 80 titles in lower case, one per line."""
    with open(TOWN / "books.csv", newline="") as f:
        return "\n".join(row["title"].lower() for row in csv.DictReader(f))


def huffman_tree(freq):
    """Merge the two lightest trees until one is left. A leaf is a symbol, an inner
    node a pair (left, right). Ties go to the tree made first (symbols in order)."""
    heap = [(f, i, s) for i, (s, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    made = len(heap)
    while len(heap) > 1:
        f1, _, t1 = heapq.heappop(heap)
        f2, _, t2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, made, (t1, t2)))  # the lighter one on the left
        made += 1
    return heap[0][2]


def codewords(tree, prefix=""):
    """The codeword of each symbol: 0 for a left branch, 1 for a right one."""
    if isinstance(tree, str):
        return {tree: prefix or "0"}
    left, right = tree
    return codewords(left, prefix + "0") | codewords(right, prefix + "1")


def main():
    text = catalogue()
    freq = Counter(text)
    code = codewords(huffman_tree(freq))
    fixed = ceil(log2(len(freq)))
    print(f"{len(text)} characters, {len(freq)} symbols; fixed-length code:"
          f" {fixed} bits each, {fixed * len(text)} bits")
    by_freq = sorted(freq.items(), key=lambda x: -x[1])
    rows = [f"{s!r:5}{f:4} {code[s]:8}" for s, f in by_freq]
    for i in range(0, len(rows), 3):
        print(("  " + "   ".join(rows[i:i + 3])).rstrip())
    bits = sum(freq[s] * len(code[s]) for s in freq)
    print(f"Huffman code: {bits} bits, {bits / len(text):.3f} bits per character")


if __name__ == "__main__":
    main()
