"""Write chains.dat and bloom.dat from the captured outputs of universal_hash.py and
bloom.py."""
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "outputs"


def rows(name, skip):
    lines = (OUT / name).read_text().splitlines()[skip:]
    return [line.replace("|", " ").split() for line in lines if line.strip()]


def main():
    chains = rows("universal_hash.txt", 2)
    (HERE / "chains.dat").write_text(
        "n fixed universal\n" + "".join(f"{r[0]} {r[1]} {r[2]}\n" for r in chains))
    bloom = [r for r in rows("bloom.txt", 3) if r[0].isdigit()]
    (HERE / "bloom.dat").write_text(
        "k measured formula\n" + "".join(f"{r[0]} {r[1]} {r[2]}\n" for r in bloom))


if __name__ == "__main__":
    main()
