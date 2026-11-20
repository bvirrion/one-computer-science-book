"""backtracking.py: Python's re on (a|a)*b against a^n, which has no b: time per n."""
import subprocess
import sys

PROGRAM = """
import re, time
pattern, text = re.compile("(a|a)*b"), "a" * {n}
t = time.perf_counter()
assert pattern.match(text) is None             # every way of splitting is tried
print(time.perf_counter() - t)
"""

print("   n   time (s)   ratio to n - 1")
previous = None
for n in range(16, 28):
    try:                                         # each run in its own process, bounded
        run = subprocess.run([sys.executable, "-c", PROGRAM.format(n=n)],
                             capture_output=True, text=True, timeout=60)
        seconds = float(run.stdout)
    except subprocess.TimeoutExpired:
        print(f"{n:4}   over 60 s: stopped")
        break
    ratio = f"{seconds / previous:6.2f}" if previous else ""
    print(f"{n:4} {seconds:10.4f}   {ratio}".rstrip())
    previous = seconds
