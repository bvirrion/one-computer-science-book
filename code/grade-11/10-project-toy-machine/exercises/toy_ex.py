"""Exercises of the toy-machine project."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
import simulator_m4  # noqa: E402
from assembler_m2 import OPS, first_pass, second_pass  # noqa: E402
from simulator_m4 import set_flags  # noqa: E402
from tokens import read_program  # noqa: E402
from trace_m5 import disassemble  # noqa: E402


def parse_number(tok):                                  # exercise 5
    tok = tok.strip()
    if len(tok) == 3 and tok[0] == tok[2] == "'":
        value = ord(tok[1])
    elif tok.lower().startswith(("0x", "-0x")):
        value = int(tok, 16)
    elif tok.lower().startswith(("0b", "-0b")):
        value = int(tok, 2)
    else:
        value = int(tok)
    if not -128 <= value <= 255:
        raise ValueError(f"{value} does not fit in one byte")
    return value % 256


def not_(m, r, b):                                      # exercise 7
    m["reg"][r] = set_flags(m, 255 - m["reg"][r])


def shr(m, r, b):
    m["reg"][r] = set_flags(m, m["reg"][r] // 2, m["reg"][r] % 2)


def dump(m):                                            # exercise 10
    f = m["flags"]
    lines = ["R0={} R1={} R2={} R3={} PC={} SP={} Z={} N={} C={}".format(
        *m["reg"], m["pc"], m["sp"], f["Z"], f["N"], f["C"])]
    cells = [(a, v) for a, v in enumerate(m["mem"]) if v]
    for i in range(0, len(cells), 8):
        lines.append("  " + "  ".join(f"M[{a}]={v}" for a, v in cells[i:i + 8]))
    return "\n".join(lines)


def expand(rows):                                       # exercise 12: INC r
    out = []
    for line, label, mnemonic, operands in rows:
        if mnemonic == "INC":
            mnemonic, operands = "ADDI", operands + ["1"]
        out.append((line, label, mnemonic, operands))
    return out


def assemble_with_inc(text):
    rows = expand(read_program(text))
    memory = [0] * 256
    for address, data, _line in second_pass(rows, first_pass(rows)):
        memory[address:address + len(data)] = data
    return memory


def disassemble_program(memory, end):                   # exercise 14
    """Lines 'address: text' for the instructions before address end, DATA after."""
    lines = [f"{a:3d}: {disassemble(memory[a], memory[a + 1])}"
             for a in range(0, end, 2)]
    last = max((a for a, v in enumerate(memory) if v), default=end - 1)
    if last >= end:
        rest = ", ".join(str(v) for v in memory[end:last + 1])
        lines.append(f"{end:3d}: DATA {rest}")
    return lines


def count_instructions():                               # exercise 15
    per_kind = {"": 1, "r": 4, "a": 256, "rn": 4 * 256, "r[a]": 4 * 256, "rs": 16}
    return sum(per_kind[kind] for _, kind in OPS)


def inverted_borrow():                                  # exercise 8: the staged fault
    def sub(m, r, s):
        a, b = m["reg"][r], m["reg"][s % 4]
        m["reg"][r] = set_flags(m, a - b, a >= b)

    def cmp(m, r, s):
        a, b = m["reg"][r], m["reg"][s % 4]
        set_flags(m, a - b, a >= b)

    return simulator_m4.EXECUTE | {5: sub, 13: cmp}


if __name__ == "__main__":
    print(count_instructions(), disassemble(0x51, 0))
