"""refcount.py -- CPython counts references; its cycle collector finds what
counting misses."""
import gc
import sys


class Loan:
    def __init__(self, title):
        self.title, self.other = title, None

    def __del__(self):
        print(f"  freed {self.title}")


a = Loan("Dune")
print("one name:        ", sys.getrefcount(a))  # one more: the argument itself
b = a
shelf = [a, a]
print("three more:      ", sys.getrefcount(a))
del b
shelf.clear()
print("back to one name:", sys.getrefcount(a))
print("del a:")
del a  # the count drops to zero: freed at once

gc.disable()  # no automatic cycle collection while we watch
x, y = Loan("Emma"), Loan("Ulysses")
x.other, y.other = y, x  # a cycle: each keeps the other's count at 1
print("del x, y:")
del x, y
print("  (nothing freed)")
print("gc.collect():")
print("  unreachable objects found:", gc.collect())
