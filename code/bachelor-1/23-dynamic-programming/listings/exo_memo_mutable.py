"""exo_memo_mutable.py: exercise 6, a memo keyed on a list the recursion changes."""

memo = {}


def ways(values, target):
    """Subsets of values with the given total; values is shortened and restored."""
    key = (id(values), target)
    if key in memo:
        return memo[key]
    if not values:
        result = int(target == 0)
    else:
        v = values.pop()  # decide the last value, then put it back
        result = ways(values, target) + ways(values, target - v)
        values.append(v)
    memo[key] = result
    return result


if __name__ == "__main__":
    values = [3, 5, 2, 8, 4]
    for target in (10, 13, 17):
        memo.clear()
        got = ways(values, target)
        true = sum(1 for m in range(32)
                   if sum(x for i, x in enumerate(values) if m >> i & 1) == target)
        print(f"total {target}: memoised {got}, all 32 subsets {true}")
