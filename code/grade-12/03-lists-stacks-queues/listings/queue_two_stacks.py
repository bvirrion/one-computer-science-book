"""A queue made of two stacks: arrivals go in, departures come out."""
from stack_linked import Stack


class Queue:
    def __init__(self):
        self._in = Stack()                  # the newest on top
        self._out = Stack()                 # the oldest on top
        self.moves = 0                      # elements placed or removed

    def is_empty(self):
        return self._in.is_empty() and self._out.is_empty()

    def enqueue(self, x):
        self._in.push(x)
        self.moves += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        if self._out.is_empty():            # transfer: reverses the order
            while not self._in.is_empty():
                self._out.push(self._in.pop())
                self.moves += 1
        self.moves += 1
        return self._out.pop()
