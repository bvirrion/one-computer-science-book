"""A seeded maze as a grid graph; its shortest exit and the hand-on-wall walk."""
import random

from bfs import bfs, path_to
from dfs import dfs_stack

ROWS, COLS = 8, 14
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]          # north, east, south, west


def make_maze(seed=12):
    rng = random.Random(seed)
    g = {(r, c): [] for r in range(ROWS) for c in range(COLS)}
    seen, stack = {(0, 0)}, [(0, 0)]
    while stack:                                     # carve a tree of passages
        r, c = stack[-1]
        fresh = [(r + dr, c + dc) for dr, dc in MOVES if (r + dr, c + dc) in g
                 and (r + dr, c + dc) not in seen]
        if not fresh:
            stack.pop()
            continue
        nxt = rng.choice(fresh)
        g[(r, c)].append(nxt)
        g[nxt].append((r, c))
        seen.add(nxt)
        stack.append(nxt)
    for _ in range(12):                              # then knock down 12 more walls
        r, c = rng.randrange(ROWS - 1), rng.randrange(COLS - 1)
        a, b = (r, c), rng.choice([(r + 1, c), (r, c + 1)])
        if b not in g[a]:
            g[a].append(b)
            g[b].append(a)
    return g


def draw(g, marked=()):
    lines = ["+" + "--+" * COLS]
    for r in range(ROWS):
        row, floor = "|", "+"
        for c in range(COLS):
            row += (" *" if (r, c) in marked else "  ")
            row += " " if (r, c + 1) in g[(r, c)] else "|"
            floor += ("  " if (r + 1, c) in g[(r, c)] else "--") + "+"
        lines += [row, floor]
    return "\n".join(lines)


def wall_follower(g, start, goal):
    """Keep the right hand on the wall; return the number of steps taken."""
    (r, c), facing, steps = start, 1, 0              # facing east
    while (r, c) != goal:
        for turn in (1, 0, 3, 2):                    # right, ahead, left, back
            d = (facing + turn) % 4
            nxt = (r + MOVES[d][0], c + MOVES[d][1])
            if nxt in g[(r, c)]:
                (r, c), facing, steps = nxt, d, steps + 1
                break
    return steps


if __name__ == "__main__":
    g = make_maze()
    start, goal = (0, 0), (ROWS - 1, COLS - 1)
    dist, parent = bfs(g, start)
    path = path_to(parent, goal)
    print(draw(g, marked=set(path)))
    print("shortest exit:", dist[goal], "steps")
    print("depth-first search visits", dfs_stack(g, start).index(goal) + 1,
          "cells before reaching the exit")
    print("hand on the wall:", wall_follower(g, start, goal), "steps")
