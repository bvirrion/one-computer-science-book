import hashlib
import sqlite3
from collections import defaultdict
from pathlib import Path

import town

DATA = Path(town.OUT)


def test_csv_files_match_the_generator(tmp_path):
    town.write(str(tmp_path))
    for f in sorted(DATA.glob("*.csv")):
        assert hashlib.sha256(f.read_bytes()).hexdigest() == \
            hashlib.sha256((tmp_path / f.name).read_bytes()).hexdigest(), f.name


def test_sizes():
    sizes = {k: len(v) for k, v in town.tables().items()}
    assert sizes["people"] == 120 and sizes["places"] == 30 and sizes["books"] == 80
    assert sizes["members"] == 60 and sizes["loans"] == 400 and sizes["streets"] == 24
    assert sizes["weather"] == 2 * 365 + 1


def test_road_network_is_connected_with_one_one_way_road():
    roads = town.load("roads")
    adj = defaultdict(set)
    for r in roads:
        adj[r["from_place"]].add(r["to_place"])
        adj[r["to_place"]].add(r["from_place"])
    seen, todo = {1}, [1]
    while todo:
        v = todo.pop()
        for w in adj[v] - seen:
            seen.add(w)
            todo.append(w)
    assert seen == set(range(1, 31))
    assert sum(r["one_way"] for r in roads) == 1
    assert all(r["length_m"] % 10 == 0 and r["length_m"] > 0 for r in roads)


def test_friendships_simple_graph_with_one_isolated_person():
    fr = town.load("friendships")
    assert all(f["person_a"] < f["person_b"] for f in fr)
    people = {f["person_a"] for f in fr} | {f["person_b"] for f in fr}
    assert 40 not in people and len(people) == 39


def test_loans_dates_and_planted_cases():
    loans = town.load("loans")
    assert [x["loan_id"] for x in loans] == list(range(1, 401))
    assert all(x["out_date"] < x["due_date"] for x in loans)
    open_ = [x for x in loans if x["return_date"] is None]
    late = [x for x in loans if x["return_date"] and x["return_date"] > x["due_date"]]
    assert 5 <= len(open_) <= 40 and len(late) > 40


def test_weather_planted_defects():
    w = town.load("weather")
    assert sum(1 for r in w if r["temp_c"] is None) == 6
    assert sum(1 for r in w if r["temp_c"] == -99.0) == 2
    keys = [(r["date"], r["station"]) for r in w]
    assert len(keys) - len(set(keys)) == 1


def test_sqlite_load_with_foreign_keys():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    town.to_sqlite(conn)
    n = conn.execute("SELECT COUNT(*) FROM loans JOIN books USING (book_id)").fetchone()[0]
    assert n == 400
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
