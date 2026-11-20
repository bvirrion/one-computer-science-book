"""count.dat is the printed count to infinity."""
import count


def test_dat_matches_output():
    rows = count.table(count.OUTPUT.read_text())
    assert rows[0] == (1, 2, 3) and rows[-1][1:] == (16, 16)
    assert count.DAT.read_text().splitlines()[1:] == [f"{r} {a} {b}" for r, a, b in rows]
