"""What happens to each count when n doubles."""
from count_insertion import insertion_sort
from count_linear import search

previous = None
for n in [1000, 2000, 4000]:
    linear = search(list(range(n)), -1)[1]             # worst case: absent
    quadratic = insertion_sort(list(range(n, 0, -1)))  # worst case: reversed
    line = f"n = {n:4}: linear search {linear:5}, insertion sort {quadratic:9}"
    if previous:
        line += f"   ratios {linear / previous[0]:.2f}"
        line += f" and {quadratic / previous[1]:.2f}"
    print(line)
    previous = (linear, quadratic)
