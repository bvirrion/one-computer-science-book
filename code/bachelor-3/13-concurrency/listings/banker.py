"""banker.py -- Dijkstra's banker: grant a request only if the state after it is safe,
that is, if some order lets every process obtain its maximum claim and finish."""


def safe_order(available, alloc, need):
    """An order in which all processes can finish, or None if the state is unsafe."""
    work, done, order = list(available), [False] * len(alloc), []
    while len(order) < len(alloc):
        for i in range(len(alloc)):
            if not done[i] and all(n <= w for n, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]  # i finishes, frees all
                done[i] = True
                order.append(i)
                break
        else:
            return None  # nobody can finish with what is left
    return order


def request(i, req, available, alloc, need):
    """Grant req to process i if the resulting state is safe; returns the new state."""
    if any(r > n for r, n in zip(req, need[i])):
        raise ValueError("more than its declared maximum")
    if any(r > a for r, a in zip(req, available)):
        return None  # must wait: not enough free now
    available = [a - r for a, r in zip(available, req)]
    alloc = [row[:] for row in alloc]
    need = [row[:] for row in need]
    alloc[i] = [a + r for a, r in zip(alloc[i], req)]
    need[i] = [n - r for n, r in zip(need[i], req)]
    if safe_order(available, alloc, need) is None:
        return None  # granting it could lead to deadlock: wait
    return available, alloc, need


if __name__ == "__main__":
    total = [6, 5, 6]  # three kinds of resource
    maximum = [[4, 2, 2], [3, 2, 2], [2, 3, 3], [2, 1, 3], [3, 3, 1]]
    alloc = [[1, 1, 0], [2, 0, 1], [0, 1, 1], [1, 0, 2], [0, 2, 0]]
    need = [[m - a for m, a in zip(mr, ar)] for mr, ar in zip(maximum, alloc)]
    available = [t - sum(col) for t, col in zip(total, zip(*alloc))]
    print("available", available, " need", need)
    print("safe order:", safe_order(available, alloc, need))
    for i, req in ((1, [1, 0, 0]), (4, [1, 0, 1])):
        state = request(i, req, available, alloc, need)
        verdict = "refused: unsafe" if state is None else (
            f"granted; safe order {safe_order(*state)}")
        print(f"P{i} asks for {req}: {verdict}")
