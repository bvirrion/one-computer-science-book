"""exo_loop.py: a name whose pointer points at itself (exercise 2)."""
from dns_message import read_name

good = bytes(12) + b"\x03www\x00" + b"\x03ftp\xc0\x0c"     # ftp, then a pointer to 12
print(read_name(good, 17))
loop = bytes(12) + b"\x03www\xc0\x0c"                      # www, then back to 12
try:
    print(read_name(loop, 12))
except ValueError as e:
    print("rejected:", e)
