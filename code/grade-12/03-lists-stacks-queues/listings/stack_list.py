"""A stack kept in a Python list: the top is the end of the list."""


class Stack:
    def __init__(self):
        self._items = []

    def is_empty(self):
        return self._items == []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def top(self):
        if self.is_empty():
            raise IndexError("top of an empty stack")
        return self._items[-1]
