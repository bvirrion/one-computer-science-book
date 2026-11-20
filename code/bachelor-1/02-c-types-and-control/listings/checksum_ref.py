# checksum_ref.py: the specification of the checksum, in Python (unbounded integers).
import csv
import sys

INT_MAX = 2**31 - 1


def words(path):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            t = float(row["temp_c"]) if row["temp_c"] else 0.0
            yield round(t * 10) % 2**16   # the int16 bits, read as unsigned


def checksum(w):
    return sum(a * b for a, b in zip(w, w[1:])) % 2**32


if __name__ == "__main__":
    w = list(words(sys.argv[1] if len(sys.argv) > 1 else "weather.csv"))
    over = [(a, b) for a, b in zip(w, w[1:]) if a * b > INT_MAX]
    print(f"{len(w)} readings, checksum {checksum(w)}")
    print(f"{len(over)} of {len(w) - 1} products exceed INT_MAX")
    print(f"largest word {max(w)}")
