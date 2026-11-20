"""wordsearch.py: is a word written in the grid along a path of neighbouring cells
(horizontally, vertically or diagonally), each cell used at most once?"""


def find(grid, word):
    """The path of cells (row, column) spelling word, or None."""
    rows, cols = len(grid), len(grid[0])
    path = []

    def extend(r, c, k):  # word[:k] is spelled by path, which ends next to (r, c)
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in path:
            return False
        if grid[r][c] != word[k]:
            return False
        path.append((r, c))
        if k + 1 == len(word):
            return True
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc) and extend(r + dr, c + dc, k + 1):
                    return True
        path.pop()  # a dead end: free the cell
        return False

    for r in range(rows):
        for c in range(cols):
            if extend(r, c, 0):
                return list(path)
    return None
