"""shift.py: a 4-bit register with an enable input, and a 4-bit shift register, clock
edge by clock edge. Each bit is one D flip-flop; a multiplexer in front of it chooses
what it loads."""


def mux(s, x0, x1):
    return ((1 - s) & x0) | (s & x1)  # s' x0 + s x1


def register_next(q, d, enable):
    """Load d when enable is 1, keep q otherwise."""
    return [mux(enable, qi, di) for qi, di in zip(q, d)]


def shift_next(q, serial_in):
    """q[0] is the left bit; every bit moves one place right, serial_in enters left."""
    return [serial_in] + q[:-1]


if __name__ == "__main__":
    q = [0, 0, 0, 0]
    for d, e in [([1, 0, 1, 1], 0), ([1, 0, 1, 1], 1), ([0, 1, 1, 0], 0),
                 ([0, 1, 1, 0], 1)]:
        q = register_next(q, d, e)
        print(f"register: D = {''.join(map(str, d))}, enable {e}",
              f"-> Q = {''.join(map(str, q))}")
    q = [0, 0, 0, 0]
    for edge, bit in enumerate([1, 1, 0, 1, 0, 0], start=1):
        q = shift_next(q, bit)
        print(f"shift register, edge {edge}: in {bit} -> {''.join(map(str, q))}")
