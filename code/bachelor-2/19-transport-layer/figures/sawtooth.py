"""Write sawtooth.dat (the window per round trip) and phase.dat (two AIMD flows)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))

import aimd  # noqa: E402
import fairness  # noqa: E402

SAW, PHASE = HERE / "sawtooth.dat", HERE / "phase.dat"


def main():
    saw = list(aimd.rounds(120, 0.002))
    SAW.write_text("round w\n" + "".join(f"{r} {w:g}\n" for r, w in enumerate(saw)))
    phase = list(fairness.trajectory(4.0, 40.0, 50.0, 120))
    PHASE.write_text("x1 x2\n" + "".join(f"{a:g} {b:g}\n" for a, b in phase))


if __name__ == "__main__":
    main()
