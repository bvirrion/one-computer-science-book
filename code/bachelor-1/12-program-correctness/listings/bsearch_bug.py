"""bsearch_bug.py: a closed interval mixed with a half-open update."""


def search(a, x, max_steps=20):
    lo, hi = 0, len(a) - 1
    steps = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid  # should be mid - 1 on a closed interval
        steps += 1
        if steps == max_steps:
            return f"stuck: lo={lo} hi={hi} mid={mid} after {steps} steps"
    return -1


if __name__ == "__main__":
    print(search([2, 5, 8], 5), search([2, 5, 8], 9))
    print(search([2, 5, 8], 1))
