"""python -m town: (re)write data/town/*.csv from the seed."""
from town import OUT, tables, write

write()
for name, rows in tables().items():
    print(f"{name:12s} {len(rows):4d} rows")
print("written to", OUT)
