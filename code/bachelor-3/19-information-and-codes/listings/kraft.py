"""kraft.py -- the Kraft sum of a code, a test for the prefix property, and a prefix
code built from any lengths whose Kraft sum is at most 1."""
from fractions import Fraction


def kraft_sum(lengths):
    return sum(Fraction(1, 2 ** n) for n in lengths)


def is_prefix_free(words):
    words = sorted(words)  # a prefix sorts just before the words it starts
    return all(not b.startswith(a) for a, b in zip(words, words[1:]))


def code_from_lengths(lengths):
    """Canonical code: shortest first, each word the next binary number, padded."""
    assert kraft_sum(lengths) <= 1
    words, value, previous = [], 0, 0
    for n in sorted(lengths):
        value <<= n - previous  # extend the next free value to n bits
        words.append(format(value, f"0{n}b"))
        value, previous = value + 1, n
    return words


if __name__ == "__main__":
    for words in (["0", "10", "110", "111"], ["0", "01", "11"], ["00", "01", "10"]):
        print(f"{words}: Kraft sum {kraft_sum(map(len, words))}, "
              f"prefix-free {is_prefix_free(words)}")
    print("lengths 1, 2, 3, 3 ->", code_from_lengths([1, 2, 3, 3]))
    print("lengths 2, 2, 2, 3, 4, 4 ->", code_from_lengths([2, 2, 2, 3, 4, 4]))
    print("lengths 1, 1, 2: Kraft sum", kraft_sum([1, 1, 2]), "> 1, no prefix code")
