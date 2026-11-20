"""The chart's data are the measured output, row for row."""
import backtrack


def test_dat():
    backtrack.main()
    rows = backtrack.DAT.read_text().splitlines()[1:]
    assert len(rows) >= 8
    times = [float(r.split()[1]) for r in rows]
    assert times[-1] > 100 * times[0]          # exponential: far more than linear
