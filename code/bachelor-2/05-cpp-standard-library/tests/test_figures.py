"""The chart's table is the captured measurement, row for row."""
import importlib.util
from pathlib import Path

FIG = Path(__file__).parent.parent / "figures" / "vector_vs_list.py"
spec = importlib.util.spec_from_file_location("vector_vs_list", FIG)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_dat_matches_output():
    rows = mod.table(mod.OUTPUT.read_text())
    assert [r[0] for r in rows] == [1000, 2000, 5000, 10000, 20000, 40000]
    dat = mod.DAT.read_text().splitlines()
    assert dat[0] == "n vector list" and len(dat) == len(rows) + 1
    for line, (n, v, s) in zip(dat[1:], rows):
        assert line.split() == [str(n), str(v), str(s)]


def test_list_slower_and_growing():
    rows = mod.table(mod.OUTPUT.read_text())
    assert all(s > v for _, v, s in rows)
