"""Write designs.dat from the output of listings/load.sh (one measured run)."""
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent / "outputs" / "load.txt"
DAT = HERE / "designs.dat"
SHORT = {"process per connection": "process", "thread per connection": "thread",
         "event loop (poll)": "poll"}


def table(text):
    rows = []
    for line in text.splitlines():
        for name, short in SHORT.items():
            if line.startswith(name):
                seconds, rate = line[len(name):].split()
                rows.append((short, float(seconds), int(rate)))
    return rows


def main():
    rows = table(OUTPUT.read_text())
    lines = "".join(f"{d} {s} {r}\n" for d, s, r in rows)
    DAT.write_text("design seconds rate\n" + lines)


if __name__ == "__main__":
    main()
