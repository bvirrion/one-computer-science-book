"""min_nand.py: the smallest circuits of two-input NAND gates that compute a half adder,
by trying every circuit of k gates for k = 1, 2, ..."""

from itertools import combinations_with_replacement

A, B = 0b0011, 0b0101  # truth tables on the four rows (a, b) = 00, 01, 10, 11
TARGETS = {"sum": A ^ B, "carry": A & B}


def search(k):
    """(number of circuits tried, first circuit found or None). A circuit is a list of
    gates, each a pair of earlier signals; a signal is a 4-bit truth table."""
    tried, found = 0, None

    def extend(signals, gates):
        nonlocal tried, found
        if len(gates) == k:
            tried += 1
            if found is None and set(TARGETS.values()) <= set(signals[2:]):
                found = list(gates)
            return
        for i, j in combinations_with_replacement(range(len(signals)), 2):
            out = ~(signals[i] & signals[j]) & 0b1111  # NAND on all four rows at once
            extend(signals + [out], gates + [(i, j)])

    extend([A, B], [])
    return tried, found


if __name__ == "__main__":
    for k in range(1, 6):
        tried, found = search(k)
        print(f"gates {k}: {tried:6} circuits, half adder: {found or 'none'}")
