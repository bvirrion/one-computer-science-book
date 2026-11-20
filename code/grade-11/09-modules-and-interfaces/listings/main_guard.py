"""Greets only when started as a program, not when imported."""


def greet(name):
    return f"hello, {name}"


print("main_guard is running as", __name__)
if __name__ == "__main__":
    print(greet("ada"))
