"""Halting within k steps is decidable: run at most k steps and look."""
from programs import COUNTDOWN, FOREVER, WRAP
from toymachine import Machine, assemble


def halts_within(text, k):
    m = Machine(assemble(text))
    while not m.halted and m.steps < k:
        m.step()
    return m.halted, m.steps


for name, text in [("COUNTDOWN", COUNTDOWN), ("FOREVER", FOREVER), ("WRAP", WRAP)]:
    for k in (100, 1000):
        halted, steps = halts_within(text, k)
        verdict = f"halts after {steps} steps" if halted else "has not halted"
        print(f"{name:9} within {k:4} steps: {verdict}")
