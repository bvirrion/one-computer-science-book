"""The series' toy machine: an assembler and a simulator (spec in TOYMACHINE.md, frozen)."""
import re

OPS = [
    # (mnemonic, operand kind): r = register in byte 0; s = second register in byte 1;
    # n = number in byte 1; a = address in byte 1 ([a] in assembly for LOAD/STORE)
    ("HALT", ""), ("LOADI", "rn"), ("LOAD", "r[a]"), ("STORE", "r[a]"), ("ADD", "rs"),
    ("SUB", "rs"), ("ADDI", "rn"), ("AND", "rs"), ("OR", "rs"), ("XOR", "rs"), ("NOT", "r"),
    ("SHL", "r"), ("SHR", "r"), ("CMP", "rs"), ("JMP", "a"), ("JZ", "a"), ("JNZ", "a"),
    ("JN", "a"), ("JC", "a"), ("IN", "r"), ("OUT", "r"), ("LOADR", "rs"), ("STORER", "rs"),
    ("PUSH", "r"), ("POP", "r"), ("CALL", "a"), ("RET", ""), ("NOP", ""),
]
OPCODE = {name: i for i, (name, _) in enumerate(OPS)}
KIND = dict(OPS)
MEMSIZE = 256


class ToyError(Exception):
    """An error in a program, with the line it comes from."""


def _number(tok, labels=None, line=0):
    tok = tok.strip()
    if labels is not None and re.fullmatch(r"[A-Za-z_]\w*", tok) and not re.fullmatch(r"[Rr][0-3]", tok):
        if tok not in labels:
            raise ToyError(f"line {line}: label {tok!r} is used but not defined")
        return labels[tok]
    m = re.fullmatch(r"'(.)'", tok)
    if m:
        v = ord(m.group(1))
    else:
        try:
            v = int(tok, 0)
        except ValueError:
            raise ToyError(f"line {line}: {tok!r} is not a number") from None
    if not -128 <= v <= 255:
        raise ToyError(f"line {line}: {v} does not fit in one byte (-128 to 255)")
    return v % 256


def _register(tok, line):
    m = re.fullmatch(r"[Rr]([0-3])", tok.strip())
    if not m:
        raise ToyError(f"line {line}: {tok.strip()!r} is not a register (R0 to R3)")
    return int(m.group(1))


def _split(text):
    """[(line number, label or None, mnemonic or None, operands, source line)]"""
    out = []
    for n, raw in enumerate(text.splitlines(), start=1):
        src = raw.rstrip()
        code = re.sub(r";.*", "", raw.replace("';'", "59")).strip()
        label = None
        m = re.match(r"([A-Za-z_]\w*)\s*:\s*(.*)$", code)
        if m:
            label, code = m.group(1), m.group(2).strip()
        if not code:
            out.append((n, label, None, [], src))
            continue
        parts = code.split(None, 1)
        mnem = parts[0].upper()
        ops = [o.strip() for o in parts[1].split(",")] if len(parts) > 1 else []
        out.append((n, label, mnem, ops, src))
    return out


def _size(mnem, ops, line):
    if mnem == "DATA":
        if not ops:
            raise ToyError(f"line {line}: DATA needs at least one number")
        return len(ops)
    if mnem not in OPCODE:
        raise ToyError(f"line {line}: unknown instruction {mnem!r}")
    return 2


def assemble_lines(text):
    """[(address, [bytes], line number, source line)] for every line that places bytes."""
    rows = _split(text)
    labels, addr = {}, 0
    for n, label, mnem, ops, _ in rows:
        if label:
            if label in labels:
                raise ToyError(f"line {n}: label {label!r} is defined twice")
            labels[label] = addr
        if mnem:
            addr += _size(mnem, ops, n)
    if addr > MEMSIZE:
        raise ToyError(f"the program needs {addr} bytes; the memory has {MEMSIZE}")
    out, addr = [], 0
    for n, _label, mnem, ops, src in rows:
        if not mnem:
            continue
        if mnem == "DATA":
            bs = [_number(o, labels, n) for o in ops]
        else:
            kind = KIND[mnem]
            want = {"": 0, "r": 1, "a": 1, "rn": 2, "rs": 2, "r[a]": 2}[kind]
            if len(ops) != want:
                raise ToyError(f"line {n}: {mnem} takes {want} operand(s), got {len(ops)}")
            r = _register(ops[0], n) if kind.startswith("r") else 0
            b1 = 0
            if kind == "rn":
                b1 = _number(ops[1], labels, n)
            elif kind == "rs":
                b1 = _register(ops[1], n)
            elif kind == "r[a]":
                m = re.fullmatch(r"\[(.+)\]", ops[1])
                if not m:
                    raise ToyError(f"line {n}: {mnem} wants an address in brackets, like [20]")
                b1 = _number(m.group(1), labels, n)
            elif kind == "a":
                b1 = _number(ops[0], labels, n)
            bs = [4 * OPCODE[mnem] + r, b1]
        out.append((addr, bs, n, src))
        addr += len(bs)
    return out


def assemble(text):
    """The 256 bytes of memory holding the program, from address 0."""
    mem = [0] * MEMSIZE
    for addr, bs, _n, _src in assemble_lines(text):
        mem[addr:addr + len(bs)] = bs
    return mem


def disassemble(b0, b1):
    op, r = b0 // 4, b0 % 4
    if op >= len(OPS):
        return f"?? ({b0} {b1})"
    name, kind = OPS[op]
    if kind == "":
        return name
    if kind == "r":
        return f"{name} R{r}"
    if kind == "a":
        return f"{name} {b1}"
    if kind == "rn":
        return f"{name} R{r}, {b1}"
    if kind == "r[a]":
        return f"{name} R{r}, [{b1}]"
    return f"{name} R{r}, R{b1 % 4}"


class Machine:
    def __init__(self, mem, inputs=()):
        if len(mem) > MEMSIZE:
            raise ToyError("a program larger than the memory")
        self.mem = list(mem) + [0] * (MEMSIZE - len(mem))
        self.reg = [0, 0, 0, 0]
        self.pc = 0
        self.sp = 0
        self.flags = {"Z": 0, "N": 0, "C": 0}
        self.inputs = list(inputs)
        self.outputs = []
        self.halted = False
        self.steps = 0
        self.on_output = None
        self.read_input = None

    def _set(self, value, carry=0):
        v = value % 256
        self.flags = {"Z": int(v == 0), "N": int(v >= 128), "C": int(carry)}
        return v

    def current(self):
        return disassemble(self.mem[self.pc], self.mem[(self.pc + 1) % MEMSIZE])

    def step(self):
        if self.halted:
            return
        if self.pc > MEMSIZE - 2:
            raise ToyError(f"PC = {self.pc}: past the end of memory")
        b0, b1 = self.mem[self.pc], self.mem[self.pc + 1]
        self.pc += 2
        self.steps += 1
        op, r = b0 // 4, b0 % 4
        if op >= len(OPS):
            raise ToyError(f"no instruction has operation code {op} (address {self.pc - 2})")
        name = OPS[op][0]
        R = self.reg
        s = b1 % 4
        if name == "HALT":
            self.halted = True
            self.pc -= 2
        elif name == "LOADI":
            R[r] = b1
        elif name == "LOAD":
            R[r] = self.mem[b1]
        elif name == "STORE":
            self.mem[b1] = R[r]
        elif name == "ADD":
            t = R[r] + R[s]
            R[r] = self._set(t, t > 255)
        elif name == "ADDI":
            t = R[r] + b1
            R[r] = self._set(t, t > 255)
        elif name == "SUB":
            R[r] = self._set(R[r] - R[s], R[r] < R[s])
        elif name == "CMP":
            self._set(R[r] - R[s], R[r] < R[s])
        elif name == "AND":
            R[r] = self._set(R[r] & R[s])
        elif name == "OR":
            R[r] = self._set(R[r] | R[s])
        elif name == "XOR":
            R[r] = self._set(R[r] ^ R[s])
        elif name == "NOT":
            R[r] = self._set(~R[r] & 255)
        elif name == "SHL":
            R[r] = self._set(R[r] << 1, R[r] >> 7)
        elif name == "SHR":
            R[r] = self._set(R[r] >> 1, R[r] & 1)
        elif name == "JMP":
            self.pc = b1
        elif name == "JZ":
            self.pc = b1 if self.flags["Z"] else self.pc
        elif name == "JNZ":
            self.pc = b1 if not self.flags["Z"] else self.pc
        elif name == "JN":
            self.pc = b1 if self.flags["N"] else self.pc
        elif name == "JC":
            self.pc = b1 if self.flags["C"] else self.pc
        elif name == "IN":
            if self.inputs:
                v = self.inputs.pop(0)
            elif self.read_input:
                v = self.read_input()
            else:
                raise ToyError("IN: no input left")
            if not -128 <= v <= 255:
                raise ToyError(f"IN: {v} does not fit in one byte")
            R[r] = v % 256
        elif name == "OUT":
            self.outputs.append(R[r])
            if self.on_output:
                self.on_output(R[r])
        elif name == "LOADR":
            R[r] = self.mem[R[s]]
        elif name == "STORER":
            self.mem[R[s]] = R[r]
        elif name == "PUSH":
            self.sp = (self.sp - 1) % 256
            self.mem[self.sp] = R[r]
        elif name == "POP":
            R[r] = self.mem[self.sp]
            self.sp = (self.sp + 1) % 256
        elif name == "CALL":
            self.sp = (self.sp - 1) % 256
            self.mem[self.sp] = self.pc
            self.pc = b1
        elif name == "RET":
            self.pc = self.mem[self.sp]
            self.sp = (self.sp + 1) % 256

    def run(self, max_steps=10_000, trace=None):
        while not self.halted:
            if self.steps >= max_steps:
                raise ToyError(f"no HALT after {max_steps} steps")
            if trace:
                trace(self)
            self.step()
        return self.outputs
