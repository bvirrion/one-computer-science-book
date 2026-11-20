"""Write thermostat_plot.dat: two hours of the room, plain and with hysteresis."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from sensor import room  # noqa: E402
from thermostat import hysteresis, plain  # noqa: E402

OUT = Path(__file__).with_suffix(".dat")


def main():
    a = room(360, plain, random.Random(4))
    b = room(360, hysteresis, random.Random(4))
    lines = ["minute plain plain_on hyst hyst_on"]
    for m in range(120, 241):
        lines.append(f"{m} {a[m][0]:.3f} {int(a[m][1])} {b[m][0]:.3f} {int(b[m][1])}")
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
