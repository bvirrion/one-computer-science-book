"""The throughput chart's data are read from the captured output."""
import load_dat


def test_load_data():
    before = load_dat.DAT.read_text()
    rows = load_dat.main()
    assert load_dat.DAT.read_text() == before
    assert [r[0] for r in rows] == ["1", "2", "4", "8"]
    # with 8 threads, the shards beat the single lock
    assert float(rows[-1][2]) > float(rows[-1][1])
