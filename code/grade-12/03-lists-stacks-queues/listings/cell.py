"""Linked lists made of cells."""


class Cell:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next                # the next cell, or None at the end


def from_list(values):
    head = None
    for v in reversed(values):          # build from the end: each new cell leads
        head = Cell(v, head)
    return head


def to_list(head):
    out = []
    cell = head
    while cell is not None:
        out.append(cell.value)
        cell = cell.next
    return out
