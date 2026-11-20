"""exo_dups.py: exercise 4."""

from bsearch import leftmost

print(leftmost([1, 1, 1], 1), leftmost([1, 1, 1], 2), leftmost([1, 1, 1], 0))
print(leftmost([1, 2, 2, 2, 3], 2), leftmost([1, 2, 2, 2, 3], 3), leftmost([4], 4))
