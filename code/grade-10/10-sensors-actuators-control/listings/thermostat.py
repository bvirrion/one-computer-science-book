import random

from convert import to_celsius
from sensor import room

TARGET = 20.0


def plain(raw, heater):
    """On below the target, off above it."""
    return to_celsius(raw) < TARGET


def hysteresis(raw, heater, half_band=0.5):
    """On below target - half_band, off above target + half_band; else keep it."""
    t = to_celsius(raw)
    if t < TARGET - half_band:
        return True
    if t > TARGET + half_band:
        return False
    return heater


if __name__ == "__main__":
    for name, controller in (("plain", plain), ("hysteresis", hysteresis)):
        trace = room(360, controller, random.Random(4))
        switches = sum(1 for a, b in zip(trace, trace[1:]) if a[1] != b[1])
        late = [t for t, _ in trace[120:]]
        print(f"{name:10}: {switches:3} switches in 6 hours,"
              f" temperature {min(late):.2f} to {max(late):.2f}")
