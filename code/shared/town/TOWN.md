# Brenmoor, the series' invented town (frozen 2026-11-19)

One seeded generator (`code/shared/town/town/__init__.py`, seed 20261119)
writes every table to `data/town/*.csv`; `python -m town` must leave no diff
(`tests/test_town.py` checks the bytes). Nothing is real and nothing is
downloaded. The chapters that use tables (grade 8 files and data tables, grade
10 data tables and graphs, grade 12 SQL and the route planner, Year 1
relational model and later database chapters) read these files or load them
with `town.to_sqlite(conn)` or the `-- load: town` directive of `sqlrun.py`.
A chapter that needs another view writes its own script that imports `town`
and never edits it.

| Table | Rows | Columns | Notes |
|---|---:|---|---|
| `people` | 120 | person_id, first_name, last_name, birth_year, street_id | invented names |
| `streets` | 24 | street_id, name, postcode | postcodes `B-100` … `B-130`, shared by six streets each |
| `places` | 30 | place_id, name, kind, x_m, y_m | map 6 km × 5 km, places at least 400 m apart; `Lighthouse Café` has a non-ASCII letter |
| `roads` | 53 | road_id, from_place, to_place, length_m, speed_kmh, one_way | each place joined to its 3 nearest; lengths 5–35 % above the straight line, multiples of 10 m; **road 1 is one-way** (from 1 to 3); the network is connected |
| `friendships` | 50 | person_a, person_b, since_year | among people 1–40, person_a < person_b; three groups (1–14, 15–27, 28–40) joined by a few bridges; **person 40 has no friend** |
| `books` | 80 | book_id, title, author, year, genre, pages | invented titles and authors |
| `members` | 60 | member_id, person_id, joined | library members |
| `loans` | 400 | loan_id, book_id, member_id, out_date, due_date, return_date | 2025, ordered by date; due 21 days after; some late, **some still out** (`return_date` empty = NULL) |
| `weather` | 731 | date, station, temp_c, rain_mm, wind_kmh | 2025 daily at Hilltop and Riverside; **planted defects:** 6 missing temperatures, 2 readings of −99.0 (an error code), and 2025-06-14 at Riverside recorded twice |

Exact counts printed in a chapter come from a run (a captured output), not
from this table.
