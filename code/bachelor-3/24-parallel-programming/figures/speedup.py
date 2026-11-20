"""speedup.py -- the measured speed-ups of sum_threads.rs and weather_scan.rs, read from
their captured outputs, as one table for the chart: p mem cpu scan."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"


def rows(name, skip):
    lines = (OUT / f"{name}.txt").read_text().splitlines()[skip:]
    return {
        int(f[0]): f for f in (line.split() for line in lines) if f and f[0].isdigit()
    }


if __name__ == "__main__":
    s, w = rows("sum_threads", 2), rows("weather_scan", 3)
    table = ["p mem cpu scan"] + [
        f"{p} {s[p][2]} {s[p][4]} {w[p][2]}" for p in range(1, 9)
    ]
    (HERE / "speedup.dat").write_text("\n".join(table) + "\n")
