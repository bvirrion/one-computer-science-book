"""linearizable.py -- is a recorded history of a concurrent FIFO queue linearisable?
Search for an order of its operations that respects real time and a FIFO queue."""
from collections import deque


def linearise(history):
    """history: (thread, op, arg, result, start, end) tuples. An order, or None."""
    def search(left, queue, order):
        if not left:
            return order
        first_end = min(h[5] for h in left)
        for h in left:
            if h[4] > first_end:  # h began after another op ended: that one comes first
                continue
            _, op, arg, result, _, _ = h
            q = deque(queue)
            if op == "enq":
                q.append(arg)
            elif (q.popleft() if q else None) != result:
                continue  # the sequential queue would not return this result here
            found = search([g for g in left if g is not h], q, order + [h])
            if found:
                return found
        return None

    return search(list(history), deque(), [])


if __name__ == "__main__":
    HISTORIES = {  # thread, operation, argument, result, start time, end time
        "overlapping enqueues": [
            ("A", "enq", 1, None, 0, 4), ("B", "enq", 2, None, 1, 3),
            ("A", "deq", None, 2, 5, 6), ("B", "deq", None, 1, 7, 8)],
        "dequeue during enqueue": [
            ("A", "enq", 1, None, 0, 6), ("B", "deq", None, 1, 2, 4),
            ("B", "deq", None, None, 5, 7)],
        "order reversed": [
            ("A", "enq", 1, None, 0, 2), ("B", "enq", 2, None, 3, 5),
            ("A", "deq", None, 2, 6, 8)],
    }
    for name, history in HISTORIES.items():
        order = linearise(history)
        shown = "none exists" if order is None else ", ".join(
            f"{t}.{op}({'' if a is None else a})"
            + (f"->{'empty' if r is None else r}" if op == "deq" else "")
            for t, op, a, r, _, _ in order)
        print(f"{name:<24} {shown}")
