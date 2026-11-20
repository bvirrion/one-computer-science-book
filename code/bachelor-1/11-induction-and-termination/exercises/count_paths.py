"""count_paths.py: the number of paths from the root to a leaf."""


def count_paths(t):
    if t is None:
        return 0
    if t.left is None and t.right is None:
        return 1  # the path made of the leaf alone
    return count_paths(t.left) + count_paths(t.right)
