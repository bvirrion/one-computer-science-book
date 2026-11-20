"""maximum.py: the maximum of a non-empty list, with its invariant checked."""


def maximum(xs):
    """Precondition: xs is not empty. Postcondition: returns m in xs, m >= every x."""
    m, i = xs[0], 1
    while i < len(xs):
        # invariant: m is the maximum of xs[0:i], and 1 <= i <= len(xs)
        assert m in xs[:i] and all(m >= x for x in xs[:i]) and 1 <= i <= len(xs)
        if xs[i] > m:
            m = xs[i]
        i += 1  # variant: len(xs) - i
    return m  # i == len(xs): m is the maximum of xs[0:len(xs)], all of xs


if __name__ == "__main__":
    print(maximum([3, 9, 2, 9, 4]), maximum([-5]), maximum([1, 2, 3]))
