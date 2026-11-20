"""forwarding.py: the forwarding unit, which picks where each ALU input comes from."""
import sys

from pipeline import steps_of
from rv import decode

REG_NAMES = ("zero ra sp gp tp t0 t1 t2 s0 s1 a0 a1 a2 a3 a4 a5 a6 a7 "
             "s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 t3 t4 t5 t6").split()


def forward(rs, ex_mem, mem_wb, check_x0=True):
    """ex_mem, mem_wb: (reg_write, rd) of the instructions one and two ahead."""
    for source, (reg_write, rd) in (("EX/MEM", ex_mem), ("MEM/WB", mem_wb)):
        if reg_write and rd == rs and (rd != 0 or not check_x0):
            return source  # the nearer one wins: it is the newer value
    return "register file"


def fields(step):
    """(reg_write, rd, rs1, rs2), as the pipeline registers hold them."""
    i = decode(step.word)
    reg_write = step.kind in ("alu", "muldiv", "load") or (step.kind == "jump")
    return reg_write, i.rd, i.rs1, i.rs2


def show(steps, check_x0=True):
    """For a stream without stalls: where each instruction takes its operands."""
    nothing = (False, 0)
    for k, s in enumerate(steps):
        reg_write, rd, rs1, rs2 = fields(s)
        ahead = [fields(steps[k - j])[:2] if k >= j else nothing for j in (1, 2)]
        uses = [rs1] + ([rs2] if decode(s.word).fmt in ("R", "S", "B") else [])
        picks = [f"{REG_NAMES[r]} <- {forward(r, *ahead, check_x0)}" for r in uses]
        print(f"{s.text:<20} " + ", ".join(picks))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        show(steps_of(f.read()), check_x0="--forget-x0" not in sys.argv)
