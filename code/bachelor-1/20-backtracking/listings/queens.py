"""queens.py: n queens on an n x n board, none attacking another; one queen per row,
cols[r] is the column of the queen of row r."""

from math import factorial


def solve(n):
    """(solutions, nodes): the tree of partial solutions, pruned at the first attack."""
    cols, diag1, diag2 = set(), set(), set()  # used columns and diagonals
    count = [0, 0]  # solutions, nodes

    def place(r):
        count[1] += 1
        if r == n:
            count[0] += 1
            return
        for c in range(n):
            if c in cols or r - c in diag1 or r + c in diag2:
                continue  # attacked: this branch is pruned
            cols.add(c), diag1.add(r - c), diag2.add(r + c)
            place(r + 1)
            cols.remove(c), diag1.remove(r - c), diag2.remove(r + c)

    place(0)
    return count[0], count[1]


def full_tree_nodes(n):
    """Nodes of the tree of all partial permutations: the sum of n!/k! for k <= n."""
    return sum(factorial(n) // factorial(k) for k in range(n + 1))


def main():
    print(f"{'n':>2} {'solutions':>9} {'nodes, pruned':>13} {'nodes, full tree':>16} "
          f"{'ratio':>7}")
    for n in range(4, 11):
        sols, nodes = solve(n)
        full = full_tree_nodes(n)
        print(f"{n:2} {sols:9} {nodes:13} {full:16} {full / nodes:7.1f}")


if __name__ == "__main__":
    main()
