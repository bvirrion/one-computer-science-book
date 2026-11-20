from stack_list import Stack

PAIRS = {")": "(", "]": "[", "}": "{"}


def balanced(text):
    s = Stack()
    for ch in text:
        if ch in "([{":
            s.push(ch)                       # an opening waits for its closing
        elif ch in PAIRS:
            if s.is_empty() or s.pop() != PAIRS[ch]:
                return False                 # nothing open, or the wrong kind
    return s.is_empty()                      # nothing left open


for text in ["f(a[i], {k: (1, 2)})", "(]", "((x)", "x)(", "print('hi')"]:
    print(f"{text:22} {balanced(text)}")
