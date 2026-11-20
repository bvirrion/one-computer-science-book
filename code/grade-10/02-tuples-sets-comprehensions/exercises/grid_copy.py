"""Exercise 14: copying a grid for the next step of a game."""
import copy


def next_step_buggy(grid):
    new = list(grid)  # shallow: the rows are shared
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            new[r][c] = 1 - grid[r][c]
    return new


def next_step(grid):
    new = copy.deepcopy(grid)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            new[r][c] = 1 - grid[r][c]
    return new
