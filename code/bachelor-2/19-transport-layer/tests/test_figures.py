"""The chart data are the listings' functions, written as they are."""
import sawtooth


def test_dat_files():
    sawtooth.main()
    rows = sawtooth.SAW.read_text().splitlines()[1:]
    assert len(rows) == 120 and rows[0] == "0 1"
    assert len(sawtooth.PHASE.read_text().splitlines()) == 121
