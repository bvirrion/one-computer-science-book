"""Problem: the steps of both multiplications, for every b from 0 to 255."""
from pathlib import Path

from toymachine import Machine, assemble

HERE = Path(__file__).parent


def steps(program, a, b):
    m = Machine(program, inputs=[a, b])
    m.run()
    assert m.outputs == [a * b % 256]
    return m.steps


repeated = assemble((HERE / "multiply.toy").read_text())
shifting = assemble((HERE / "shift_multiply.toy").read_text())
for name, program in (("repeated addition", repeated), ("shift and add", shifting)):
    counts = [steps(program, 13, b) for b in range(256)]
    worst = max(counts)
    mean = sum(counts) / 256
    print(f"{name:17}: b = 0 -> {counts[0]:3} steps, b = 1 -> {counts[1]:3},"
          f" worst {worst} (first at b = {counts.index(worst)}), mean {mean:.1f}")
