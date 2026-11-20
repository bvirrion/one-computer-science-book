"""A stack made of linked cells: the top is the first cell."""
from cell import Cell


class Stack:
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def push(self, x):
        self._head = Cell(x, self._head)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        x = self._head.value
        self._head = self._head.next
        return x

    def top(self):
        if self.is_empty():
            raise IndexError("top of an empty stack")
        return self._head.value
