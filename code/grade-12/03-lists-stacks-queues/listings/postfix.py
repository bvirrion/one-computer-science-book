from stack_list import Stack

OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
       "*": lambda a, b: a * b, "/": lambda a, b: a / b}


def evaluate(expression, show=False):
    s = Stack()
    for token in expression.split():
        if token in OPS:
            b = s.pop()                      # the right operand is on top
            a = s.pop()
            s.push(OPS[token](a, b))
        else:
            s.push(float(token))
        if show:
            print(f"  read {token:>2}   top {s.top()}")
    result = s.pop()
    if not s.is_empty():
        raise ValueError("too many numbers")
    return result


print(evaluate("3 4 + 2 *", show=True))      # (3 + 4) * 2
print(evaluate("3 4 2 * +"))                 # 3 + 4 * 2
print(evaluate("10 2 8 * + 3 -"))            # 10 + 2 * 8 - 3
try:
    evaluate("1 +")
except IndexError as error:
    print("IndexError:", error)
