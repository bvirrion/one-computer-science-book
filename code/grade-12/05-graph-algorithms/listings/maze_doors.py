"""The same maze, where some passages are doors that take 6 seconds to open."""
import random

from bfs import bfs, path_to
from dijkstra import dijkstra
from maze import COLS, ROWS, make_maze

maze = make_maze()
rng = random.Random(5)
passages = sorted({tuple(sorted((a, b))) for a in maze for b in maze[a]})
doors = set(rng.sample(passages, 30))
g = {a: {b: 6 if tuple(sorted((a, b))) in doors else 1 for b in maze[a]} for a in maze}

start, goal = (0, 0), (ROWS - 1, COLS - 1)
short = path_to(bfs(maze, start)[1], goal)
cost_short = sum(g[a][b] for a, b in zip(short, short[1:]))
dist, parent = dijkstra(g, start)
cheap = path_to(parent, goal)
print(len(passages), "passages,", len(doors), "of them doors")
print(f"fewest steps: {len(short) - 1} steps, {cost_short} seconds")
print(f"fastest:      {len(cheap) - 1} steps, {dist[goal]} seconds")
