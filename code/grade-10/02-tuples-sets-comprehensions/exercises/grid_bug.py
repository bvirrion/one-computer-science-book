"""Exercise 8: a grid built by repetition shares one inner list."""


def bad_grid(rows, cols):
    return [[0] * cols] * rows


def good_grid(rows, cols):
    return [[0] * cols for _ in range(rows)]


def demo():
    bad = bad_grid(3, 3)
    bad[0][0] = 1
    good = good_grid(3, 3)
    good[0][0] = 1
    return bad, good


if __name__ == "__main__":
    bad, good = demo()
    print(bad)
    print(good)
