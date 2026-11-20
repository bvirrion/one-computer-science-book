"""trap_cost.py -- the slowdown of trap and emulate, counted. A guest loop runs B
instructions per iteration, one of them a clock read that traps (trap fraction f = 1/B);
the baseline is the same loop with an ordinary instruction instead. The cost of a run is
the number of Python lines the machine and the monitor execute: a clock that never
jitters."""
import sys

from monitor import Monitor
from rv import Machine

CLOCK_READ = ".word 0x5c2022f3"  # csrr t0, 0x5c2: traps to the monitor
PLAIN = "addi t0, t0, 1"
INSTRUCTIONS = 30_000


def guest(body, first):  # the loop's own add and branch count in its B instructions
    work = ["addi t1, t1, 1"] * (body - 3)
    return "\n".join([f"main: li t2, {INSTRUCTIONS // body}", "loop:", first, *work,
                      "addi t2, t2, -1", "bnez t2, loop", "li a0, 0", "ret"])


def cost(m):  # Python lines executed per guest instruction
    lines = 0

    def tracer(frame, event, arg):
        nonlocal lines
        lines += event == "line"
        return tracer

    sys.settrace(tracer)
    m.run(10 * INSTRUCTIONS)
    sys.settrace(None)
    return lines / m.steps


plain = cost(Machine(guest(3, PLAIN)))
T = cost(Monitor(guest(3, CLOCK_READ)).m) * 3 / plain - 2  # a trap, in plain ones
print(f"a plain instruction: {plain:.1f} lines; a trap: T = {T:.1f} plain instructions")
print("trap fraction f   counted slowdown   1 + f(T - 1)")
for body in (10, 30, 100, 300, 1000):
    slow = cost(Monitor(guest(body, CLOCK_READ)).m) / cost(Machine(guest(body, PLAIN)))
    print(f"{1 / body:>15.4f}   {slow:>16.4f}   {1 + (T - 1) / body:>12.4f}")
