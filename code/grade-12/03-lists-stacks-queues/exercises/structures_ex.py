"""Exercises of the chapter on linked lists, stacks and queues."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
import stack_linked  # noqa: E402
import stack_list  # noqa: E402
from cell import Cell  # noqa: E402


class SizedListStack(stack_list.Stack):            # exercise 5
    def size(self):
        return len(self._items)


class SizedLinkedStack(stack_linked.Stack):        # exercise 5: a counter kept
    def __init__(self):
        super().__init__()
        self._size = 0

    def push(self, x):
        super().push(x)
        self._size += 1

    def pop(self):
        x = super().pop()
        self._size -= 1
        return x

    def size(self):
        return self._size


def length_rec(cell):                               # exercise 7
    return 0 if cell is None else 1 + length_rec(cell.next)


def length_iter(cell):
    n = 0
    while cell is not None:
        n, cell = n + 1, cell.next
    return n


class BrokenQueue:                                  # exercise 8: the staged fault
    def __init__(self):
        self._head = self._tail = None

    def enqueue(self, x):
        cell = Cell(x)
        if self._tail is None:
            self._head = cell
        else:
            self._tail.next = cell
        self._tail = cell

    def dequeue(self):
        x = self._head.value
        self._head = self._head.next                # the tail is never reset
        return x


def reverse(head):                                  # exercise 10
    previous = None
    while head is not None:
        head.next, previous, head = previous, head, head.next
    return previous


class CircularQueue:                                # exercise 13
    def __init__(self, capacity):
        self._slots = [None] * capacity
        self._first = 0                             # index of the oldest
        self._count = 0

    def enqueue(self, x):
        if self._count == len(self._slots):
            raise OverflowError("the queue is full")
        self._slots[(self._first + self._count) % len(self._slots)] = x
        self._count += 1

    def dequeue(self):
        if self._count == 0:
            raise IndexError("dequeue from an empty queue")
        x = self._slots[self._first]
        self._first = (self._first + 1) % len(self._slots)
        self._count -= 1
        return x


PRIORITY = {"+": 1, "-": 1, "*": 2, "/": 2}


def to_postfix(expression):                         # exercise 14
    out, ops = [], stack_list.Stack()
    for token in expression.split():
        if token in PRIORITY:
            while (not ops.is_empty() and ops.top() != "("
                   and PRIORITY[ops.top()] >= PRIORITY[token]):
                out.append(ops.pop())
            ops.push(token)
        elif token == "(":
            ops.push(token)
        elif token == ")":
            while ops.top() != "(":
                out.append(ops.pop())
            ops.pop()                               # drop the "("
        else:
            out.append(token)
    while not ops.is_empty():
        out.append(ops.pop())
    return " ".join(out)


if __name__ == "__main__":
    q = BrokenQueue()
    q.enqueue(1)
    q.dequeue()
    q.enqueue(2)
    print(q._head)
    print(to_postfix("( 2 + 3 ) * ( 7 - 4 ) / 5"))
