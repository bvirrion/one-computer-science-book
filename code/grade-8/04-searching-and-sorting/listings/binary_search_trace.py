items = [2, 5, 8, 12, 16, 23, 38, 41, 47, 56, 61, 72, 77, 85, 90, 98]
target = 77
low = 0
high = len(items) - 1
found = False
while low <= high and not found:
    middle = (low + high) // 2
    print("low", low, "middle", middle, "high", high, "->", items[middle])
    if items[middle] == target:
        found = True
    elif items[middle] < target:
        low = middle + 1
    else:
        high = middle - 1
print("found:", found)
