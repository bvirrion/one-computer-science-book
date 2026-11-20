"""sweep.dat is the measured sweep, and the sweep has the shape of a memory hierarchy."""
import sweep


def test_dat_matches_output():
    rows = sweep.table(sweep.OUTPUT.read_text())
    assert sweep.DAT.read_text().splitlines()[1:] == [f"{k} {ns}" for k, ns in rows]


def test_rises_past_each_level():
    ns = dict(sweep.table(sweep.OUTPUT.read_text()))
    l1, l2, l3, dram = ns[16], ns[512], ns[4096], ns[262144]   # inside each level
    assert l1 < l2 < l3 < dram
    assert dram > 10 * l1                                       # main memory is far away
