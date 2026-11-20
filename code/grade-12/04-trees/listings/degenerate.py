import random

from bst import build, search
from node import height

for keys in [[1, 2, 3, 4, 5, 6, 7], [4, 2, 6, 1, 3, 5, 7], [7, 1, 6, 2, 5, 3, 4]]:
    print(keys, "-> height", height(build(keys)))

n = 1023
sorted_tree = build(range(1, n + 1))
shuffled = list(range(1, n + 1))
random.Random(4).shuffle(shuffled)
shuffled_tree = build(shuffled)
print(f"n = {n}, one shuffled order: height {height(shuffled_tree)},"
      f" finding {n} visits {search(shuffled_tree, n)} nodes")
print(f"n = {n}, sorted order: finding {n} visits {search(sorted_tree, n)} nodes")
try:
    height(sorted_tree)
except RecursionError as error:
    print("height of the sorted tree: RecursionError:", error)
