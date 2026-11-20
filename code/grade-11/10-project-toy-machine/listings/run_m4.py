from pathlib import Path

from assembler_m2 import assemble
from simulator_m4 import new_machine, run

PROGRAMS = Path(__file__).resolve().parents[2] / "02-von-neumann-machine" / "listings"
for name, inputs in [("count_down", []), ("max2", [57, 201]), ("multiply", [6, 7]),
                     ("abs_value", [-25]), ("call_square", []), ("sum_array", [])]:
    m = new_machine(assemble((PROGRAMS / f"{name}.toy").read_text()), inputs)
    outputs = run(m)
    print(f"{name:<12} inputs {str(inputs):<10} outputs {str(outputs):<10}"
          f" steps {m['steps']:3d}  SP {m['sp']}")
