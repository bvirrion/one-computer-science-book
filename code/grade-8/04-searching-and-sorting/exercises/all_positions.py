def all_positions(items, target):
    positions = []
    for i in range(len(items)):
        if items[i] == target:
            positions.append(i)
    return positions


print(all_positions([12, 9, 15, 11, 9, 14, 13, 9], 9), all_positions([1, 2], 5))
