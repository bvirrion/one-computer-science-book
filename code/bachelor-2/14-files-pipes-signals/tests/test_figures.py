"""copy_times.dat is the measured output; reads follow the law; time falls as b grows."""
import copy_times


def test_dat_matches_output():
    rows = copy_times.table(copy_times.OUTPUT.read_text())
    lines = copy_times.DAT.read_text().splitlines()[1:]
    assert lines == [f"{b} {x} {t}" for b, x, t in rows]


def test_law_and_shape():
    rows = copy_times.table(copy_times.OUTPUT.read_text())
    n = 4 << 20
    assert all(x == -(-n // b) + 1 for b, x, _ in rows)
    times = [t for _, _, t in rows]
    assert times[0] > 100 * times[-1]                 # one byte at a time: far slower
    assert all(t1 >= t2 * 0.8 for t1, t2 in zip(times, times[1:]))
