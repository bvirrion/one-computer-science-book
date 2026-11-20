"""The chart's data are the measured output, row for row."""
import kmp_bench


def test_dat():
    kmp_bench.main()
    rows = [r.split() for r in kmp_bench.DAT.read_text().splitlines()[1:]]
    assert len(rows) == 8
    assert all(float(naive) > 10 * float(kmp) for _, naive, kmp in rows)
