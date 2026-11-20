"""pb_fib.py -- instructions executed by the compiled fib(n), counted by rv,
against the Fibonacci numbers, for the weekend problem."""
from rv import Machine, assemble

prog = assemble(open("fib.S").read(), "fib.S")


def fibonacci(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


print(" n  F(n+1)  calls  instructions  loads  stores")
for n in range(21):
    m = Machine(prog, inputs=[n])
    calls = 0

    def count(step):
        global calls
        if step.text.startswith("jal ra"):
            calls += 1

    m.run(trace=count)
    s = m.stats
    print(f"{n:>2}  {fibonacci(n + 1):>6}  {calls:>5}  {s['instructions']:>12}"
          f"  {s['loads']:>5}  {s['stores']:>6}")
