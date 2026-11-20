"""The charts' data are the captured outputs, row for row."""
import chart_data


def test_dat():
    chart_data.main()
    chains = chart_data.HERE.joinpath("chains.dat").read_text().splitlines()[1:]
    assert len(chains) == 5
    assert all(int(f) == int(n) > int(u) for n, f, u in (r.split() for r in chains))
    bloom = chart_data.HERE.joinpath("bloom.dat").read_text().splitlines()[1:]
    assert [r.split()[0] for r in bloom] == [str(k) for k in range(1, 11)]
    assert all(abs(float(m) - float(f)) < 0.005 for _, m, f in (r.split() for r in bloom))
