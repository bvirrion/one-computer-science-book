"""exo_aaaa.py: an AAAA query for www.brenmoor.test, byte by byte (exercise 3)."""
from dns_message import query

q = query(0x0b0e, "www.brenmoor.test", "AAAA", recurse=True)
for start in range(0, len(q), 12):
    print(q[start:start + 12].hex(" "))
