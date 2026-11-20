"""Milestone 5: disassembling one instruction, and a trace like the shared tool."""
from assembler_m2 import OPS


def disassemble(b0, b1):
    """The assembly text of the two bytes b0, b1."""
    opcode, r = b0 // 4, b0 % 4
    if opcode >= len(OPS):
        return f"?? ({b0} {b1})"
    name, kind = OPS[opcode]
    shapes = {"": name, "r": f"{name} R{r}", "a": f"{name} {b1}",
              "rn": f"{name} R{r}, {b1}", "r[a]": f"{name} R{r}, [{b1}]",
              "rs": f"{name} R{r}, R{b1 % 4}"}
    return shapes[kind]


HEADER = (f"{'step':>4} {'PC':>3}  {'instruction':<16} {'R0':>3} {'R1':>3} {'R2':>3}"
          f" {'R3':>3}  Z N C")


def trace_row(m):
    """One row, printed before each step: what is about to run, and the state."""
    pc, f = m["pc"], m["flags"]
    text = disassemble(m["mem"][pc], m["mem"][(pc + 1) % 256])
    registers = " ".join(f"{v:3d}" for v in m["reg"])
    flags = f"{f['Z']} {f['N']} {f['C']}"
    return f"{m['steps'] + 1:4d} {pc:3d}  {text:<16} {registers}  {flags}"


def run_traced(m, run, max_steps=10_000):
    """Run with a trace; an output is printed as soon as OUT runs, as the tool does."""
    print(HEADER)
    printed = 0

    def trace(m):
        nonlocal printed
        for v in m["outputs"][printed:]:
            print(v)
        printed = len(m["outputs"])
        print(trace_row(m))

    run(m, max_steps, trace)
    for v in m["outputs"][printed:]:
        print(v)
    print(f"halted after {m['steps']} steps")
