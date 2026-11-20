"""seven_segment.py: the decoder from a decimal digit, in four bits abcd, to the seven
segments of a display; the codes 10 to 15 never occur, so they are don't-cares."""

from karnaugh import as_product, covers, essential, prime_implicants

SEGMENTS = {  # segment: the digits that light it
    "a": [0, 2, 3, 5, 6, 7, 8, 9], "b": [0, 1, 2, 3, 4, 7, 8, 9],
    "c": [0, 1, 3, 4, 5, 6, 7, 8, 9], "d": [0, 2, 3, 5, 6, 8, 9],
    "e": [0, 2, 6, 8], "f": [0, 4, 5, 6, 8, 9], "g": [2, 3, 4, 5, 6, 8, 9],
}
DONT_CARE = range(10, 16)


def cover(ones, dont_care):
    """Essential primes first, then greedily the prime covering most 1s still bare."""
    primes = prime_implicants(ones, dont_care)
    chosen = essential(primes, ones)
    bare = [m for m in ones if not any(covers(p, m) for p in chosen)]
    while bare:
        best = max(primes, key=lambda p: (sum(covers(p, m) for m in bare),
                                          p.count("-")))
        chosen.append(best)
        bare = [m for m in bare if not covers(best, m)]
    return chosen


if __name__ == "__main__":
    total = 0
    for seg, ones in SEGMENTS.items():
        terms = cover(ones, DONT_CARE)
        ok = all(any(covers(t, d) for t in terms) == (d in ones) for d in range(10))
        total += sum(4 - t.count("-") for t in terms)
        formula = " + ".join(as_product(t) for t in terms)
        print(f"{seg} = {formula:27} correct on 0-9: {ok}")
    print(f"{total} literals in all, against {sum(map(len, SEGMENTS.values())) * 4}"
          f" in the canonical sums")
