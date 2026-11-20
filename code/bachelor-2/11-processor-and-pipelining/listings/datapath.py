"""datapath.py: a single-cycle datapath for a subset of RV32I, checked against rv."""
import sys
from dataclasses import dataclass

from rv import Machine

MASK = 0xFFFFFFFF


@dataclass(frozen=True)
class Control:
    """The control signals the control unit derives from the opcode."""
    name: str
    alu_src: int       # 1: the ALU's second operand is the immediate, 0: rs2
    mem_to_reg: int    # 1: the register written from data memory, 0: from the ALU
    reg_write: int
    mem_read: int
    mem_write: int
    branch: int
    alu_op: str        # "add", "funct" (look at funct3/funct7), "compare" (branch)


CONTROL = {                       # opcode -> signals: the control table
    0b0110011: Control("R-type", 0, 0, 1, 0, 0, 0, "funct"),
    0b0010011: Control("I-type", 1, 0, 1, 0, 0, 0, "funct"),
    0b0000011: Control("lw",     1, 1, 1, 1, 0, 0, "add"),
    0b0100011: Control("sw",     1, 0, 0, 0, 1, 0, "add"),
    0b1100011: Control("branch", 0, 0, 0, 0, 0, 1, "compare"),
}


def signed(v):
    return v - (1 << 32) if v & 0x80000000 else v


def sext(v, bits):
    return v - (1 << bits) if v >> (bits - 1) & 1 else v


def imm_gen(word):
    """The immediate generator: gather the scattered bits, then sign-extend."""
    op = word & 0x7F
    if op in (0b0010011, 0b0000011):  # I
        return sext(word >> 20, 12)
    if op == 0b0100011:               # S
        return sext((word >> 25) << 5 | (word >> 7) & 0x1F, 12)
    if op == 0b1100011:               # B
        return sext((word >> 31) << 12 | (word >> 7 & 1) << 11
                    | (word >> 25 & 0x3F) << 5 | (word >> 8 & 0xF) << 1, 13)
    return 0


ALU = {
    "add": lambda a, b: a + b, "sub": lambda a, b: a - b,
    "and": lambda a, b: a & b, "or": lambda a, b: a | b, "xor": lambda a, b: a ^ b,
    "sll": lambda a, b: a << (b & 31), "srl": lambda a, b: (a & MASK) >> (b & 31),
    "sra": lambda a, b: signed(a & MASK) >> (b & 31),
    "slt": lambda a, b: int(signed(a & MASK) < signed(b & MASK)),
    "sltu": lambda a, b: int((a & MASK) < (b & MASK)),
}
FUNCT3 = dict(enumerate(["add", "sll", "slt", "sltu", "xor", "srl", "or", "and"]))
BRANCH = {0: lambda a, b: a == b, 1: lambda a, b: a != b,
          4: lambda a, b: signed(a) < signed(b), 5: lambda a, b: signed(a) >= signed(b),
          6: lambda a, b: a < b, 7: lambda a, b: a >= b}


def alu_control(c, word):
    """ALU control: the operation from alu_op and the funct fields."""
    if c.alu_op == "add":
        return "add"
    f3, f7 = word >> 12 & 7, word >> 25
    op = FUNCT3[f3]
    if op == "add" and f7 == 0b0100000 and c.name == "R-type":
        return "sub"           # addi has no sub: its bit 30 is immediate
    if op == "srl" and f7 == 0b0100000:
        return "sra"
    return op


@dataclass(frozen=True)
class Effect:
    rd: int | None
    rd_value: int | None
    mem_addr: int | None
    mem_value: int | None
    next_pc: int


def cycle(m, pc, word):
    """One clock cycle of the datapath, reading machine m without changing it."""
    c = CONTROL.get(word & 0x7F)
    if c is None or (c.name in ("lw", "sw") and word >> 12 & 7 != 2):
        return None                                # outside the subset: lb, sh, ...
    if c.name == "R-type" and word >> 25 == 1:
        return None                                # mul, div: the M extension
    rd, rs1, rs2 = word >> 7 & 31, word >> 15 & 31, word >> 20 & 31
    a, b_reg = m.x[rs1], m.x[rs2]                  # the register file: two reads
    imm = imm_gen(word)
    b = imm & MASK if c.alu_src else b_reg         # the ALUSrc multiplexer
    if c.branch:
        taken = BRANCH[word >> 12 & 7](a, b_reg)
        return Effect(None, None, None, None, (pc + imm) & MASK if taken else pc + 4)
    result = ALU[alu_control(c, word)](a, b) & MASK
    mem_value = m.load(result, 4) if c.mem_read else (b_reg if c.mem_write else None)
    value = mem_value if c.mem_to_reg else result  # the MemtoReg multiplexer
    write = c.reg_write and rd != 0
    return Effect(rd if write else None, value if write else None,
                  result if c.mem_read or c.mem_write else None, mem_value, pc + 4)


def check(text, inputs=(), show=False, model=None):
    """Run text on rv, comparing the datapath's effect with rv's at every step."""
    model = model or cycle
    m = Machine(text, inputs=list(inputs))
    agree = outside = 0
    if show:
        names = ("ALUSrc", "MemtoReg", "RegWrite", "MemRead", "MemWrite", "Branch")
        print(f"{'instruction':<20} {'decoded':<7}" + "".join(f"{h:>9}" for h in names))
    while not m.halted:
        pc = m.pc
        instr = m.instruction_at(pc)[0]
        word = instr.word if instr else 0
        effect = model(m, pc, word)
        step = m.step()
        if effect is None:
            outside += 1
            if show:
                print(f"{step.text:<20} outside the model's subset")
            continue
        e = effect
        got = (e.rd, e.rd_value, e.mem_addr, e.mem_value, e.next_pc)
        want = (step.rd, step.rd_value, step.mem_addr, step.mem_value, step.next_pc)
        if got != want:
            raise AssertionError(f"{step.text}: datapath {got}, rv {want}")
        agree += 1
        if show:
            c = CONTROL[word & 0x7F]
            sig = (c.alu_src, c.mem_to_reg, c.reg_write, c.mem_read, c.mem_write,
                   c.branch)
            cells = "".join(f"{v:>9}" for v in sig)
            print(f"{step.text:<20} {c.name:<7}" + cells, " agrees")
    return agree, outside


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "four.S"
    with open(path) as f:
        agree, outside = check(f.read(), show=True)
    print(f"{agree} instructions agree with rv, {outside} outside the subset")
