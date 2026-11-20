"""python -m toymachine run|asm|dis ...  (see TOYMACHINE.md)"""
import argparse
import sys

from toymachine import Machine, ToyError, assemble, assemble_lines, disassemble


def _read_number():
    line = sys.stdin.readline()
    if not line:
        raise ToyError("IN: no input left")
    try:
        return int(line.strip(), 0)
    except ValueError:
        raise ToyError(f"IN: {line.strip()!r} is not a number") from None


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m toymachine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("file")
    r.add_argument("--trace", action="store_true")
    r.add_argument("--dump", action="store_true")
    r.add_argument("--steps", type=int, default=10_000)
    a = sub.add_parser("asm")
    a.add_argument("file")
    d = sub.add_parser("dis")
    d.add_argument("file")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "dis":
            data = [int(x) for x in open(args.file).read().split()]
            for addr in range(0, len(data) - 1, 2):
                print(f"{addr:3d}: {data[addr]:3d} {data[addr + 1]:3d}   {disassemble(data[addr], data[addr + 1])}")
            return 0
        text = open(args.file, encoding="utf8").read()
        if args.cmd == "asm":
            for addr, bs, _n, src in assemble_lines(text):
                dec = " ".join(f"{b:3d}" for b in bs)
                binary = " ".join(f"{b:08b}" for b in bs)
                print(f"{addr:3d}: {dec:<8} {binary:<17}  {src.strip()}")
            return 0
        m = Machine(assemble(text))
        m.read_input = _read_number
        m.on_output = lambda v: print(v, flush=True)
        trace = None
        if args.trace:
            print(f"{'step':>4} {'PC':>3}  {'instruction':<16} {'R0':>3} {'R1':>3} {'R2':>3} {'R3':>3}  Z N C")

            def trace(mm):
                f = mm.flags
                print(f"{mm.steps + 1:4d} {mm.pc:3d}  {mm.current():<16} "
                      + " ".join(f"{v:3d}" for v in mm.reg) + f"  {f['Z']} {f['N']} {f['C']}", flush=True)
        m.run(max_steps=args.steps, trace=trace)
        if args.trace:
            print(f"halted after {m.steps} steps")
        if args.dump:
            f = m.flags
            print("R0={} R1={} R2={} R3={} PC={} SP={} Z={} N={} C={}".format(*m.reg, m.pc, m.sp, f["Z"], f["N"], f["C"]))
            cells = [(i, v) for i, v in enumerate(m.mem) if v]
            for i in range(0, len(cells), 8):
                print("  " + "  ".join(f"M[{a}]={v}" for a, v in cells[i:i + 8]))
        return 0
    except ToyError as e:
        print(f"error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
