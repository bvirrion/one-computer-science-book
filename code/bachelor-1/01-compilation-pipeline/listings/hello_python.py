# hello_python.py: the same program in Python, run at once by the interpreter.
GREETING = "Hello from Python"


def square(x):
    return x * x


n = 7
print(f"{GREETING}: {n} squared is {square(n)}")
