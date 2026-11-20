"""exo_keys.py: the candidate keys of the reading-room bookings."""
from fd import fds, keys

R = ["seat", "day", "slot", "member", "desk"]
DEPS = fds("seat day slot -> member; member day slot -> seat; seat -> desk")
for k in keys(R, DEPS):
    print("key:", sorted(k))
