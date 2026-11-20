"""The instruction set of the book's RISC-V subset: RV32I (user level) and RV32M.

Encodings follow the RISC-V Unprivileged ISA specification (formats R, I, S, B, U, J), as listed in
RISC-V International's riscv-opcodes tables (extensions/rv_i, rv32_i, rv_m). See RV.md.
"""
from dataclasses import dataclass

MASK = 0xFFFFFFFF

ABI = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1",
       "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7",
       "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11",
       "t3", "t4", "t5", "t6"]
REGS = {f"x{i}": i for i in range(32)} | {name: i for i, name in enumerate(ABI)} | {"fp": 8}

# major opcodes
LUI, AUIPC, JAL, JALR, BRANCH, LOAD, STORE, OP_IMM, OP, SYSTEM = (
    0x37, 0x17, 0x6F, 0x67, 0x63, 0x03, 0x23, 0x13, 0x33, 0x73)

# mnemonic -> (format, operand kind, opcode, funct3, funct7)
#   kinds: R "rd, rs1, rs2"; I "rd, rs1, imm"; SH "rd, rs1, shamt"; L "rd, imm(rs1)"; S "rs2, imm(rs1)";
#          B "rs1, rs2, label"; U "rd, imm20"; J "rd, label"; JR (jalr) ; N (no operand)
SPEC = {
    "lui": ("U", "U", LUI, None, None),
    "auipc": ("U", "U", AUIPC, None, None),
    "jal": ("J", "J", JAL, None, None),
    "jalr": ("I", "JR", JALR, 0, None),
    "beq": ("B", "B", BRANCH, 0, None), "bne": ("B", "B", BRANCH, 1, None),
    "blt": ("B", "B", BRANCH, 4, None), "bge": ("B", "B", BRANCH, 5, None),
    "bltu": ("B", "B", BRANCH, 6, None), "bgeu": ("B", "B", BRANCH, 7, None),
    "lb": ("I", "L", LOAD, 0, None), "lh": ("I", "L", LOAD, 1, None), "lw": ("I", "L", LOAD, 2, None),
    "lbu": ("I", "L", LOAD, 4, None), "lhu": ("I", "L", LOAD, 5, None),
    "sb": ("S", "S", STORE, 0, None), "sh": ("S", "S", STORE, 1, None), "sw": ("S", "S", STORE, 2, None),
    "addi": ("I", "I", OP_IMM, 0, None), "slti": ("I", "I", OP_IMM, 2, None),
    "sltiu": ("I", "I", OP_IMM, 3, None), "xori": ("I", "I", OP_IMM, 4, None),
    "ori": ("I", "I", OP_IMM, 6, None), "andi": ("I", "I", OP_IMM, 7, None),
    "slli": ("I", "SH", OP_IMM, 1, 0x00), "srli": ("I", "SH", OP_IMM, 5, 0x00),
    "srai": ("I", "SH", OP_IMM, 5, 0x20),
    "add": ("R", "R", OP, 0, 0x00), "sub": ("R", "R", OP, 0, 0x20), "sll": ("R", "R", OP, 1, 0x00),
    "slt": ("R", "R", OP, 2, 0x00), "sltu": ("R", "R", OP, 3, 0x00), "xor": ("R", "R", OP, 4, 0x00),
    "srl": ("R", "R", OP, 5, 0x00), "sra": ("R", "R", OP, 5, 0x20), "or": ("R", "R", OP, 6, 0x00),
    "and": ("R", "R", OP, 7, 0x00),
    "mul": ("R", "R", OP, 0, 0x01), "mulh": ("R", "R", OP, 1, 0x01), "mulhsu": ("R", "R", OP, 2, 0x01),
    "mulhu": ("R", "R", OP, 3, 0x01), "div": ("R", "R", OP, 4, 0x01), "divu": ("R", "R", OP, 5, 0x01),
    "rem": ("R", "R", OP, 6, 0x01), "remu": ("R", "R", OP, 7, 0x01),
    "ecall": ("I", "N", SYSTEM, 0, None),
    "ebreak": ("I", "N", SYSTEM, 0, None),
}

_R = {(spec[3], spec[4]): name for name, spec in SPEC.items() if spec[2] == OP}
_I = {spec[3]: name for name, spec in SPEC.items() if spec[2] == OP_IMM and spec[1] == "I"}
_BR = {spec[3]: name for name, spec in SPEC.items() if spec[2] == BRANCH}
_LD = {spec[3]: name for name, spec in SPEC.items() if spec[2] == LOAD}
_ST = {spec[3]: name for name, spec in SPEC.items() if spec[2] == STORE}


def sext(value, bits):
    """Read the low `bits` bits of value as a two's-complement number."""
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def signed(value):
    return sext(value, 32)


class EncodingError(ValueError):
    pass


def _check(value, lo, hi, what):
    if not lo <= value <= hi:
        raise EncodingError(f"{what} {value} out of range {lo}..{hi}")


def encode(mnemonic, rd=0, rs1=0, rs2=0, imm=0):
    """The 32-bit word of one instruction. imm is the immediate as the instruction reads it: a signed
    number for I, S, B, J (B and J: a byte offset, even), the 20-bit field for U, the shift amount for
    shifts."""
    fmt, kind, op, f3, f7 = SPEC[mnemonic]
    for r in (rd, rs1, rs2):
        _check(r, 0, 31, "register")
    if fmt == "R":
        return f7 << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op
    if fmt == "I":
        if kind == "N":
            return (1 if mnemonic == "ebreak" else 0) << 20 | op
        if kind == "SH":
            _check(imm, 0, 31, "shift amount")
            return (f7 << 5 | imm) << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op
        _check(imm, -2048, 2047, "immediate")
        return (imm & 0xFFF) << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op
    if fmt == "S":
        _check(imm, -2048, 2047, "offset")
        u = imm & 0xFFF
        return (u >> 5) << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | (u & 0x1F) << 7 | op
    if fmt == "B":
        _check(imm, -4096, 4094, "branch offset")
        if imm & 1:
            raise EncodingError(f"branch offset {imm} is odd")
        u = imm & 0x1FFF
        return ((u >> 12) & 1) << 31 | ((u >> 5) & 0x3F) << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 \
            | ((u >> 1) & 0xF) << 8 | ((u >> 11) & 1) << 7 | op
    if fmt == "U":
        _check(imm, 0, 0xFFFFF, "upper immediate")
        return imm << 12 | rd << 7 | op
    if fmt == "J":
        _check(imm, -(1 << 20), (1 << 20) - 2, "jump offset")
        if imm & 1:
            raise EncodingError(f"jump offset {imm} is odd")
        u = imm & 0x1FFFFF
        return ((u >> 20) & 1) << 31 | ((u >> 1) & 0x3FF) << 21 | ((u >> 11) & 1) << 20 \
            | ((u >> 12) & 0xFF) << 12 | rd << 7 | op
    raise AssertionError(fmt)


@dataclass(frozen=True, slots=True)
class Instr:
    """A decoded instruction. imm: signed for I/S/B/J, the 20-bit field for U, the shift amount for
    shifts, None when the format has none."""
    mnemonic: str
    fmt: str
    rd: int
    rs1: int
    rs2: int
    imm: int | None
    word: int


def decode(word):
    """Decode a 32-bit word; None if it is not an instruction of the subset."""
    word &= MASK
    op = word & 0x7F
    rd = (word >> 7) & 31
    f3 = (word >> 12) & 7
    rs1 = (word >> 15) & 31
    rs2 = (word >> 20) & 31
    f7 = word >> 25
    imm_i = sext(word >> 20, 12)
    if op == OP:
        name = _R.get((f3, f7))
        return name and Instr(name, "R", rd, rs1, rs2, None, word)
    if op == OP_IMM:
        if f3 == 1:
            return Instr("slli", "I", rd, rs1, 0, rs2, word) if f7 == 0 else None
        if f3 == 5:
            name = {0x00: "srli", 0x20: "srai"}.get(f7)
            return name and Instr(name, "I", rd, rs1, 0, rs2, word)
        return Instr(_I[f3], "I", rd, rs1, 0, imm_i, word)
    if op == LOAD:
        name = _LD.get(f3)
        return name and Instr(name, "I", rd, rs1, 0, imm_i, word)
    if op == STORE:
        name = _ST.get(f3)
        imm = sext((f7 << 5) | rd, 12)
        return name and Instr(name, "S", 0, rs1, rs2, imm, word)
    if op == BRANCH:
        name = _BR.get(f3)
        imm = sext(((word >> 31) & 1) << 12 | ((word >> 7) & 1) << 11 | ((word >> 25) & 0x3F) << 5
                   | ((word >> 8) & 0xF) << 1, 13)
        return name and Instr(name, "B", 0, rs1, rs2, imm, word)
    if op in (LUI, AUIPC):
        return Instr("lui" if op == LUI else "auipc", "U", rd, 0, 0, word >> 12, word)
    if op == JAL:
        imm = sext(((word >> 31) & 1) << 20 | ((word >> 12) & 0xFF) << 12 | ((word >> 20) & 1) << 11
                   | ((word >> 21) & 0x3FF) << 1, 21)
        return Instr("jal", "J", rd, 0, 0, imm, word)
    if op == JALR:
        return Instr("jalr", "I", rd, rs1, 0, imm_i, word) if f3 == 0 else None
    if op == SYSTEM and f3 == 0 and rd == 0 and rs1 == 0:
        if word >> 20 == 0:
            return Instr("ecall", "I", 0, 0, 0, None, word)
        if word >> 20 == 1:
            return Instr("ebreak", "I", 0, 0, 0, None, word)
    return None


def disassemble(word, pc=None, symbols=None):
    """Canonical text of a word: ABI register names, decimal immediates, branch and jump targets as
    absolute addresses (or a label from `symbols`, a dict address -> name) when pc is known. Only real
    instructions are printed, never pseudo-instructions."""
    ins = decode(word)
    if ins is None:
        return f".word 0x{word & MASK:08x}"
    n, r = ins.mnemonic, ABI

    def target(off):
        if pc is None:
            return f"{off:+d}"
        t = (pc + off) & MASK
        return symbols[t] if symbols and t in symbols else f"0x{t:08x}"

    kind = SPEC[n][1]
    if kind == "R":
        return f"{n} {r[ins.rd]}, {r[ins.rs1]}, {r[ins.rs2]}"
    if kind in ("I", "SH"):
        return f"{n} {r[ins.rd]}, {r[ins.rs1]}, {ins.imm}"
    if kind in ("L", "JR"):
        return f"{n} {r[ins.rd]}, {ins.imm}({r[ins.rs1]})"
    if kind == "S":
        return f"{n} {r[ins.rs2]}, {ins.imm}({r[ins.rs1]})"
    if kind == "B":
        return f"{n} {r[ins.rs1]}, {r[ins.rs2]}, {target(ins.imm)}"
    if kind == "U":
        return f"{n} {r[ins.rd]}, 0x{ins.imm:x}"
    if kind == "J":
        return f"{n} {r[ins.rd]}, {target(ins.imm)}"
    return n


def fields(word):
    """The word split into its format's fields, in binary, e.g. 'R  f7=0000000 rs2=01100 ...'."""
    ins = decode(word)
    b = f"{word & MASK:032b}"
    if ins is None:
        return "?  " + b
    f = ins.fmt
    if f == "R":
        parts = [("f7", b[0:7]), ("rs2", b[7:12]), ("rs1", b[12:17]), ("f3", b[17:20]), ("rd", b[20:25])]
    elif f == "I":
        parts = [("imm", b[0:12]), ("rs1", b[12:17]), ("f3", b[17:20]), ("rd", b[20:25])]
    elif f == "S":
        parts = [("imm[11:5]", b[0:7]), ("rs2", b[7:12]), ("rs1", b[12:17]), ("f3", b[17:20]),
                 ("imm[4:0]", b[20:25])]
    elif f == "B":
        parts = [("imm[12|10:5]", b[0:7]), ("rs2", b[7:12]), ("rs1", b[12:17]), ("f3", b[17:20]),
                 ("imm[4:1|11]", b[20:25])]
    elif f == "U":
        parts = [("imm[31:12]", b[0:20]), ("rd", b[20:25])]
    else:
        parts = [("imm[20|10:1|11|19:12]", b[0:20]), ("rd", b[20:25])]
    return f"{f}  " + " ".join(f"{k}={v}" for k, v in parts) + f" op={b[25:32]}"
