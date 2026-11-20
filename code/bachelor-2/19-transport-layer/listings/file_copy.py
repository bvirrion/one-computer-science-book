"""file_copy.py: the town's people table sent in 100-byte packets over a lossy link."""
from pathlib import Path

from selective_repeat import transfer

town = Path(__file__).resolve().parents[4] / "data" / "town"
table = (town / "people.csv").read_bytes()
packets = [table[i:i + 100] for i in range(0, len(table), 100)]
out, t, link = transfer(packets, k=6, window=16, loss=0.2, dup=0.05, jitter=20, seed=7)
copy = b"".join(out)
print(f"file: {len(table)} bytes in {len(packets)} packets")
print(f"link: {link.lost} of {link.sent} packets lost, some duplicated, some reordered")
print(f"received {len(copy)} bytes, identical to the original: {copy == table}")
