"""state_space.py: search in an implicit graph. A problem gives a start state, a goal
test and the successors of a state with their costs; each search counts the states
it expands."""
import heapq
from collections import deque


def path_to(parent, s):
    path = [s]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def bfs(start, is_goal, successors):
    parent, queue, expanded = {start: None}, deque([start]), 0
    while queue:
        s = queue.popleft()
        expanded += 1
        if is_goal(s):
            return path_to(parent, s), expanded
        for t, _ in successors(s):
            if t not in parent:
                parent[t] = s
                queue.append(t)
    return None, expanded


def depth_limited(s, is_goal, successors, limit, path, count):
    count[0] += 1
    if is_goal(s):
        return list(path)
    if limit == 0:
        return None
    for t, _ in successors(s):
        if t not in path:  # no cycles along the current path
            path.append(t)
            found = depth_limited(t, is_goal, successors, limit - 1, path, count)
            path.pop()
            if found:
                return found
    return None


def iterative_deepening(start, is_goal, successors, max_depth=50):
    count = [0]
    for limit in range(max_depth + 1):
        found = depth_limited(start, is_goal, successors, limit, [start], count)
        if found:
            return found, count[0]
    return None, count[0]


def astar(start, is_goal, successors, h=lambda s: 0, order=None):
    """A*: expand the state of smallest g + h. With h = 0, uniform-cost search.
    Returns (path, cost, number of states expanded); order lists them if given."""
    g, parent = {start: 0}, {start: None}
    frontier, done, tie = [(h(start), 0, start)], set(), 0
    while frontier:
        _, _, s = heapq.heappop(frontier)
        if s in done:
            continue  # a stale entry: s was reached again more cheaply
        done.add(s)
        if order is not None:
            order.append(s)
        if is_goal(s):
            return path_to(parent, s), g[s], len(done)
        for t, cost in successors(s):
            if t not in done and g[s] + cost < g.get(t, float("inf")):
                g[t], parent[t] = g[s] + cost, s
                tie += 1  # a counter breaks ties without comparing states
                heapq.heappush(frontier, (g[t] + h(t), tie, t))
    return None, float("inf"), len(done)
