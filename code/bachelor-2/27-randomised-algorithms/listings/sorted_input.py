"""sorted_input.py: the town's 120 people, already sorted, given to quicksort."""
import random

from quicksort import first, quicksort, random_pivot, shuffle
from town import people

names = sorted(people())
n = len(names)
for label, data, pick in [
        ("first pivot, sorted list", names, first),
        ("first pivot, shuffled list", shuffle(names, random.Random(1)), first),
        ("random pivot, sorted list", names, random_pivot(random.Random(1)))]:
    count = [0]
    assert quicksort(data, pick, count) == names
    print(f"{label:27}: {count[0]:5} comparisons")
print(f"n(n - 1)/2 = {n * (n - 1) // 2}")
