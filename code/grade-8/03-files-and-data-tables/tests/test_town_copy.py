"""The chapter's copies of the town tables are byte for byte those of data/town/."""

from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TOWN = HERE.parents[2] / "data" / "town"


def test_copies():
    for name in ["books.csv", "loans.csv", "weather.csv"]:
        assert (HERE / "listings" / name).read_bytes() == (TOWN / name).read_bytes()
