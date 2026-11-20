"""The assembler of the book's RISC-V subset: two passes, labels, directives, pseudo-instructions."""
import re
from dataclasses import dataclass, field

from rv.isa import MASK, REGS, SPEC, EncodingError, encode, sext

TEXT_BASE = 0x00010000
DATA_BASE = 0x10000000

LABEL = re.compile(r"\s*([A-Za-z_.][A-Za-z0-9_.]*)\s*:")
NAME = re.compile(r"[A-Za-z_.][A-Za-z0-9_.]*$")
DIRECTIVES = {".text", ".data", ".globl", ".word", ".half", ".byte", ".asciz", ".space", ".align"}
BRANCH_PSEUDO = {"bgt": ("blt", True), "ble": ("bge", True), "bgtu": ("bltu", True),
                 "bleu": ("bgeu", True)}
ZERO_BRANCH = {"beqz": ("beq", False), "bnez": ("bne", False), "bgez": ("bge", False),
               "bltz": ("blt", False), "blez": ("bge", True), "bgtz": ("blt", True)}
PSEUDO = {"li", "la", "mv", "not", "neg", "nop", "j", "jr", "ret", "call", "tail", "seqz", "snez"} \
    | set(BRANCH_PSEUDO) | set(ZERO_BRANCH)


class AsmError(Exception):
    def __init__(self, name, line, text, msg):
        stmt = statement_text(text)
        where = f"line {line}: {stmt}: " if stmt else f"line {line}: "
        super().__init__(where + msg)
        self.name, self.line, self.text, self.msg = name, line, text, msg


@dataclass
class Program:
    """An assembled program. words[i] sits at text_base + 4*i; lines[i] = (line number, source line,
    True on the first word of its statement). data is placed at data_base."""
    name: str
    text_base: int
    words: list = field(default_factory=list)
    lines: list = field(default_factory=list)
    data_base: int = DATA_BASE
    data: bytearray = field(default_factory=bytearray)
    data_lines: list = field(default_factory=list)   # (address, length, line number, source line)
    symbols: dict = field(default_factory=dict)
    globls: list = field(default_factory=list)
    entry: int = TEXT_BASE

    def text_labels(self):
        """address -> the first label defined there, for labels in the text section."""
        out = {}
        end = self.text_base + 4 * len(self.words)
        for name, addr in self.symbols.items():
            if self.text_base <= addr < end and addr not in out:
                out[addr] = name
        return out

    def line_of(self, pc):
        i = (pc - self.text_base) >> 2
        if 0 <= i < len(self.lines) and (pc - self.text_base) % 4 == 0:
            return self.lines[i][0], self.lines[i][1]
        return None, ""


def _strip_comment(line):
    out, quote = [], None
    i = 0
    while i < len(line):
        c = line[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < len(line):
                out.append(line[i + 1])
                i += 1
            elif c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            out.append(c)
        elif c == "#":
            break
        else:
            out.append(c)
        i += 1
    return "".join(out)


def _split_operands(s):
    """Split on commas outside quotes."""
    parts, cur, quote = [], [], None
    i = 0
    while i < len(s):
        c = s[i]
        if quote:
            cur.append(c)
            if c == "\\" and i + 1 < len(s):
                cur.append(s[i + 1])
                i += 1
            elif c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            cur.append(c)
        elif c == ",":
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    if "".join(cur).strip() or parts:
        parts.append("".join(cur).strip())
    return parts


ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", "\\": "\\", '"': '"', "'": "'"}


def _unescape(body, err):
    out, i = [], 0
    while i < len(body):
        c = body[i]
        if c == "\\":
            if i + 1 >= len(body):
                raise err("a backslash ends the string")
            e = body[i + 1]
            if e in ESCAPES:
                out.append(ESCAPES[e])
                i += 2
            elif e == "x" and re.fullmatch(r"[0-9a-fA-F]{2}", body[i + 2:i + 4]):
                out.append(chr(int(body[i + 2:i + 4], 16)))
                i += 4
            else:
                raise err(f"unknown escape \\{e}")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def parse_number(tok, err):
    t = tok.strip()
    if len(t) >= 3 and t[0] == "'" and t[-1] == "'":
        s = _unescape(t[1:-1], err)
        if len(s) != 1:
            raise err(f"bad character {tok}")
        return ord(s)
    m = re.fullmatch(r"([+-]?)(0[xX][0-9a-fA-F_]+|0[bB][01_]+|[0-9][0-9_]*)", t)
    if not m:
        raise err(f"expected a number, found {tok!r}")
    v = int(m.group(2), 0)
    return -v if m.group(1) == "-" else v


class _Assembler:
    def __init__(self, text, name):
        self.name = name
        self.lines = text.splitlines()
        self.prog = Program(name=name, text_base=TEXT_BASE)
        self.lineno = 0
        self.src = ""

    def err(self, msg):
        return AsmError(self.name, self.lineno, self.src, msg)

    # ---- operands -------------------------------------------------------------------------------
    def reg(self, tok):
        r = REGS.get(tok.strip())
        if r is None:
            raise self.err(f"unknown register {tok.strip()!r}")
        return r

    def num(self, tok):
        return parse_number(tok, self.err)

    def mem(self, tok):
        m = re.fullmatch(r"\s*(.*?)\s*\(\s*([A-Za-z0-9]+)\s*\)\s*", tok)
        if not m:
            raise self.err(f"expected offset(register), found {tok.strip()!r}")
        off = self.num(m.group(1)) if m.group(1) else 0
        return off, self.reg(m.group(2))

    def symbol(self, tok, pass2):
        """label, label+n or label-n -> address (0 in pass 1)."""
        m = re.fullmatch(r"\s*([A-Za-z_.][A-Za-z0-9_.]*)\s*(?:([+-])\s*(\S+))?\s*", tok)
        if not m or m.group(1) in REGS:
            raise self.err(f"expected a label, found {tok.strip()!r}")
        if not pass2:
            return 0
        if m.group(1) not in self.prog.symbols:
            raise self.err(f"undefined label {m.group(1)!r}")
        v = self.prog.symbols[m.group(1)]
        if m.group(2):
            k = self.num(m.group(3))
            v = v + k if m.group(2) == "+" else v - k
        return v & MASK

    def value(self, tok, pass2):
        """A number or a label expression (.word)."""
        t = tok.strip()
        if re.match(r"[+-]?[0-9']", t):
            return self.num(t)
        return self.symbol(t, pass2)

    def count(self, ops, n, form):
        if len(ops) != n:
            raise self.err(f"expected {form}")

    # ---- pseudo-instructions --------------------------------------------------------------------
    @staticmethod
    def li_parts(v):
        """The real instructions of li: [('addi', imm)] or [('lui', hi)] or [('lui', hi), ('addi', lo)]."""
        sv = sext(v & MASK, 32)
        if -2048 <= sv <= 2047:
            return [("addi", sv)]
        hi = (((v & MASK) + 0x800) >> 12) & 0xFFFFF
        lo = sext(v & 0xFFF, 12)
        return [("lui", hi)] if lo == 0 else [("lui", hi), ("addi", lo)]

    def expand(self, mn, ops, pc, pass2):
        """-> list of (mnemonic, rd, rs1, rs2, imm) real instructions."""
        z, ra = 0, 1
        if mn == "li":
            self.count(ops, 2, "li rd, number")
            rd, v = self.reg(ops[0]), self.num(ops[1])
            if not -(1 << 31) <= v <= MASK:
                raise self.err(f"li: {v} does not fit in 32 bits")
            parts = self.li_parts(v)
            if parts[0][0] == "addi":
                return [("addi", rd, z, 0, parts[0][1])]
            out = [("lui", rd, 0, 0, parts[0][1])]
            if len(parts) == 2:
                out.append(("addi", rd, rd, 0, parts[1][1]))
            return out
        if mn == "la":
            self.count(ops, 2, "la rd, label")
            rd, t = self.reg(ops[0]), self.symbol(ops[1], pass2)
            off = (t - pc) & MASK
            hi = ((off + 0x800) >> 12) & 0xFFFFF
            lo = sext(off & 0xFFF, 12)
            return [("auipc", rd, 0, 0, hi), ("addi", rd, rd, 0, lo)]
        if mn == "mv":
            self.count(ops, 2, "mv rd, rs")
            return [("addi", self.reg(ops[0]), self.reg(ops[1]), 0, 0)]
        if mn == "not":
            self.count(ops, 2, "not rd, rs")
            return [("xori", self.reg(ops[0]), self.reg(ops[1]), 0, -1)]
        if mn == "neg":
            self.count(ops, 2, "neg rd, rs")
            return [("sub", self.reg(ops[0]), z, self.reg(ops[1]), 0)]
        if mn == "seqz":
            self.count(ops, 2, "seqz rd, rs")
            return [("sltiu", self.reg(ops[0]), self.reg(ops[1]), 0, 1)]
        if mn == "snez":
            self.count(ops, 2, "snez rd, rs")
            return [("sltu", self.reg(ops[0]), z, self.reg(ops[1]), 0)]
        if mn == "nop":
            self.count(ops, 0, "nop")
            return [("addi", z, z, 0, 0)]
        if mn in ("j", "call", "tail"):
            self.count(ops, 1, f"{mn} label")
            return [("jal", ra if mn == "call" else z, 0, 0, self.offset(ops[0], pc, pass2))]
        if mn == "jr":
            self.count(ops, 1, "jr rs")
            return [("jalr", z, self.reg(ops[0]), 0, 0)]
        if mn == "ret":
            self.count(ops, 0, "ret")
            return [("jalr", z, ra, 0, 0)]
        if mn in ZERO_BRANCH:
            real, swap = ZERO_BRANCH[mn]
            self.count(ops, 2, f"{mn} rs, label")
            r = self.reg(ops[0])
            a, b = (z, r) if swap else (r, z)
            return [(real, 0, a, b, self.offset(ops[1], pc, pass2))]
        if mn in BRANCH_PSEUDO:
            real, _ = BRANCH_PSEUDO[mn]
            self.count(ops, 3, f"{mn} rs, rt, label")
            return [(real, 0, self.reg(ops[1]), self.reg(ops[0]), self.offset(ops[2], pc, pass2))]
        raise AssertionError(mn)

    def offset(self, tok, pc, pass2):
        """A branch or jump target: a label expression, or an absolute address written as a number."""
        if re.match(r"\s*[+-]?[0-9]", tok):
            return sext(self.num(tok) - pc, 32) if pass2 else 0
        if not pass2:
            self.symbol(tok, False)
            return 0
        return sext(self.symbol(tok, True) - pc, 32)

    def real(self, mn, ops, pc, pass2):
        fmt, kind, *_ = SPEC[mn]
        if kind == "R":
            self.count(ops, 3, f"{mn} rd, rs1, rs2")
            return [(mn, self.reg(ops[0]), self.reg(ops[1]), self.reg(ops[2]), 0)]
        if kind in ("I", "SH"):
            self.count(ops, 3, f"{mn} rd, rs1, {'shamt' if kind == 'SH' else 'imm'}")
            return [(mn, self.reg(ops[0]), self.reg(ops[1]), 0, self.num(ops[2]))]
        if kind == "L":
            self.count(ops, 2, f"{mn} rd, offset(rs1)")
            off, base = self.mem(ops[1])
            return [(mn, self.reg(ops[0]), base, 0, off)]
        if kind == "S":
            self.count(ops, 2, f"{mn} rs2, offset(rs1)")
            off, base = self.mem(ops[1])
            return [(mn, 0, base, self.reg(ops[0]), off)]
        if kind == "B":
            self.count(ops, 3, f"{mn} rs1, rs2, label")
            return [(mn, 0, self.reg(ops[0]), self.reg(ops[1]), self.offset(ops[2], pc, pass2))]
        if kind == "U":
            self.count(ops, 2, f"{mn} rd, imm20")
            return [(mn, self.reg(ops[0]), 0, 0, self.num(ops[1]))]
        if kind == "J":
            if len(ops) == 1:
                return [("jal", 1, 0, 0, self.offset(ops[0], pc, pass2))]
            self.count(ops, 2, "jal rd, label")
            return [("jal", self.reg(ops[0]), 0, 0, self.offset(ops[1], pc, pass2))]
        if kind == "JR":
            if len(ops) == 1:
                return [("jalr", 1, self.reg(ops[0]), 0, 0)]
            if len(ops) == 2:
                off, base = self.mem(ops[1])
                return [("jalr", self.reg(ops[0]), base, 0, off)]
            self.count(ops, 3, "jalr rd, offset(rs1)")
            return [("jalr", self.reg(ops[0]), self.reg(ops[1]), 0, self.num(ops[2]))]
        self.count(ops, 0, mn)
        return [(mn, 0, 0, 0, 0)]

    def size(self, mn, ops):
        """Number of words of an instruction statement, known in pass 1."""
        if mn == "li":
            self.count(ops, 2, "li rd, number")
            return len(self.li_parts(self.num(ops[1])))
        return 2 if mn == "la" else 1

    # ---- the two passes -------------------------------------------------------------------------
    def statements(self):
        for i, raw in enumerate(self.lines, 1):
            self.lineno, self.src = i, raw
            line = _strip_comment(raw)
            labels = []
            while True:
                m = LABEL.match(line)
                if not m or m.group(1) in DIRECTIVES:
                    break
                labels.append(m.group(1))
                line = line[m.end():]
            stmt = line.strip()
            if not stmt:
                yield labels, None, []
                continue
            parts = stmt.split(None, 1)
            yield labels, parts[0].lower() if parts[0][0] != "." else parts[0], \
                _split_operands(parts[1]) if len(parts) > 1 else []

    def data_bytes(self, d, ops, pass2):
        if d in (".word", ".half", ".byte"):
            width = {".word": 4, ".half": 2, ".byte": 1}[d]
            if not ops:
                raise self.err(f"{d} needs at least one value")
            out = bytearray()
            for o in ops:
                v = self.value(o, pass2) if width == 4 else self.num(o)
                if not -(1 << (8 * width - 1)) <= v < (1 << (8 * width)):
                    raise self.err(f"{d}: {v} does not fit in {8 * width} bits")
                out += (v & ((1 << (8 * width)) - 1)).to_bytes(width, "little")
            return out
        if d == ".asciz":
            out = bytearray()
            if not ops:
                raise self.err(".asciz needs a string")
            for o in ops:
                if len(o) < 2 or o[0] != '"' or o[-1] != '"':
                    raise self.err(f'.asciz expects a string in double quotes, found {o!r}')
                out += _unescape(o[1:-1], self.err).encode("utf8") + b"\0"
            return out
        if d == ".space":
            self.count(ops, 1, ".space n")
            n = self.num(ops[0])
            if n < 0:
                raise self.err(".space: negative size")
            return bytearray(n)
        raise AssertionError(d)

    def run_pass(self, pass2):
        text_pc, data_pc, section = TEXT_BASE, DATA_BASE, ".text"
        for labels, mn, ops in self.statements():
            for lab in labels:
                if not pass2:
                    if lab in self.prog.symbols:
                        raise self.err(f"label {lab!r} defined twice")
                    self.prog.symbols[lab] = text_pc if section == ".text" else data_pc
            if mn is None:
                continue
            if mn.startswith("."):
                if mn not in DIRECTIVES:
                    raise self.err(f"unknown directive {mn}")
                if mn in (".text", ".data"):
                    self.count(ops, 0, mn)
                    section = mn
                    continue
                if mn == ".globl":
                    self.count(ops, 1, ".globl name")
                    if not pass2:
                        self.prog.globls.append(ops[0])
                    continue
                if mn == ".align":
                    self.count(ops, 1, ".align n")
                    n = self.num(ops[0])
                    if not 0 <= n <= 12:
                        raise self.err(".align n needs 0 <= n <= 12")
                    step = 1 << n
                    if section == ".text":
                        if step < 4:
                            continue
                        while text_pc % step:
                            if pass2:
                                self.emit(encode("addi"), first=False)
                            text_pc += 4
                    else:
                        pad = (-data_pc) % step
                        if pass2 and pad:
                            self.prog.data += bytearray(pad)
                        data_pc += pad
                    continue
                if section == ".text":
                    if mn != ".word":
                        raise self.err(f"{mn} belongs in .data (only .word and .align may appear in .text)")
                    data = self.data_bytes(mn, ops, pass2)
                    for k in range(0, len(data), 4):
                        if pass2:
                            self.emit(int.from_bytes(data[k:k + 4], "little"), first=(k == 0))
                        text_pc += 4
                    continue
                data = self.data_bytes(mn, ops, pass2)
                if pass2:
                    self.prog.data_lines.append((data_pc, len(data), self.lineno, self.src))
                    self.prog.data += data
                data_pc += len(data)
                continue
            if section != ".text":
                raise self.err(f"instruction {mn!r} in the .data section")
            if mn not in SPEC and mn not in PSEUDO:
                raise self.err(f"unknown instruction {mn!r}")
            if not pass2:
                text_pc += 4 * self.size(mn, ops)
                continue
            reals = self.expand(mn, ops, text_pc, True) if mn in PSEUDO else self.real(mn, ops, text_pc, True)
            for k, (rm, rd, rs1, rs2, imm) in enumerate(reals):
                try:
                    self.emit(encode(rm, rd, rs1, rs2, imm), first=(k == 0))
                except EncodingError as e:
                    raise self.err(str(e)) from None
            text_pc += 4 * len(reals)

    def emit(self, word, first):
        self.prog.words.append(word)
        self.prog.lines.append((self.lineno, self.src, first))

    def assemble(self):
        self.run_pass(False)
        self.run_pass(True)
        main = self.prog.symbols.get("main")
        if main is not None and TEXT_BASE <= main < TEXT_BASE + 4 * len(self.prog.words):
            self.prog.entry = main
        return self.prog


def assemble(text, name="<input>"):
    """Assemble source text into a Program. Raises AsmError with the line number."""
    return _Assembler(text, name).assemble()


def statement_text(src, labels=False):
    """A source line without its comment and (unless labels=True) its labels:
    '  loop: lw a0, 0(a1)  # x' -> 'lw a0, 0(a1)'."""
    line = _strip_comment(src)
    while not labels:
        m = LABEL.match(line)
        if not m or m.group(1) in DIRECTIVES:
            break
        line = line[m.end():]
    return " ".join(line.split()) if '"' not in line else line.strip()
