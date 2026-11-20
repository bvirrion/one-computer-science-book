"""games.py: reachability games on a graph. Each position belongs to a player, who
chooses the next position among its successors; player p wins if play reaches the
target set."""
from collections import deque


def attractor(owner, succ, target, p):
    """The positions from which p can force a visit to target, each with its layer
    (target is reached within that many moves), and a memoryless strategy for p."""
    pred = {v: [] for v in owner}
    for u in owner:
        for v in succ[u]:
            pred[v].append(u)
    left = {u: len(succ[u]) for u in owner}  # successors not yet in the attractor
    layer = {v: 0 for v in target}
    strategy, queue = {}, deque(target)
    while queue:
        v = queue.popleft()
        for u in pred[v]:
            if u in layer:
                continue
            if owner[u] == p:  # one good move is enough
                layer[u], strategy[u] = layer[v] + 1, v
                queue.append(u)
            else:
                left[u] -= 1
                if left[u] == 0:  # every move of the opponent leads in
                    layer[u] = layer[v] + 1
                    queue.append(u)
    return layer, strategy
