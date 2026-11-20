"""measure.py -- run each program at the three levels on rv and compare the
counts. Usage: python measure.py NAME[:INPUT] ...
(reads NAME.0.S, NAME.1.S and NAME.2.S)"""
import sys

from rv import Machine

head = f"{'instructions':>13} {'loads':>7} {'stores':>7}"
print(f"{'program':<10} {'level':>5} {head}   output")
for arg in sys.argv[1:]:
    name, _, given = arg.partition(":")
    inputs = [int(x) for x in given.split(",")] if given else []
    outputs = set()
    for level in "012":
        m = Machine(open(f"{name}.{level}.S").read(), inputs=inputs)
        code = m.run()
        s = m.stats
        out = m.output_text.split()
        outputs.add((tuple(out), code))
        shown = " ".join(out[:3]) + (" ..." if len(out) > 3 else "")
        counts = f"{s['instructions']:>13} {s['loads']:>7} {s['stores']:>7}"
        print(f"{name:<10} {'-O' + level:>5} {counts}   {shown}")
    verdict = "same output and exit code" if len(outputs) == 1 else "OUTPUTS DIFFER"
    print(f"{'':<16} {verdict}")
