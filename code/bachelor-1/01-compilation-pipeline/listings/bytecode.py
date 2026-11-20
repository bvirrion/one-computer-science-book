# bytecode.py: the bytecode that Python compiles a small function into.
import dis


def square_plus(x, y):
    return x * x + y


dis.dis(square_plus)
print(square_plus(7, 1))
