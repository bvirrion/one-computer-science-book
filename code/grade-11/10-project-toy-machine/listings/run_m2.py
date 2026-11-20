from pathlib import Path

from assembler_m2 import first_pass, second_pass
from tokens import read_program

PROGRAMS = Path(__file__).resolve().parents[2] / "02-von-neumann-machine" / "listings"
rows = read_program((PROGRAMS / "sum_array.toy").read_text())
symbols = first_pass(rows)
print("symbol table:", symbols)
for address, data, line in second_pass(rows, symbols):
    print(f"{address:3d}: {' '.join(f'{b:3d}' for b in data):<12} from line {line}")
