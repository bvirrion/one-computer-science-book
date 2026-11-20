"""designs.dat is the measured output; 4000 requests per design; the rates agree."""
import designs


def test_dat_matches_output():
    rows = designs.table(designs.OUTPUT.read_text())
    assert [r[0] for r in rows] == ["process", "thread", "poll"]
    assert designs.DAT.read_text().splitlines()[1:] == [f"{d} {s} {r}" for d, s, r in rows]
    for _, seconds, rate in rows:
        assert abs(4000 / seconds - rate) <= 0.01 * rate + 1
    assert "failed requests: 0" in designs.OUTPUT.read_text()
