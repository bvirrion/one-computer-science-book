"""For the toy machine without IN, halting is decidable: watch for a repeated state."""
from programs import COUNTDOWN, FOREVER, SPIN, WRAP
from toymachine import Machine, assemble


def state(m):
    """Everything that decides the future: memory, registers, PC, SP, flags."""
    return bytes(m.mem + m.reg + [m.pc, m.sp, m.flags["Z"], m.flags["N"], m.flags["C"]])


def decide(text):
    m, seen = Machine(assemble(text)), set()
    while not m.halted:
        s = state(m)
        if s in seen:                            # the same state: the same future
            return "never halts", m.steps, len(seen)
        seen.add(s)
        m.step()
    return "halts", m.steps, len(seen)


for name, text in [("COUNTDOWN", COUNTDOWN), ("FOREVER", FOREVER), ("WRAP", WRAP),
                   ("SPIN", SPIN)]:
    verdict, steps, states = decide(text)
    print(f"{name:9}: {verdict:11} decided after {steps:3} steps,"
          f" {states:3} states stored")
