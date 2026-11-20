import sys


def countdown(n):
    if n == 0:
        return "done"
    return countdown(n - 1)


print("recursion limit:", sys.getrecursionlimit())
print(countdown(500))
sys.setrecursionlimit(100)           # lowered, to fail quickly
try:
    countdown(500)
except RecursionError as error:
    print("RecursionError:", error)
