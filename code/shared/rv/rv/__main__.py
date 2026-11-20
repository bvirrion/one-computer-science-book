"""python -m rv run|asm|dis ...  (see RV.md)"""
import argparse
import sys

from rv.asm import AsmError, assemble, statement_text
from rv.isa import ABI, MASK, disassemble, fields
from rv.machine import ECALL_NAMES, Machine, RVFault, StepLimit, describe

TRACE_HEAD = f"{'step':>5}  {'pc':<8}  {'word':<8}  {'instruction':<26}effect"


def _line(n, pc, word, text, effect):
    return f"{n:5d}  {pc:08x}  {word:08x}  {text:<26}{effect}".rstrip()


class _Out:
    """stdout, remembering whether the program left the cursor in the middle of a line."""

    def __init__(self, m):
        self.m = m

    def newline(self):
        if self.m.column:
            sys.stdout.write("\n")
            self.m.column = 0

    def say(self, text):
        self.newline()
        print(text, flush=True)


def _where(prog, pc):
    if pc is None:
        return ""
    line, src = prog.line_of(pc)
    return f"line {line}: {statement_text(src)}: " if line else ""


def _run(args, prog):
    m = Machine(prog, stdin=sys.stdin, out=sys.stdout, echo=not sys.stdin.isatty())
    o = _Out(m)
    try:
        if args.trace:
            o.say(TRACE_HEAD)
        while not m.halted:
            if m.steps >= args.steps:
                raise StepLimit(f"stopped after {args.steps} steps, the step limit (raise it with --steps N)",
                                m.pc)
            if not args.trace:
                m.step()
                continue
            found = m.instruction_at(m.pc)
            if found and found[0] is not None and found[0].mnemonic == "ecall":
                n = m.reg("a7")
                a0 = m.x[10]
                o.say(_line(m.steps + 1, m.pc, found[0].word, found[1], f"ecall {n} ({ECALL_NAMES.get(n, '?')})"))
                m.step()
                if m.x[10] != a0 and not m.halted:
                    o.say(" " * 53 + describe_a0(m))
                continue
            st = m.step()
            if st is not None:
                o.say(_line(m.steps, st.pc, st.word, st.text, describe(st, m)))
    except RVFault as e:
        o.newline()
        sys.stdout.flush()
        print(f"rv: {_where(prog, e.pc)}{e.msg}", file=sys.stderr, flush=True)
        return 1
    if args.trace:
        o.say(f"exit status {m.exit_code} after {m.steps} steps")
    if args.stats:
        s = m.stats
        o.say("--- stats ---")
        for k in ("instructions", "loads", "stores"):
            o.say(f"{k:<13}{s[k]:>9}")
        o.say(f"{'branches':<13}{s['branches']:>9}  ({s['taken']} taken)")
        for k in ("jumps", "ecalls"):
            o.say(f"{k:<13}{s[k]:>9}")
    if args.regs:
        o.say(f"--- registers (pc = 0x{m.pc & MASK:08x}) ---")
        for row in range(8):
            cells = []
            for i in range(row * 4, row * 4 + 4):
                v = m.x[i]
                sv = v - (1 << 32) if v >> 31 else v
                val = str(sv) if -65536 < sv < 65536 else f"0x{v:08x}"
                cells.append(f"{ABI[i]:>4} {val:<11}")
            o.say(" ".join(cells).rstrip())
    return m.exit_code


def describe_a0(m):
    v = m.x[10]
    sv = v - (1 << 32) if v >> 31 else v
    return f"a0 = {sv}" if -65536 < sv < 65536 else f"a0 = 0x{v:08x}"


def _asm(args, prog):
    if args.hex:
        for w in prog.words:
            print(f"{w:08x}")
        return 0
    labels = prog.text_labels()
    for i, w in enumerate(prog.words):
        pc = prog.text_base + 4 * i
        _ln, src, first = prog.lines[i]
        text = disassemble(w, pc, labels)
        print(f"{pc:08x}  {w:08x}  {text:<26}{statement_text(src, labels=True) if first else ''}".rstrip())
        if args.fields:
            print(f"{'':20}{fields(w)}")
    for addr, length, _ln, src in prog.data_lines:
        shown = prog.data[addr - prog.data_base:addr - prog.data_base + min(length, 8)]
        hexes = " ".join(f"{b:02x}" for b in shown) + (" ..." if length > 8 else "")
        print(f"{addr:08x}  {hexes:<28}{statement_text(src, labels=True)}".rstrip())
    return 0


def _dis(args):
    words = []
    for line in open(args.file, encoding="utf8"):
        for tok in line.split("#")[0].split():
            words.append(int(tok, 16) & MASK)
    for i, w in enumerate(words):
        pc = args.base + 4 * i
        print(f"{pc:08x}  {w:08x}  {disassemble(w, pc)}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m rv")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="assemble and run a program")
    r.add_argument("file")
    r.add_argument("--trace", action="store_true", help="print every instruction and its effect")
    r.add_argument("--regs", action="store_true", help="print the registers at the end")
    r.add_argument("--stats", action="store_true", help="count instructions, loads, stores, branches")
    r.add_argument("--steps", type=int, default=1_000_000, help="the step limit (default 1000000)")
    a = sub.add_parser("asm", help="assemble and list addresses, words and instructions")
    a.add_argument("file")
    a.add_argument("--fields", action="store_true", help="show each word's fields in binary")
    a.add_argument("--hex", action="store_true", help="print only the words, in hex")
    d = sub.add_parser("dis", help="disassemble words written in hex")
    d.add_argument("file")
    d.add_argument("--base", type=lambda s: int(s, 0), default=0x00010000, help="address of the first word")
    args = ap.parse_args(argv)
    if args.cmd == "dis":
        return _dis(args)
    try:
        prog = assemble(open(args.file, encoding="utf8").read(), args.file)
    except AsmError as e:
        print(f"rv: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"rv: {e.strerror}: {args.file}", file=sys.stderr)
        return 2
    return _asm(args, prog) if args.cmd == "asm" else _run(args, prog)


if __name__ == "__main__":
    sys.exit(main())
