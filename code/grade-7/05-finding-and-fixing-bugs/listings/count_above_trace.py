def count_above(values, limit):
    count = 0
    for value in values:
        if value > limit:
            count = count + 1
        print("  trace: value", value, "count", count)
        return count


print(count_above([3, 9, 7], 5))
