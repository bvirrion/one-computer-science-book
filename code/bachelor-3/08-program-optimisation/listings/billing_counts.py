"""billing_counts.py -- the weekend problem: the billing program compiled at
each level, run on rv with the days late of the town library's returned loans.
Counts the whole run, then the hot loop alone (from label .Lmain_4 to .Lmain_6).
Usage: python billing_counts.py loans.csv FILE.S ..."""
import csv
import sys
from datetime import date

from rv import Machine, assemble

days = []
with open(sys.argv[1]) as f:
    for row in csv.DictReader(f):
        if row["return_date"]:
            due = date.fromisoformat(row["due_date"])
            days.append((date.fromisoformat(row["return_date"]) - due).days)
late = sum(d > 0 for d in days)
print(f"{len(days)} returned loans, {late} late, at most {max(days)} days")
print(f"{'':<7} {'whole run':>28}   {'hot loop':>16}")
head = f"{'instructions':>12} {'loads':>7} {'stores':>7}"
head += f"   {'instr.':>7} {'ld+st':>7}"
print(f"{'program':<7} {head}   output")
for name in sys.argv[2:]:
    prog = assemble(open(name).read(), name)
    start, end = prog.symbols[".Lmain_4"], prog.symbols[".Lmain_6"]
    loop = {"instr": 0, "mem": 0}

    def count(step, start=start, end=end, loop=loop):
        if start <= step.pc < end:
            loop["instr"] += 1
            loop["mem"] += step.kind in ("load", "store")

    m = Machine(prog, inputs=[len(days)] + days)
    m.run(trace=count)
    s, out = m.stats, " ".join(m.output_text.split())
    print(f"{name:<7} {s['instructions']:>12} {s['loads']:>7} {s['stores']:>7}"
          f"   {loop['instr']:>7} {loop['mem']:>7}   {out}")
