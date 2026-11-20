"""The figure files are what figs.py writes from the code and the captured outputs."""
import figs


def test_figures_regenerate():
    names = ["kd_partition.tex", "kmeans_0.tex", "kmeans_1.tex", "kmeans_2.tex",
             "dendrogram.tex", "overfit.dat"]
    before = {n: (figs.HERE / n).read_text() for n in names}
    figs.kd_partition()
    states = figs.kmeans_panels()
    figs.dendrogram()
    rows = figs.depth_chart()
    assert {n: (figs.HERE / n).read_text() for n in names} == before
    assert len(states) == 3 and len(rows) == 11
