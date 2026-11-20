"""aloha.dat is the simulation's output; the theory column is G e^-G; maximum 1/e."""
import math

import aloha


def test_dat_matches_output():
    rows = aloha.table(aloha.OUTPUT.read_text())
    assert len(rows) == 12
    assert aloha.DAT.read_text().splitlines()[1:] == [f"{g} {s} {t}" for g, s, t in rows]
    for g, s, t in rows:
        assert abs(t - g * math.exp(-g)) < 6e-4
        assert abs(s - t) < 0.01
    assert max(rows, key=lambda r: r[2])[0] == 1.0
