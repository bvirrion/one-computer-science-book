"""chain.py: the cheapest order to multiply a chain of matrices."""


def chain_order(dims):
    """Matrix i is dims[i] x dims[i+1]. Returns (cost table, split table)."""
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):  # by diagonals: shorter chains first
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = None
            for k in range(i, j):  # (A_i ... A_k)(A_k+1 ... A_j)
                c = cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost[i][j] is None or c < cost[i][j]:
                    cost[i][j], split[i][j] = c, k
    return cost, split


def parenthesise(split, i, j):
    if i == j:
        return f"A{i + 1}"
    k = split[i][j]
    return f"({parenthesise(split, i, k)} {parenthesise(split, k + 1, j)})"


def main():
    dims = [20, 5, 40, 10, 30, 4]  # five matrices: 20x5, 5x40, 40x10, 10x30, 30x4
    cost, split = chain_order(dims)
    n = len(dims) - 1
    print("cost table (row i, column j: A_i ... A_j)")
    for i in range(n):
        cells = [" " * 6 if j < i else f"{cost[i][j]:6}" for j in range(n)]
        print("  " + " ".join(cells))
    print("best order:", parenthesise(split, 0, n - 1), "with", cost[0][n - 1],
          "products")
    left_to_right = sum(dims[0] * dims[k] * dims[k + 1] for k in range(1, n))
    print("left to right:", left_to_right, "products")


if __name__ == "__main__":
    main()
