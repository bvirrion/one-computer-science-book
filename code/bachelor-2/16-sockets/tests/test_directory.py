"""The directory server, each design, against the Python client and the town's tables."""
import csv
import shutil
import subprocess
import time
from pathlib import Path

import pytest
from directory_client import ask

HERE = Path(__file__).resolve().parent.parent
L = HERE / "listings"
TOWN = HERE.parents[2] / "data" / "town"
PORT = 44166


@pytest.fixture(scope="module")
def server_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("dir")
    for name in ("people.csv", "streets.csv"):
        shutil.copy(TOWN / name, d / name)
    srcs = [str(L / f) for f in ("directory_server.c", "directory.c", "servers.c", "net.c")]
    subprocess.run(["gcc", "-std=c17", "-O2", "-Wall", "-Wextra", "-Werror", "-o",
                    str(d / "directory_server"), *srcs], check=True)
    return d


def expected():
    streets = {r["street_id"]: r["name"] for r in csv.DictReader(open(TOWN / "streets.csv"))}
    people = list(csv.DictReader(open(TOWN / "people.csv")))
    return streets, people


@pytest.mark.parametrize("design", ["fork", "threads", "poll"])
def test_answers(server_dir, design):
    streets, people = expected()
    requests = ["who 1", f"who {len(people)}", "who 0", f"who {len(people) + 1}",
                "street Bridge Road", "street Nowhere", "hello", ""]
    proc = subprocess.Popen([str(server_dir / "directory_server"), str(PORT), design,
                             str(len(requests))], cwd=server_dir)
    time.sleep(0.2)
    try:
        got = [ask(PORT, r) for r in requests]
    finally:
        proc.wait(timeout=10)
    first, last = people[0], people[-1]
    assert got[0] == (f"{first['first_name']} {first['last_name']}, born "
                      f"{first['birth_year']}, {streets[first['street_id']]}")
    assert got[1].startswith(f"{last['first_name']} {last['last_name']}")
    assert got[2] == "error: no person 0"
    assert got[3] == f"error: no person {len(people) + 1}"
    n = sum(streets[p["street_id"]] == "Bridge Road" for p in people)
    assert got[4] == f"Bridge Road: {n} people"
    assert got[5] == "Nowhere: 0 people"
    assert got[6] == got[7] == "error: unknown request"
