"""queens_subtrees.py: the size of each subtree under the root of the queens search."""


def subtree(n, c0):
    """Nodes of the n-queens search below a first queen at column c0, included."""
    cols, diag1, diag2 = {c0}, {-c0}, {c0}
    count = 0

    def place(r):
        nonlocal count
        count += 1
        if r == n:
            return
        for c in range(n):
            if c in cols or r - c in diag1 or r + c in diag2:
                continue
            cols.add(c), diag1.add(r - c), diag2.add(r + c)
            place(r + 1)
            cols.remove(c), diag1.remove(r - c), diag2.remove(r + c)

    place(1)
    return count


if __name__ == "__main__":
    print([subtree(6, c) for c in range(6)])
