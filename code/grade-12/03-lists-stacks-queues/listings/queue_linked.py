"""A queue of linked cells, with a pointer to each end."""
from cell import Cell


class Queue:
    def __init__(self):
        self._head = None                   # the first in line: dequeued next
        self._tail = None                   # the last in line
        self.moves = 0                      # cells linked or unlinked

    def is_empty(self):
        return self._head is None

    def enqueue(self, x):
        cell = Cell(x)
        if self.is_empty():
            self._head = cell
        else:
            self._tail.next = cell
        self._tail = cell
        self.moves += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        x = self._head.value
        self._head = self._head.next
        if self._head is None:              # the queue is empty again
            self._tail = None
        self.moves += 1
        return x
