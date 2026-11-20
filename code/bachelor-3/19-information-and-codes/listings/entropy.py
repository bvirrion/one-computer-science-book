"""entropy.py -- self-information and entropy of the letters of the library catalogue,
against a uniform source on the same alphabet."""
import math
from collections import Counter

from source import catalogue_text


def entropy(probabilities):
    """H = sum of p log2(1/p), in bits per symbol; zero probabilities add nothing."""
    return sum(p * math.log2(1 / p) for p in probabilities if p > 0)


def frequencies(text, block=1):
    """Relative frequencies of the non-overlapping blocks of `block` symbols."""
    blocks = [text[i:i + block] for i in range(0, len(text) - block + 1, block)]
    return {b: c / len(blocks) for b, c in Counter(blocks).items()}


if __name__ == "__main__":
    text = catalogue_text()
    f = frequencies(text)
    print(f"{len(text)} symbols, alphabet of {len(f)}")
    ranked = sorted(f, key=f.get, reverse=True)
    for ch in ranked[:3] + ranked[-1:]:
        print(f"  {ch!r}: p = {f[ch]:.4f}, information {math.log2(1 / f[ch]):.2f} bits")
    print(f"entropy of the letters: {entropy(f.values()):.3f} bits per symbol")
    print(f"uniform on {len(f)} symbols: {math.log2(len(f)):.3f} bits per symbol")
