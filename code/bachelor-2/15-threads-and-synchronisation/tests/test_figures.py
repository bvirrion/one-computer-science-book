"""lost.dat is the measured output, and the percentages agree with the counts."""
import lost


def test_dat_matches_output():
    rows = lost.table(lost.OUTPUT.read_text())
    assert lost.DAT.read_text().splitlines()[1:] == [f"{k} {e} {g} {p}"
                                                     for k, e, g, p in rows]
    for k, e, g, p in rows:
        assert e == k * 1_000_000 and 0 < g <= e
        assert abs(100 * (e - g) / e - p) < 0.051
    assert rows[0][3] == 0.0 and rows[-1][3] > 10           # alone: nothing lost
