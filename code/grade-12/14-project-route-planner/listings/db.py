"""Milestone 1: the planner's database, with its keys and constraints."""
import sqlite3

import town

SCHEMA = """
CREATE TABLE place (
    place_id  INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    kind      TEXT NOT NULL
);
CREATE TABLE road (
    road_id    INTEGER PRIMARY KEY,
    from_place INTEGER NOT NULL REFERENCES place(place_id),
    to_place   INTEGER NOT NULL REFERENCES place(place_id),
    length_m   INTEGER NOT NULL CHECK (length_m > 0),
    speed_kmh  INTEGER NOT NULL CHECK (speed_kmh BETWEEN 10 AND 130),
    one_way    INTEGER NOT NULL CHECK (one_way IN (0, 1)),
    CHECK (from_place <> to_place)
);
"""


def build():
    """A new in-memory database filled from the town's places and roads."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    places = town.load("places")
    conn.executemany("INSERT INTO place VALUES (?, ?, ?)",
                     [(p["place_id"], p["name"], p["kind"]) for p in places])
    conn.executemany("INSERT INTO road VALUES (?, ?, ?, ?, ?, ?)",
                     [(r["road_id"], r["from_place"], r["to_place"], r["length_m"],
                       r["speed_kmh"], r["one_way"]) for r in town.load("roads")])
    conn.commit()
    return conn
