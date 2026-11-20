"""run_guest.py -- the guest of guest.S under the monitor: what its devices showed, and
how often it trapped."""
from monitor import Monitor

vm = Monitor(open("guest.S").read())
console, status = vm.run()
print(console, end="")
print(f"powered off with status {status}")
m = vm.m
print(f"{m.steps} guest instructions, {m.traps} traps: one trap every "
      f"{m.steps / m.traps:.1f} instructions")
