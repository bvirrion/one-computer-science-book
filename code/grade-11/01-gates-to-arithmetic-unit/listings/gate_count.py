"""Count the gates of an adder, and the longest chain of gates a signal goes through."""

count = 0


def gate(*inputs):
    """A gate seen from outside: its output is ready one level after its last input."""
    global count
    count += 1
    return max(inputs) + 1


def full_adder(a, b, c):  # the same five gates as full_adder.py, on levels
    p = gate(a, b)                      # XOR
    s = gate(p, c)                      # XOR
    carry = gate(gate(a, b), gate(p, c))  # OR of two ANDs
    return s, carry


def ripple(n, carry=0):
    sums = []
    for _ in range(n):
        s, carry = full_adder(0, 0, carry)  # the inputs are ready at level 0
        sums.append(s)
    return sums, carry


def carry_select(n):
    """The low half ripples; the high half is computed twice, for carry 0 and 1."""
    low, c = ripple(n // 2)
    high0, c0 = ripple(n // 2, 0)  # assuming carry 0
    high1, c1 = ripple(n // 2, 0)  # assuming carry 1: a constant too, at level 0
    not_c = gate(c)
    chosen = [gate(gate(not_c, x0), gate(c, x1))  # a 2:1 multiplexer per bit
              for x0, x1 in zip(high0 + [c0], high1 + [c1])]
    return low + chosen[:-1], chosen[-1]


def measure(adder, n):
    global count
    count = 0
    sums, carry = adder(n)
    return count, max(sums + [carry])


print("   n | ripple: gates levels | carry-select: gates levels")
for n in (2, 4, 8, 16, 32, 64):
    g1, d1 = measure(ripple, n)
    g2, d2 = measure(carry_select, n)
    print(f"{n:4} | {g1:13} {d1:6} | {g2:19} {d2:6}")
