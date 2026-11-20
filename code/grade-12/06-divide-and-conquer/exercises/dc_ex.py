"""Exercises of the chapter on divide and conquer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from merge import merge  # noqa: E402


def merge_desc(a, b):                              # exercise 5
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] >= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]


def merge_no_tail(a, b):                           # exercise 6: the staged fault
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out


def mat_mult(p, q):
    return [[sum(p[i][k] * q[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def fib(n):                                        # exercise 7
    result, square = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
    while n > 0:
        if n % 2 == 1:
            result = mat_mult(result, square)
        square = mat_mult(square, square)
        n //= 2
    return result[0][1]


def merge_sort_bad_mid(t, depth=0):                # exercise 10: the staged fault
    if len(t) <= 1:
        return list(t)
    mid = len(t) // 2 + 1                          # for two items: mid = 2
    return merge(merge_sort_bad_mid(t[:mid], depth + 1),
                 merge_sort_bad_mid(t[mid:], depth + 1))[0]


def merge_sort_bottom_up(t):                       # exercise 11
    runs = [[x] for x in t]
    while len(runs) > 1:
        runs = [merge(runs[k], runs[k + 1])[0] if k + 1 < len(runs) else runs[k]
                for k in range(0, len(runs), 2)]
    return runs[0] if runs else []


def rotate_layers(grid):                           # exercise 13: any n, in place
    n = len(grid)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for k in range(last - first):
            top = grid[first][first + k]
            grid[first][first + k] = grid[last - k][first]        # left -> top
            grid[last - k][first] = grid[last][last - k]          # bottom -> left
            grid[last][last - k] = grid[first + k][last]          # right -> bottom
            grid[first + k][last] = top                           # top -> right


def max_subarray(t):                               # exercise 15: t not empty
    if len(t) == 1:
        return t[0]
    mid = len(t) // 2
    best_left = max_subarray(t[:mid])
    best_right = max_subarray(t[mid:])
    s, across_left = 0, t[mid - 1]
    for x in reversed(t[:mid]):                    # best sum ending at mid - 1
        s += x
        across_left = max(across_left, s)
    s, across_right = 0, t[mid]
    for x in t[mid:]:                              # best sum starting at mid
        s += x
        across_right = max(across_right, s)
    return max(best_left, best_right, across_left + across_right)


if __name__ == "__main__":
    print(merge_no_tail([1, 4, 9], [2, 3]), fib(90))
    print(merge_sort_bottom_up([5, 2, 4, 6, 1, 3]))
    print(max_subarray([2, -5, 3, 4, -1, 6, -8, 2]))
    try:
        merge_sort_bad_mid([2, 1])
    except RecursionError as error:
        print("RecursionError:", error)
