"""division.py: a specification checked by assertions, and a loop invariant."""


def divide(a, b):
    """Precondition: a >= 0 and b > 0.
    Postcondition: returns (q, r) with a == q * b + r and 0 <= r < b."""
    assert a >= 0 and b > 0, "precondition"
    q, r = 0, a
    while r >= b:
        assert a == q * b + r and r >= 0, "invariant"  # holds at each test
        q, r = q + 1, r - b  # the variant r decreases by b > 0
    assert a == q * b + r and 0 <= r < b, "postcondition"
    return q, r


def divide_unchecked(a, b, max_steps=1000):
    """The same loop without the precondition, with a step cap to show b == 0."""
    q, r, steps = 0, a, 0
    while r >= b:
        q, r, steps = q + 1, r - b, steps + 1
        if steps == max_steps:
            return f"still running after {steps} steps: q={q}, r={r}"
    return q, r


if __name__ == "__main__":
    print(divide(17, 5), divide(0, 3), divide(4, 9))
    print(divide_unchecked(17, 0))
    try:
        divide(17, 0)
    except AssertionError as e:
        print("AssertionError:", e)
