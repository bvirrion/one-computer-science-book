"""exo_ties.py: exercise 6, an encoder and a decoder that break ties differently."""

import heapq
from itertools import count


def tree(freq, tie):
    """Huffman's merges; `tie` orders trees of equal weight."""
    order = count()
    heap = [(f, tie(s), next(order), s) for s, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, _, t1 = heapq.heappop(heap)
        f2, _, _, t2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, 0, next(order), (t1, t2)))
    return heap[0][3]


def code(t, prefix=""):
    if isinstance(t, str):
        return {t: prefix}
    return code(t[0], prefix + "0") | code(t[1], prefix + "1")


def decode(bits, t):
    out, node = "", t
    for b in bits:
        node = node[int(b)]
        if isinstance(node, str):
            out, node = out + node, t
    return out


if __name__ == "__main__":
    freq = {"a": 2, "b": 2, "c": 2, "d": 2}
    sender = tree(freq, tie=lambda s: s)  # equal weights: alphabetical order
    receiver = tree(freq, tie=lambda s: -ord(s))  # equal weights: reverse order
    bits = "".join(code(sender)[ch] for ch in "bad")
    print("sender's code:  ", code(sender))
    print("receiver's code:", code(receiver))
    print(f"'bad' sent as {bits}, received as {decode(bits, receiver)!r}")
