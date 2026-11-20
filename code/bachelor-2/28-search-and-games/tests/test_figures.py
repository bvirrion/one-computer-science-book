"""The town map figure is what town_fig.py writes from the code."""
import town_fig


def test_town_figure():
    before = town_fig.FIG.read_text()
    dij, ast = town_fig.main()
    assert town_fig.FIG.read_text() == before
    assert set(ast) <= set(dij)
    assert before.count("\\node[astar]") == len(ast)


def test_puzzle_data():
    import puzzle_dat

    rows = puzzle_dat.main()
    assert len(rows) == 5
    assert all(int(b) > int(m) > int(h) for _, b, m, h in rows)
