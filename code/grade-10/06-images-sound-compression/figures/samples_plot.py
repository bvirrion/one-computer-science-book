"""Write samples_plot.dat: a 440 Hz tone sampled at 8000 Hz, quantised on 8 levels."""
import math
from pathlib import Path

OUT = Path(__file__).with_suffix(".dat")
RATE, FREQUENCY, LEVELS = 8000, 440, 8


def sample(k):
    """The tone at sample k, between -1 and 1."""
    return math.sin(2 * math.pi * FREQUENCY * k / RATE)


def quantised(x):
    step = 2 / (LEVELS - 1)
    return -1 + round((x + 1) / step) * step


def main():
    lines = ["ms value level"]
    for k in range(0, 21):
        x = sample(k)
        lines.append(f"{1000 * k / RATE:.4f} {x:.5f} {quantised(x):.5f}")
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
