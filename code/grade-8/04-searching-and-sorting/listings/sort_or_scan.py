from binary_search import binary_search
from count_comparisons import mixed
from insertion_sort import insertion_sort
from linear_search import linear_search
from selection_sort import selection_sort

n = 1000
words = mixed(n)            # 1,000 "words", numbered 0 to 999, in a mixed order

scan = 0
for target in range(n):
    position, comparisons = linear_search(words, target)
    scan = scan + comparisons
print("1,000 linear searches:", scan, "comparisons")

by_selection = selection_sort(list(words))
by_insertion = insertion_sort(list(words))
sorted_words = sorted(words)
halving = 0
for target in range(n):
    position, guesses = binary_search(sorted_words, target)
    halving = halving + guesses
print("selection sort:", by_selection, "+ 1,000 binary searches:", halving)
print("insertion sort:", by_insertion, "+ 1,000 binary searches:", halving)
