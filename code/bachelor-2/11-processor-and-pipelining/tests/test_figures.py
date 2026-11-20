"""cpi.dat is the CPI table that cpi_table.py prints, and that table is the model's."""
from pathlib import Path

import cpi
from pipeline import schedule, steps_of
from predictor import TwoBit

HERE = Path(__file__).resolve().parent.parent


def test_dat_matches_output_and_model():
    rows = cpi.table(cpi.OUTPUT.read_text())
    assert cpi.DAT.read_text().splitlines()[1:] == [f"{n} {a} {b} {c}" for n, a, b, c in rows]
    for name, a, b, c in rows:
        steps = steps_of((HERE / "listings" / (name.replace("-", "_") + ".S")).read_text())
        got = [schedule(steps, False).cpi(), schedule(steps).cpi(), schedule(steps, True, TwoBit()).cpi()]
        assert [round(g, 3) for g in got] == [a, b, c]
