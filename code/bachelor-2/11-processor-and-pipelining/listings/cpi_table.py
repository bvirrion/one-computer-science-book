"""cpi_table.py: the CPI of three programs in three pipeline configurations."""
from pipeline import schedule, steps_of
from predictor import TwoBit

PROGRAMS = ["loop_sum.S", "bubble_sort.S", "collatz.S"]
CONFIGS = [("no forwarding", False, None), ("forwarding", True, None),
           ("forwarding + two-bit", True, TwoBit)]

print(f"{'program':<15}{'instructions':>13}" + "".join(f"{c[0]:>22}" for c in CONFIGS))
for name in PROGRAMS:
    with open(name) as f:
        steps = steps_of(f.read())
    cpis = [schedule(steps, fwd, p() if p else None).cpi() for _, fwd, p in CONFIGS]
    print(f"{name:<15}{len(steps):>13}" + "".join(f"{c:>22.3f}" for c in cpis))
