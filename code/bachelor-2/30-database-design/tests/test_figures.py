"""The chart's data are read from the captured output."""
import index_dat


def test_index_data():
    before = index_dat.DAT.read_text()
    rows = index_dat.main()
    assert index_dat.DAT.read_text() == before
    assert [r[0] for r in rows] == ["10000", "100000", "1000000"]
    assert all(float(scan) > float(seek) for _, scan, seek in rows)
