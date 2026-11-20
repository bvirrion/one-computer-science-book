from binary_search import binary_search
from linear_search import linear_search

ages = [12, 9, 15, 11, 9, 14, 13, 10]       # not sorted
print("binary:", binary_search(ages, 15))
print("linear:", linear_search(ages, 15))
