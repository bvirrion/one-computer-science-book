"""Exercises 4, 10 and 11 of the chapter on modules."""
import statistics
from collections import Counter


def ex4():
    return statistics.median([7, 1, 3, 9]), Counter("banana").most_common(2)


def ex10():
    before = pow(2, 10)
    from math import pow as math_pow    # what "from math import *" brings in
    return before, math_pow(2, 10)


def word_count(text, n):                # exercise 11
    """Return the n most common words of text, in lower case, with their counts."""
    words = [w.strip(".,;:!?") for w in text.lower().split()]
    return Counter(w for w in words if w).most_common(n)


if __name__ == "__main__":
    print(ex4(), ex10())
    print(word_count("The cat saw the dog. The dog saw the cat run.", 3))
