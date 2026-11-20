"""The series' invented town, Brenmoor: every table generated from one seed (frozen 2026-11-19).

    python -m town              (re)write data/town/*.csv; must leave no diff
    import town; town.load("loans")      -> list of dicts (values typed: int, float, str or None)
    town.to_sqlite(conn)                  -> every table into an sqlite3 connection, with keys

Tables (see TOWN.md for columns and the planted defects):
  people, streets, places, roads, friendships, books, members, loans, weather
Nothing here is real: names, titles, places and readings are invented.
"""
import csv
import datetime as dt
import math
import os
import random

SEED = 20261119
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "data", "town"))

FIRST = ["Ada", "Ben", "Chloe", "Dev", "Elif", "Farid", "Grace", "Hugo", "Ines", "Jonas", "Kira",
         "Leo", "Maya", "Nils", "Omar", "Priya", "Quinn", "Rosa", "Sami", "Tara", "Umar", "Vera",
         "Wen", "Xavi", "Yara", "Zoe", "Aarav", "Bea", "Caio", "Dara", "Emil", "Fatou", "Gil",
         "Hana", "Ivo", "Jade", "Kofi", "Lina", "Milo", "Nora"]
LAST_A = ["Ash", "Brook", "Cole", "Dale", "Elm", "Fern", "Glen", "Hart", "Ivy", "Lake", "Moss",
          "North", "Oak", "Pine", "Reed", "Stone", "Thorn", "West", "Wood", "Yew"]
LAST_B = ["by", "field", "ford", "ham", "ley", "more", "ton", "well", "wick", "worth"]
STREET_A = ["Mill", "Church", "Bridge", "Station", "Market", "Garden", "Orchard", "River",
            "School", "Castle", "Meadow", "Willow"]
STREET_B = ["Street", "Road", "Lane", "Way", "Avenue", "Row"]
PLACES = [("Town Square", "square"), ("Station", "station"), ("Library", "library"),
          ("North School", "school"), ("South School", "school"), ("Market Hall", "market"),
          ("Swimming Pool", "sport"), ("Hospital", "health"), ("Town Hall", "office"),
          ("River Park", "park"), ("Hill Park", "park"), ("Museum", "museum"),
          ("Bakery Corner", "shop"), ("Old Mill", "museum"), ("Football Ground", "sport"),
          ("Bus Depot", "transport"), ("Fire Station", "service"), ("Post Office", "office"),
          ("Cinema", "leisure"), ("Theatre", "leisure"), ("East Gate", "junction"),
          ("West Gate", "junction"), ("North Bridge", "junction"), ("South Bridge", "junction"),
          ("Clinic", "health"), ("Garden Centre", "shop"), ("Allotments", "park"),
          ("Sports Hall", "sport"), ("College", "school"), ("Lighthouse Café", "shop")]
GENRES = ["adventure", "mystery", "science", "history", "poetry", "comics", "nature", "sport"]
TITLE_A = ["The Silent", "A Map of the", "Under the", "The Last", "Seven", "The Clockwork",
           "Beyond the", "The Paper", "Notes on the", "The Hidden", "A Year by the", "The Lost"]
TITLE_B = ["Lighthouse", "Orchard", "Engine", "River", "Island", "Garden", "Forest", "Tower",
           "Harbour", "Machine", "Valley", "Comet", "Library", "Bridge", "Kingdom", "Code"]
STATIONS = ["Hilltop", "Riverside"]
DATES = (dt.date(2025, 1, 1), dt.date(2025, 12, 31))


def _people(rng):
    rows, used = [], set()
    streets = _streets(rng)
    for pid in range(1, 121):
        while True:
            f, last = rng.choice(FIRST), rng.choice(LAST_A) + rng.choice(LAST_B)
            if (f, last) not in used:
                used.add((f, last))
                break
        rows.append({"person_id": pid, "first_name": f, "last_name": last,
                     "birth_year": rng.randint(1940, 2018),
                     "street_id": rng.choice(streets)["street_id"]})
    return rows


def _streets(rng):
    r = random.Random(SEED + 1)
    names, rows = set(), []
    while len(names) < 24:
        names.add(r.choice(STREET_A) + " " + r.choice(STREET_B))
    for i, n in enumerate(sorted(names), start=1):
        rows.append({"street_id": i, "name": n, "postcode": f"B-{100 + 10 * ((i - 1) // 6)}"})
    return rows


def _places(rng):
    r = random.Random(SEED + 2)
    rows = []
    pts = []
    for i, (name, kind) in enumerate(PLACES, start=1):
        while True:  # keep places at least 400 m apart on a 6 km x 5 km map
            x, y = r.randint(0, 6000), r.randint(0, 5000)
            if all(math.hypot(x - a, y - b) >= 400 for a, b in pts):
                break
        pts.append((x, y))
        rows.append({"place_id": i, "name": name, "kind": kind, "x_m": x, "y_m": y})
    return rows


def _roads(places):
    """Each place to its 3 nearest neighbours, both ways merged; lengths 10 % above the straight line,
    rounded to 10 m; speed limit by the kind of the road's ends."""
    r = random.Random(SEED + 3)
    pos = {p["place_id"]: (p["x_m"], p["y_m"]) for p in places}
    pairs = set()
    for a in pos:
        near = sorted((math.dist(pos[a], pos[b]), b) for b in pos if b != a)[:3]
        for _d, b in near:
            pairs.add((min(a, b), max(a, b)))
    rows = []
    for i, (a, b) in enumerate(sorted(pairs), start=1):
        d = math.dist(pos[a], pos[b])
        length = int(round(d * r.uniform(1.05, 1.35) / 10.0)) * 10
        speed = r.choice([30, 30, 30, 50, 50, 70])
        rows.append({"road_id": i, "from_place": a, "to_place": b, "length_m": length,
                     "speed_kmh": speed, "one_way": 0})
    # one one-way street, for the directed-graph exercises
    rows[0]["one_way"] = 1
    return rows


def _friendships(rng, people):
    r = random.Random(SEED + 4)
    ids = [p["person_id"] for p in people[:40]]
    pairs = set()
    # three loose groups (classes) plus a few bridges
    groups = [ids[:14], ids[14:27], ids[27:]]
    for g in groups:
        for a in g:
            for b in g:
                if a < b and r.random() < 0.22:
                    pairs.add((a, b))
    for _ in range(4):
        g1, g2 = r.sample(range(3), 2)
        a, b = r.choice(groups[g1]), r.choice(groups[g2])
        pairs.add((min(a, b), max(a, b)))
    # one person with no friend yet (a vertex of degree 0)
    lonely = ids[-1]
    pairs = {p for p in pairs if lonely not in p}
    return [{"person_a": a, "person_b": b, "since_year": r.randint(2015, 2025)} for a, b in sorted(pairs)]


def _books():
    r = random.Random(SEED + 5)
    rows, used = [], set()
    authors = [f"{r.choice(FIRST)} {r.choice(LAST_A)}{r.choice(LAST_B)}" for _ in range(25)]
    for bid in range(1, 81):
        while True:
            t = f"{r.choice(TITLE_A)} {r.choice(TITLE_B)}"
            if t not in used:
                used.add(t)
                break
        rows.append({"book_id": bid, "title": t, "author": r.choice(authors),
                     "year": r.randint(1950, 2025), "genre": r.choice(GENRES),
                     "pages": r.randint(48, 520)})
    return rows


def _members(people):
    r = random.Random(SEED + 6)
    chosen = sorted(r.sample([p["person_id"] for p in people], 60))
    return [{"member_id": i, "person_id": pid,
             "joined": (dt.date(2015, 1, 1) + dt.timedelta(days=r.randrange(3650))).isoformat()}
            for i, pid in enumerate(chosen, start=1)]


def _loans(books, members):
    """Loans of 2025: 21 days each; returned late sometimes; a few still out (return_date NULL)."""
    r = random.Random(SEED + 7)
    rows = []
    for lid in range(1, 401):
        out = DATES[0] + dt.timedelta(days=r.randrange(330))
        due = out + dt.timedelta(days=21)
        u = r.random()
        if u < 0.05:
            ret = None
        elif u < 0.80:
            ret = out + dt.timedelta(days=r.randint(2, 21))
        else:
            ret = due + dt.timedelta(days=r.randint(1, 30))
        rows.append({"loan_id": lid, "book_id": r.choice(books)["book_id"],
                     "member_id": r.choice(members)["member_id"], "out_date": out.isoformat(),
                     "due_date": due.isoformat(), "return_date": ret.isoformat() if ret else None})
    rows.sort(key=lambda x: (x["out_date"], x["loan_id"]))
    for i, row in enumerate(rows, start=1):
        row["loan_id"] = i
    return rows


def _weather():
    """Daily readings of 2025 at two stations. Planted defects, for the cleaning exercises:
    6 missing temperatures (None), 2 impossible ones (-99.0, the station's error code),
    and one day recorded twice at Riverside."""
    r = random.Random(SEED + 8)
    rows = []
    d = DATES[0]
    while d <= DATES[1]:
        doy = d.timetuple().tm_yday
        for s, off in zip(STATIONS, (0.0, 1.4), strict=True):
            base = 10.5 + off - 8.5 * math.cos(2 * math.pi * (doy - 15) / 365.0)
            t = round(base + r.gauss(0, 2.2), 1)
            rain = 0.0 if r.random() < 0.6 else round(r.expovariate(1 / 4.5), 1)
            wind = round(abs(r.gauss(14, 7)), 1)
            rows.append({"date": d.isoformat(), "station": s, "temp_c": t, "rain_mm": rain,
                         "wind_kmh": wind})
        d += dt.timedelta(days=1)
    idx = r.sample(range(len(rows)), 8)
    for i in idx[:6]:
        rows[i]["temp_c"] = None
    for i in idx[6:]:
        rows[i]["temp_c"] = -99.0
    dup = next(i for i, row in enumerate(rows) if row["station"] == "Riverside" and row["date"] == "2025-06-14")
    rows.insert(dup + 1, dict(rows[dup]))
    return rows


def tables():
    rng = random.Random(SEED)
    people = _people(rng)
    places = _places(rng)
    books = _books()
    members = _members(people)
    return {
        "people": people,
        "streets": _streets(rng),
        "places": places,
        "roads": _roads(places),
        "friendships": _friendships(rng, people),
        "books": books,
        "members": members,
        "loans": _loans(books, members),
        "weather": _weather(),
    }


def write(out=OUT):
    os.makedirs(out, exist_ok=True)
    for name, rows in tables().items():
        with open(os.path.join(out, name + ".csv"), "w", newline="", encoding="utf8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            for row in rows:
                w.writerow({k: ("" if v is None else v) for k, v in row.items()})


def _typed(v):
    if v == "":
        return None
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def load(name, folder=OUT):
    with open(os.path.join(folder, name + ".csv"), encoding="utf8") as f:
        return [{k: _typed(v) for k, v in row.items()} for row in csv.DictReader(f)]


SCHEMA = """
CREATE TABLE streets (street_id INTEGER PRIMARY KEY, name TEXT NOT NULL, postcode TEXT);
CREATE TABLE people (person_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
  birth_year INTEGER, street_id INTEGER REFERENCES streets(street_id));
CREATE TABLE places (place_id INTEGER PRIMARY KEY, name TEXT NOT NULL, kind TEXT, x_m INTEGER, y_m INTEGER);
CREATE TABLE roads (road_id INTEGER PRIMARY KEY, from_place INTEGER REFERENCES places(place_id),
  to_place INTEGER REFERENCES places(place_id), length_m INTEGER, speed_kmh INTEGER, one_way INTEGER);
CREATE TABLE friendships (person_a INTEGER REFERENCES people(person_id),
  person_b INTEGER REFERENCES people(person_id), since_year INTEGER, PRIMARY KEY (person_a, person_b));
CREATE TABLE books (book_id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, year INTEGER,
  genre TEXT, pages INTEGER);
CREATE TABLE members (member_id INTEGER PRIMARY KEY, person_id INTEGER REFERENCES people(person_id),
  joined TEXT);
CREATE TABLE loans (loan_id INTEGER PRIMARY KEY, book_id INTEGER REFERENCES books(book_id),
  member_id INTEGER REFERENCES members(member_id), out_date TEXT, due_date TEXT, return_date TEXT);
CREATE TABLE weather (date TEXT, station TEXT, temp_c REAL, rain_mm REAL, wind_kmh REAL);
"""
ORDER = ["streets", "people", "places", "roads", "friendships", "books", "members", "loans", "weather"]


def to_sqlite(conn, folder=OUT):
    conn.executescript(SCHEMA)
    for name in ORDER:
        rows = load(name, folder)
        cols = list(rows[0])
        conn.executemany(f"INSERT INTO {name} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                         [tuple(r[c] for c in cols) for r in rows])
    conn.commit()
