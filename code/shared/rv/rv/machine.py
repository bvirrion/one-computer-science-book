"""The machine: registers, memory regions, one step at a time, system calls by ecall. See RV.md."""
import sys
from dataclasses import dataclass

from rv.asm import Program, assemble
from rv.isa import ABI, MASK, REGS, decode, disassemble, sext

EXIT_ADDR = 0xFFFF0000          # ra at start: a jump here ends the program with status a0 & 0xff
STACK_TOP = 0x80000000
STACK_SIZE = 8 << 20
SP_START = 0x7FFFFFF0           # 16-byte aligned, as the calling convention requires
HEAP_MAX = 16 << 20
SIZE_NAME = {1: "byte", 2: "half", 4: "word"}
ECALL_NAMES = {1: "print int", 4: "print string", 5: "read int", 9: "sbrk", 10: "exit",
               11: "print char", 93: "exit with code"}


class RVFault(Exception):
    """The program did something the machine refuses: pc is the address of the instruction."""

    def __init__(self, msg, pc=None):
        super().__init__(msg)
        self.msg, self.pc = msg, pc


class StepLimit(RVFault):
    pass


@dataclass(slots=True)
class Step:
    """What one instruction did. rd is None when no register changed (x0 never appears, nor in srcs);
    mem_kind is 'load', 'store' or None; branch_taken is None except for conditional branches; ecall is
    the a7 number of an ecall."""
    pc: int
    word: int
    text: str
    kind: str              # alu, muldiv, load, store, branch, jump, system
    rd: int | None
    rd_value: int | None   # unsigned 32-bit
    srcs: tuple
    mem_kind: str | None
    mem_addr: int | None
    mem_size: int | None
    mem_value: int | None  # the value loaded (after extension) or stored (after truncation), unsigned
    branch_taken: bool | None
    next_pc: int
    ecall: int | None
    trap: str | None = None   # 'ecall', 'ebreak' or 'illegal' when on_trap handled the instruction


def _fmt(v):
    s = sext(v, 32)
    return str(s) if -65536 < s < 65536 else f"0x{v & MASK:08x}"


class Memory:
    """Three regions: text (read-only, from text_base), data + heap (from data_base up to the break),
    stack (8 MiB below 0x80000000). Every other address faults. Little-endian."""

    def __init__(self, prog):
        self.text_base = prog.text_base
        self.text = bytes(b"".join(w.to_bytes(4, "little") for w in prog.words))
        self.text_end = self.text_base + len(self.text)
        self.data_base = prog.data_base
        self.heap_start = (prog.data_base + len(prog.data) + 15) & ~15
        self.brk = self.heap_start
        self.data = bytearray(prog.data) + bytearray(self.heap_start - prog.data_base - len(prog.data))
        self.stack_base = STACK_TOP - STACK_SIZE
        self.stack = bytearray(STACK_SIZE)

    def _where(self, addr, size, write):
        if self.data_base <= addr and addr + size <= self.brk:
            return self.data, addr - self.data_base
        if self.stack_base <= addr and addr + size <= STACK_TOP:
            return self.stack, addr - self.stack_base
        if self.text_base <= addr and addr + size <= self.text_end:
            if write:
                raise RVFault(f"store to the read-only text at 0x{addr:08x}")
            return self.text, addr - self.text_base
        raise RVFault(f"{'store' if write else 'load'} access fault at 0x{addr:08x}")

    def load(self, addr, size):
        if addr % size:
            raise RVFault(f"misaligned {SIZE_NAME[size]} load at 0x{addr:08x}")
        buf, off = self._where(addr, size, False)
        return int.from_bytes(buf[off:off + size], "little")

    def store(self, addr, size, value):
        if addr % size:
            raise RVFault(f"misaligned {SIZE_NAME[size]} store at 0x{addr:08x}")
        buf, off = self._where(addr, size, True)
        buf[off:off + size] = (value & ((1 << (8 * size)) - 1)).to_bytes(size, "little")

    def sbrk(self, n):
        """Move the break by n bytes rounded up to a multiple of 4; the old break, or -1 if refused."""
        n = (n + 3) & ~3
        new = self.brk + n
        if new < self.heap_start or new - self.heap_start > HEAP_MAX:
            return MASK
        old = self.brk
        if new > old:
            self.data += bytearray(new - old)
        else:
            del self.data[new - self.data_base:]
        self.brk = new
        return old


class Machine:
    """Machine(prog or source text, inputs=[...] or stdin=file, out=file, echo=False).

    x[i] holds register i as an unsigned 32-bit number (reg('a0') gives it signed). Output is collected
    in .output and also written to `out` if given. ecall 5 reads from `inputs` (numbers or strings) or,
    without it, a line of `stdin`; with echo=True the line read is written to the output, as a terminal
    shows what is typed. The system-call table is .ecalls (number -> function(machine)): add or replace
    entries, or set .on_ecall(machine, number) -> True for numbers not in it, and .on_ebreak(machine)
    for ebreak; without a handler both stop the machine with an RVFault. These handlers run inside the
    instruction, and the machine then goes on to the next one. For a precise trap instead, set
    .on_trap(machine, cause): every ecall, ebreak and undecodable word ('ecall', 'ebreak', 'illegal')
    then calls it with .pc still at that instruction, and execution resumes at whatever .pc the handler
    leaves (a handler that forgets pc += 4 runs the same instruction again)."""

    def __init__(self, prog, inputs=None, stdin=None, out=None, echo=False):
        if isinstance(prog, str):
            prog = assemble(prog)
        self.prog: Program = prog
        self.mem = Memory(prog)
        self.code = [decode(w) for w in prog.words]
        self.labels = prog.text_labels()
        self.texts = [disassemble(w, prog.text_base + 4 * i, self.labels) for i, w in enumerate(prog.words)]
        self.x = [0] * 32
        self.x[1] = EXIT_ADDR
        self.x[2] = SP_START
        self.pc = prog.entry
        self.steps = 0
        self.halted = False
        self.exit_code = None
        self.output = []
        self.out = out
        self.inputs = None if inputs is None else iter(inputs)
        self.stdin = stdin if stdin is not None else (sys.stdin if inputs is None else None)
        self.echo = echo
        self.stats = {"instructions": 0, "loads": 0, "stores": 0, "branches": 0, "taken": 0,
                      "jumps": 0, "ecalls": 0}
        self.ecalls = {1: _print_int, 4: _print_string, 5: _read_int, 9: _sbrk, 10: _exit0,
                       11: _print_char, 93: _exit_code}
        self.on_ecall = None
        self.on_ebreak = None
        self.on_trap = None
        self.traps = 0
        self.column = 0       # characters written since the last newline (for --trace layout)

    # ---- helpers for system calls and hooks ------------------------------------------------------
    def reg(self, name):
        i = name if isinstance(name, int) else REGS[name]
        return sext(self.x[i], 32)

    def set_reg(self, i, value):
        if i:
            self.x[i] = value & MASK

    def write(self, text):
        if not text:
            return
        self.output.append(text)
        if self.out is not None:
            self.out.write(text)
            self.out.flush()
        nl = text.rfind("\n")
        self.column = len(text) - nl - 1 if nl >= 0 else self.column + len(text)

    @property
    def output_text(self):
        return "".join(self.output)

    def read_string(self, addr):
        out = bytearray()
        while True:
            b = self.mem.load(addr, 1)
            if b == 0:
                return out.decode("utf8", errors="replace")
            out.append(b)
            addr = (addr + 1) & MASK
            if len(out) > HEAP_MAX:
                raise RVFault("print string: no NUL byte found")

    def read_line(self):
        if self.inputs is not None:
            item = next(self.inputs, None)
            if item is None:
                raise RVFault("read int: no input left")
            line = f"{item}\n"
        else:
            line = self.stdin.readline() if self.stdin is not None else ""
            if not line:
                raise RVFault("read int: no input left")
        if self.echo:
            self.write(line if line.endswith("\n") else line + "\n")
        return line

    def halt(self, code):
        self.halted = True
        self.exit_code = code & 0xFF

    def load(self, addr, size, signed=False):
        v = self.mem.load(addr & MASK, size)
        return sext(v, 8 * size) & MASK if signed else v

    def store(self, addr, size, value):
        self.mem.store(addr & MASK, size, value)

    def instruction_at(self, pc):
        """(decoded instruction, disassembly) at pc, or None outside the text."""
        i = (pc - self.prog.text_base) >> 2
        if pc % 4 == 0 and 0 <= i < len(self.code):
            return self.code[i], self.texts[i]
        return None

    # ---- execution ------------------------------------------------------------------------------
    def _target(self, t):
        t &= MASK
        if t == EXIT_ADDR:
            return t
        if t % 4:
            raise RVFault(f"jump to a misaligned address 0x{t:08x}")
        if not self.prog.text_base <= t < self.mem.text_end:
            raise RVFault(f"jump to 0x{t:08x}, outside the program")
        return t

    def step(self):
        """Execute one instruction and return its Step record."""
        if self.halted:
            raise RVFault("the machine has stopped", self.pc)
        pc = self.pc
        if pc == EXIT_ADDR:
            self.halt(self.x[10])
            return None
        found = self.instruction_at(pc)
        if found is None:
            if pc == self.mem.text_end:
                raise RVFault(f"execution ran past the end of the program, to 0x{pc:08x}", pc - 4)
            raise RVFault(f"no instruction at 0x{pc:08x}", None)
        ins, text = found
        if ins is None:
            word = self.prog.words[(pc - self.prog.text_base) >> 2]
            if self.on_trap is not None:
                return self._trap(pc, word, f".word 0x{word:08x}", "illegal")
            raise RVFault(f"illegal instruction 0x{word:08x}", pc)
        if self.on_trap is not None and ins.mnemonic in ("ecall", "ebreak"):
            return self._trap(pc, ins.word, text, ins.mnemonic)
        try:
            st = self._execute(ins, pc, text)
        except RVFault as e:
            if e.pc is None:
                e.pc = pc
            raise
        self.steps += 1
        self.stats["instructions"] += 1
        self.pc = st.next_pc
        if self.pc == EXIT_ADDR and not self.halted:
            self.halt(self.x[10])
        return st

    def _trap(self, pc, word, text, cause):
        """A precise trap: on_trap(machine, cause) runs with .pc at the trapping instruction, and the
        machine resumes wherever the handler leaves .pc (pc + 4 skips the instruction)."""
        self.steps += 1
        self.traps += 1
        self.stats["instructions"] += 1
        number = None
        if cause == "ecall":
            number = sext(self.x[17], 32)
            self.stats["ecalls"] += 1
        try:
            self.on_trap(self, cause)
        except RVFault as e:
            if e.pc is None:
                e.pc = pc
            raise
        if self.pc == EXIT_ADDR and not self.halted:
            self.halt(self.x[10])
        return Step(pc, word, text, "system", None, None, (), None, None, None, None, None, self.pc, number,
                    cause)

    def _execute(self, ins, pc, text):
        n, x = ins.mnemonic, self.x
        rs1, rs2, rd, imm = ins.rs1, ins.rs2, ins.rd, ins.imm
        a, b = x[rs1], x[rs2]
        nxt = (pc + 4) & MASK
        kind, val, srcs = "alu", None, ()
        mem_kind = mem_addr = mem_size = mem_value = taken = ecall = None
        if ins.fmt == "R":
            srcs = tuple(r for r in (rs1, rs2) if r)
            if n == "add":
                val = a + b
            elif n == "sub":
                val = a - b
            elif n == "and":
                val = a & b
            elif n == "or":
                val = a | b
            elif n == "xor":
                val = a ^ b
            elif n == "sll":
                val = a << (b & 31)
            elif n == "srl":
                val = a >> (b & 31)
            elif n == "sra":
                val = sext(a, 32) >> (b & 31)
            elif n == "slt":
                val = int(sext(a, 32) < sext(b, 32))
            elif n == "sltu":
                val = int(a < b)
            else:
                kind = "muldiv"
                sa, sb = sext(a, 32), sext(b, 32)
                if n == "mul":
                    val = a * b
                elif n == "mulh":
                    val = (sa * sb) >> 32
                elif n == "mulhsu":
                    val = (sa * b) >> 32
                elif n == "mulhu":
                    val = (a * b) >> 32
                elif n == "div":
                    val = -1 if sb == 0 else sa if (sa == -(1 << 31) and sb == -1) else _tdiv(sa, sb)
                elif n == "divu":
                    val = MASK if b == 0 else a // b
                elif n == "rem":
                    val = sa if sb == 0 else 0 if (sa == -(1 << 31) and sb == -1) else sa - sb * _tdiv(sa, sb)
                elif n == "remu":
                    val = a if b == 0 else a % b
        elif ins.fmt == "I" and ins.word & 0x7F == 0x13:
            srcs = (rs1,) if rs1 else ()
            sa = sext(a, 32)
            if n == "addi":
                val = a + imm
            elif n == "andi":
                val = a & (imm & MASK)
            elif n == "ori":
                val = a | (imm & MASK)
            elif n == "xori":
                val = a ^ (imm & MASK)
            elif n == "slti":
                val = int(sa < imm)
            elif n == "sltiu":
                val = int(a < (imm & MASK))
            elif n == "slli":
                val = a << imm
            elif n == "srli":
                val = a >> imm
            elif n == "srai":
                val = sa >> imm
        elif n in ("lb", "lh", "lw", "lbu", "lhu"):
            kind, mem_kind = "load", "load"
            srcs = (rs1,) if rs1 else ()
            mem_size = {"lb": 1, "lbu": 1, "lh": 2, "lhu": 2, "lw": 4}[n]
            mem_addr = (a + imm) & MASK
            val = self.load(mem_addr, mem_size, signed=n in ("lb", "lh"))
            mem_value = val
            self.stats["loads"] += 1
        elif ins.fmt == "S":
            kind, mem_kind = "store", "store"
            srcs = tuple(r for r in (rs1, rs2) if r)
            mem_size = {"sb": 1, "sh": 2, "sw": 4}[n]
            mem_addr = (a + imm) & MASK
            mem_value = b & ((1 << (8 * mem_size)) - 1)
            self.store(mem_addr, mem_size, b)
            self.stats["stores"] += 1
        elif ins.fmt == "B":
            kind = "branch"
            srcs = tuple(r for r in (rs1, rs2) if r)
            sa, sb = sext(a, 32), sext(b, 32)
            taken = {"beq": a == b, "bne": a != b, "blt": sa < sb, "bge": sa >= sb,
                     "bltu": a < b, "bgeu": a >= b}[n]
            self.stats["branches"] += 1
            if taken:
                self.stats["taken"] += 1
                nxt = self._target(pc + imm)
        elif n == "lui":
            val = imm << 12
        elif n == "auipc":
            val = pc + (imm << 12)
        elif n == "jal":
            kind = "jump"
            nxt = self._target(pc + imm)
            val = pc + 4
            self.stats["jumps"] += 1
        elif n == "jalr":
            kind = "jump"
            srcs = (rs1,) if rs1 else ()
            nxt = self._target((a + imm) & ~1)
            val = pc + 4
            self.stats["jumps"] += 1
        elif n == "ecall":
            kind = "system"
            ecall = sext(x[17], 32)
            self.stats["ecalls"] += 1
            handler = self.ecalls.get(ecall)
            if handler is not None:
                handler(self)
            elif not (self.on_ecall and self.on_ecall(self, ecall)):
                raise RVFault(f"unknown ecall {ecall} (the number is read from a7)")
        elif n == "ebreak":
            kind = "system"
            if self.on_ebreak is None:
                raise RVFault("ebreak: a breakpoint, and no debugger is attached")
            self.on_ebreak(self)
        out_rd = None
        if val is not None and rd:
            x[rd] = val & MASK
            out_rd, val = rd, x[rd]
        else:
            val = None
        return Step(pc, ins.word, text, kind, out_rd, val, srcs, mem_kind, mem_addr, mem_size, mem_value,
                    taken, nxt, ecall)

    def run(self, max_steps=1_000_000, trace=None):
        """Run until the program exits; return its exit status. trace(step) is called after each
        instruction. Raises RVFault (StepLimit when max_steps instructions ran without an exit)."""
        while not self.halted:
            if self.steps >= max_steps:
                raise StepLimit(f"stopped after {max_steps} steps, the step limit", self.pc)
            st = self.step()
            if trace is not None and st is not None:
                trace(st)
        return self.exit_code


def _tdiv(a, b):
    """Signed division rounding toward zero, as div does."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _print_int(m):
    m.write(str(m.reg(10)))


def _print_string(m):
    m.write(m.read_string(m.x[10]))


def _print_char(m):
    m.write(chr(m.x[10] & 0xFF))


def _read_int(m):
    line = m.read_line().strip()
    try:
        v = int(line, 10)
    except ValueError:
        try:
            v = int(line, 0)
        except ValueError:
            raise RVFault(f"read int: {line!r} is not a number") from None
    if not -(1 << 31) <= v <= MASK:
        raise RVFault(f"read int: {v} does not fit in 32 bits")
    m.set_reg(10, v)


def _sbrk(m):
    m.set_reg(10, m.mem.sbrk(m.reg(10)))


def _exit0(m):
    m.halt(0)


def _exit_code(m):
    m.halt(m.x[10])


def run_source(text, inputs=(), max_steps=1_000_000):
    """Assemble and run; return (output, exit status, stats). Raises AsmError or RVFault."""
    m = Machine(assemble(text), inputs=list(inputs))
    code = m.run(max_steps)
    return m.output_text, code, dict(m.stats)


def describe(st, m):
    """The effect column of a --trace line."""
    parts = []
    if st.mem_kind == "store":
        parts.append(f"mem[0x{st.mem_addr:08x}] = {_fmt(st.mem_value)} ({SIZE_NAME[st.mem_size]})")
    if st.rd is not None:
        s = f"{ABI[st.rd]} = {_fmt(st.rd_value)}"
        if st.mem_kind == "load":
            s += f"  <- mem[0x{st.mem_addr:08x}] ({SIZE_NAME[st.mem_size]})"
        parts.append(s)
    if st.branch_taken is not None:
        parts.append(f"taken -> {st.next_pc:08x}" if st.branch_taken else "not taken")
    elif st.kind == "jump":
        parts.append("-> exit" if st.next_pc == EXIT_ADDR else f"-> {st.next_pc:08x}")
    return ", ".join(parts)
