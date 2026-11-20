"""Exercise: a synchronous counter modulo 6 on three D flip-flops (A the high bit);
the codes 6 and 7 never occur and are don't-cares."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from seq import minimal_sop, sop_gates, sop_text, sop_value  # noqa: E402


def equations():
    """A+, B+, C+ as functions of (A, B, C)."""
    return [minimal_sop([q for q in range(6) if (q + 1) % 6 >> bit & 1], [6, 7], 3)
            for bit in (2, 1, 0)]


def count(edges):
    eqs, q, seen = equations(), (0, 0, 0), [0]
    for _ in range(edges):
        q = tuple(sop_value(e, q) for e in eqs)
        seen.append(4 * q[0] + 2 * q[1] + q[2])
    return seen


if __name__ == "__main__":
    for name, e in zip("ABC", equations()):
        print(f"{name}+ = {sop_text(e, 'ABC')}")
    print("gates:", sop_gates(equations()), "| states:", *count(13))
