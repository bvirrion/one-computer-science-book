"""The chart of the measurement must show the printed output: figures/measure.dat
is what figures/measure.py derives from outputs/timing.txt (rerun it after a capture)."""

import importlib.util
from pathlib import Path

CHAPTER = Path(__file__).resolve().parents[1]


def test_measure_dat_is_derived_from_the_printed_timing():
    path = CHAPTER / "figures" / "measure.py"
    spec = importlib.util.spec_from_file_location("measure_fig", path)
    measure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measure)
    expected = measure.table((CHAPTER / "outputs" / "timing.txt").read_text())
    assert (CHAPTER / "figures" / "measure.dat").read_text() == expected
