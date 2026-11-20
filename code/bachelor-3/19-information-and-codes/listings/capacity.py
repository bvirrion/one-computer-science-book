"""capacity.py -- the binary entropy function h(p) and the capacity 1 - h(p) of the
binary symmetric channel, in bits per use."""
import math


def h(p):
    return 0.0 if p in (0, 1) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)


if __name__ == "__main__":
    print("    p      h(p)   capacity 1 - h(p)")
    for p in (0.0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.5):
        print(f"{p:>5}  {h(p):>8.4f}  {1 - h(p):>18.4f}")
