"""datapath_more.py: lui, jal and jalr in the single-cycle datapath (ex. 3 and 12)."""
from datapath import MASK, Effect, cycle, sext

# New signals: a_zero (the ALU's first input is 0, not rs1), pc4 (rd gets pc + 4), jump
# ("jal": the next pc is pc + imm; "jalr": the ALU result with bit 0 cleared).
MORE = {
    0b0110111: dict(name="lui", alu_src=1, reg_write=1, a_zero=1, pc4=0, jump=None),
    0b1101111: dict(name="jal", alu_src=1, reg_write=1, a_zero=0, pc4=1, jump="jal"),
    0b1100111: dict(name="jalr", alu_src=1, reg_write=1, a_zero=0, pc4=1, jump="jalr"),
}


def imm_more(word):
    op = word & 0x7F
    if op == 0b0110111:          # U: the upper 20 bits
        return word & 0xFFFFF000
    if op == 0b1101111:          # J
        return sext((word >> 31) << 20 | (word >> 12 & 0xFF) << 12
                    | (word >> 20 & 1) << 11 | (word >> 21 & 0x3FF) << 1, 21)
    return sext(word >> 20, 12)  # jalr: I


def cycle_more(m, pc, word):
    c = MORE.get(word & 0x7F)
    if c is None:
        return cycle(m, pc, word)
    rd, rs1 = word >> 7 & 31, word >> 15 & 31
    imm = imm_more(word)
    a = 0 if c["a_zero"] else m.x[rs1]
    result = (a + imm) & MASK  # the ALU adds
    if c["jump"] == "jal":
        next_pc = (pc + imm) & MASK
    elif c["jump"] == "jalr":
        next_pc = result & ~1
    else:
        next_pc = pc + 4
    value = pc + 4 if c["pc4"] else result
    write = rd != 0
    return Effect(rd if write else None, value if write else None, None, None, next_pc)
