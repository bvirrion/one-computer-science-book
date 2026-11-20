# Book 2 (grades 10–12) — chapter briefs (Phase A, 2026-11-20)

Owned by the Book 2 writer. Binding inputs: `sources/BATCH_BOOKS_1-5.md`, `OUTLINE.md` (chapter list of record,
ownership maps), `sources/SERIES_DEFINITIONS.md`, `CONTRIBUTING.md`, `../book_style.md`. Term ownership details:
`sources/book2/DEFINITIONS.md`. Nothing here is printed; programme names appear in this file only.

## 0. Book-wide decisions

- **35 chapters**: grade 10 (11), grade 11 (10), grade 12 (14). Target ~420 pp → **~12 pp per chapter**
  (course ~7 pp with listings and outputs, exercises ~2 pp, problem ~1.5 pp, solutions ~2.5 pp). Projects ~12–14 pp.
- **Calibration** (gate): exactly 15 exercises, 5★ / 6★★ / 4★★★ in order; one weekend problem of 18–22 top-level
  questions in Parts I–IV ending on a named, quantified result. Projects (`10-11`, `11-10`, `12-14`): 15 exercises,
  no problem, one `\section` per milestone.
- **Mix of kinds** in every chapter's 15 exercises: at least 3 predict-the-output (P), 3 find-and-fix (F),
  3 write-to-a-specification (W, tested file under `exercises/`), 3 prove-or-count (C). Tags below.
- **Register**: proofs of correctness and termination from grade 11 (invariants, variants); costs counted from
  grade 11; the cost of halving counted in grade 11 and called a **logarithm only in grade 12** (recalled from the
  mathematics book's grade 12, where it is `ln`; `\log_2 x = \ln x / \ln 2` is stated as a notation);
  **induction only in grade 12** (recalled from the mathematics book's grade 12 `sequences`); no expected values
  (probability frequencies only as in Book 1 grade 9 simulations).
- **Languages**: Python 3.12 standard library only; toy assembly (`.toy`) in grade 11; SQL through `sqlrun.py` and
  `sqlite3` in grade 12; bash sessions in grade 11 ch. 3 (and grade 12 ch. 10 if `ps` captures deterministically).
  HTML/CSS as markup only (recalled from Book 1 grade 9). JavaScript is described in prose, never listed.
  Test files that the reader sees use `unittest`/`doctest` (standard library); the repo's own `tests/` use pytest.
- **Ports**: 42000–42999. Plan: g10-08 42080–42089, g10-11 42110–42119, g12-12 none (no live TLS), g11-04 none
  (simulated network). Every server binds `127.0.0.1`, starts and stops inside one capture.
- **Data**: the town (`code/shared/town`, frozen) for tables, graphs, SQL and the route planner; seeded generators in
  chapter code for k-NN parcels, text-search strings, sensor readings, routing networks, scheduling workloads.
  **No dataset download is needed anywhere in Book 2.**
- **Visuals**: ~4 schematics per chapter (TikZ: memory/cell diagrams, trees, graphs, automata, circuitikz logic,
  bytefield layouts, generic windows); charts only from a tested `figures/` script's `.dat`; photographs of real
  hardware and historic machines (free licence, licence page read first); a few AI illustrations of everyday scenes
  (grades 10–12 use them sparingly: ~10 in the book).
- **Boxes**: `recall` at the top of every chapter that builds on an earlier notion (3–5 lines, Book 1 named in prose:
  ``as Book 1 showed in grade 8''); `history[...]` boxes carry the programme's transversal history rubric (dates and
  people through the ledger); `dated{2026}` for volatile figures; `safety` for passwords, updates, backups,
  untrusted input; `inpractice[...]` for professional practice (pytest, version numbers, real protocols).
- **Label scheme**: `<type>:g1X:<slug>:<name>`, slug = file slug without `NN-`. Listing stems unique per chapter.
- **Ledger**: `sources/ledger/book2.md`, ids prefixed `g10:` / `g11:` / `g12:` or by standard (`rfc9110:` …);
  check `sources/data_ledger.md` and other books' ledgers before minting. Expected ~150 rows, ~250 fetches.

## 1. Programme coverage (checked 2026-11-20 against the published texts)

Texts read (fetched as data; copies in the scratchpad, not in the repo):
- **SNT seconde** — the programme annex as published with the arrêté of January 2019 (the copy read is the
  pre-publication arrêté with its annex, hosted by a teachers' union, `snes.edu/.../arrete_snt_2e_ensemble.pdf`;
  the BO page `education.gouv.fr/bo/19/Special1/MENE1901641A.htm` and eduscol returned 403/redirected to another
  subject, so the wording was checked on that copy). Seven themes + transversal programming notions.
- **NSI première** — eduscol `document/30007` (annex of BO spécial n°1, 22 January 2019, MENE1901633A).
- **NSI terminale** — eduscol `document/30010` (annex of BO spécial n°8, 25 July 2019, MENE1921247A).
- **Mathematics seconde, "Algorithmique et programmation"** — `snes.edu/.../arrete_maths_2egt_ensemble.pdf`
  (types, assignment, conditionals, bounded/unbounded loops, functions, random functions): all owned by Book 1
  (grades 6–9); nothing for Book 2 to add.

Per chapter, the items covered (S = SNT, P = NSI première, T = NSI terminale). Items marked **(add)** are not in the
outline's one-line description and are added to the brief as a section, remark or exercise (no chapter changes).

| Ch. | Programme items covered |
|---|---|
| g10-01 specifications-and-tests | P *Spécification* (prototype, preconditions, postconditions, assertions); P *Mise au point* (test sets; a passing suite does not prove correctness); T *Gestion des bugs* — **(add)** a catalogue of typical bug causes (typing, unwanted side effects, index out of range, non-exhaustive `if`, wrong inequality, float comparison, bad names); P *Booléens* — **(add)** the sequential (short-circuit) evaluation of `and`/`or` |
| g10-02 tuples-sets-comprehensions | P *p-uplets, p-uplets nommés* (a function returning a tuple; **(add)** named tuples); P *Tableau donné en compréhension*; T side effects (aliasing) |
| g10-03 machine-integers | P *Écriture d'un entier dans une base b ≥ 2* (recalled from Book 1 g8, extended to any base); P *Représentation binaire d'un entier relatif* (bits needed for a number, a sum, a product; sizes 8/16/32/64; two's complement; Python's arbitrary-size integers); P xor and binary addition |
| g10-04 floating-point | P *nombre flottant* (0.1, 0.25, 1/3 by hand; 0.1 + 0.2 ≠ 0.3; never test equality); T float comparisons as a bug cause |
| g10-05 text-encodings | P *Représentation d'un texte* (ASCII, ISO-8859-1, Unicode; converting a text file between encodings) |
| g10-06 images-sound-compression | S *Photographie numérique* (photosites vs pixels, sensor and image resolution, colour depth, EXIF metadata, **(add)** the camera's processing chain: colour filter mosaic and demosaicing, told + a small program); S *Métadonnées*; P EXIF data as a record |
| g10-07 data-tables | S *Données structurées* (descriptors vs values, formats; search, filter, sort, compute over one or several tables); P *Traitement de données en tables* (import CSV, search with Boolean criteria, duplicates and consistency tests, sort on a column, merge two tables, domain of values); S personal data — **(add)** a short remark defining personal data, technical angle only |
| g10-08 http-clients-servers | S *Le Web* (URL decomposed, secure pages recognised, HTTP request decomposed with its parameters, client/server, what runs where; browser settings for cookies as a `safety` box; **(add)** a `history` box on the web's development); P *Interactions homme–machine sur le Web* (events and graphical components of a page **told**, JavaScript described not taught; client vs server; what the client stores and resends — cookies; when the transmission is encrypted; forms; **GET vs POST** explicit) |
| g10-09 graphs-first-look | S *Réseaux sociaux* (graph of friends; **(add)** eccentricity, **radius, diameter and centre** of a graph; small-world remark with a `history` box on the 1967 letter experiment); S *Localisation* (route computation as a graph problem; satellite positioning recalled from the Earth series; **(add)** decoding one NMEA 0183 position sentence as an exercise, see ledger) |
| g10-10 sensors-actuators-control | S *Informatique embarquée et objets connectés* (control algorithms from sensor data, HMI of a connected object, programs that acquire data or command an actuator); P *Périphériques d'entrée et de sortie* (role of sensors and actuators; an HMI to a given specification) |
| g10-11 project-web-application | S *Le Web* and P web interaction as a project; T project practice (milestones, tests) |
| g11-01 gates-to-arithmetic-unit | P combinational circuits realise Boolean functions; binary addition by gates (xor) |
| g11-02 von-neumann-machine | P *Modèle d'architecture séquentielle* (components and roles, single- and multi-processor; running machine-language instructions by hand); T *Composants intégrés d'un système sur puce* — **(add)** a closing section on the system on a chip (components on a diagram, why integration saves time and energy) |
| g11-03 os-and-command-line | P *Systèmes d'exploitation* (functions of an OS, basic commands, rights and permissions, free vs proprietary systems; a free system is used) |
| g11-04 network-protocols | P *Transmission de données dans un réseau* (packets, encapsulation, the alternating-bit protocol, simulating a network); S *Internet* (roles of IP and TCP, reliability without timing guarantee, symbolic addresses and DNS recalled from Book 1 g8, **(add)** peer-to-peer networks as a remark, physical network kinds and traffic orders of magnitude in a `dated` box) |
| g11-05 proving-algorithms-correct | P invariants for insertion and selection sort; P termination of binary search by a variant; P terminations of sorts |
| g11-06 cost-of-an-algorithm | P linear cost of a sequential scan; quadratic worst case of the two sorts; T the gain from n² to n log₂ n and from n to log₂ n (here: counted halvings) |
| g11-07 greedy-algorithms | P *Algorithmes gloutons* (knapsack, change-making) |
| g11-08 k-nearest-neighbours | P *k plus proches voisins* (predict the majority class of the k nearest neighbours; a learning algorithm) |
| g11-09 modules-and-interfaces | P *Utilisation de bibliothèques* (reading a library's documentation); T *Modularité* (APIs and libraries, documentation, simple modules documented); T interface vs implementation (shared with g12-03); P *Diversité et unité des langages* — partial, see g12-13 |
| g11-10 project-toy-machine | P running machine-language instructions; T program as data (a program that reads programs) |
| g12-01 recursion | T *Récursivité* (write and analyse a recursive program); P/T termination by a variant for recursive functions |
| g12-02 classes-and-objects | T *Vocabulaire de la programmation objet* (class, attributes, methods, objects); T *Paradigmes de programmation* — **(add)** a closing section: the same small task in imperative, functional and object style, and how to choose (inheritance kept as a first look, polymorphism not developed) |
| g12-03 lists-stacks-queues | T *Structures de données, interface et implémentation* (several implementations of one structure; **the queue with two stacks**); T *Listes, piles, files* (LIFO/FIFO; choosing a structure; **(add)** searching a value in a list vs in a dictionary, measured) |
| g12-04 trees | T *Arbres* (situations needing a tree; size; **bounds on the height**; traversals in four orders; search and insertion in a BST; logarithmic cost when balanced) |
| g12-05 graph-algorithms | T *Graphes* (adjacency matrix recalled, successor/predecessor lists, converting between them); T *Algorithmes sur les graphes* (DFS, BFS, cycle detection, finding a path; a maze; graphs written as classes) |
| g12-06 divide-and-conquer | T *Diviser pour régner* (quarter-turn rotation of a bitmap in constant memory; merge sort n log₂ n in the worst case) |
| g12-07 dynamic-programming | T *Programmation dynamique* (alignment of sequences, change-making; memory cost discussed) |
| g12-08 text-search | T *Recherche textuelle* (Boyer–Moore, here in Horspool's simplified form; interest of preprocessing; cost not required — measured, not proved, beyond the worst case of the naive search) |
| g12-09 relational-databases-sql | T *Bases de données* (relation, attribute, domain, primary and foreign keys, relational schema; integrity constraints of domain, relation and reference; structure vs content; anomalies of redundancy, insertion, deletion, update; DBMS services: persistence, concurrent access, efficient queries, access security — described, not detailed; SQL SELECT/FROM/WHERE/JOIN, DISTINCT, ORDER BY, aggregate functions **without GROUP BY/HAVING**, INSERT/UPDATE/DELETE; SQL combined with Python) |
| g12-10 processes-and-scheduling | T *Gestion des processus et des ressources* (creating a process, scheduling several processes, deadlock risk; observing active and waiting processes with a standard tool; **(add)** interrupts, which the programme's introduction names) |
| g12-11 routing | T *Protocoles de routage* (route of a packet from given tables, by hop count (RIP) or by route cost (OSPF); link with path-finding on graphs) |
| g12-12 secure-communication | T *Sécurisation des communications* (symmetric and asymmetric principles; exchanging a symmetric key with an asymmetric protocol to secure HTTPS; cipher negotiation is not studied) |
| g12-13 halting-problem | T *Notion de programme en tant que donnée; calculabilité, décidabilité* (every program is data; computability does not depend on the language; the halting problem is undecidable, without formalism); P *Diversité et unité des langages* — **(add)** one section "one algorithm, several languages": Euclid's algorithm in Python, in toy assembly, and as an SQL recursive query, read side by side |
| g12-14 project-route-planner | T project themes "route finding on a map", "web site with a database" (SQL + graph + class); T modularity |

**Items no chapter covers** (deliberately, by the series' rules — proposed to stay uncovered):
- S *Réseaux sociaux*: digital identity, e-reputation, existing networks and their subscriber counts, their economic
  model, cyber-violence and the penal-code article; S *Le Web*: legal notions (licence, copyright, right of use),
  critical reading of search results, "every query leaves traces"; S *Localisation*: using map services and
  contributing to a collaborative map, phone privacy settings; S *Données*: using an open-data site (**no downloads**),
  using cloud storage, sharing and syncing files. These are digital-citizenship or online-service items; the outline
  keeps technical content only and forbids online services. What is technical in them is kept: authentication and
  passwords (`safety` box in g10-08, key pairs in g12-12), data-centre energy in a `dated` box (g10-07), cloud
  storage described in prose (g11-03, a file system on another machine), search-engine ranking from links as an
  exercise (g10-09).
- S *Internet*: "on real examples, find an IP address from a symbolic address and back" — needs a live DNS query
  (an online service). Proposed: the name system is recalled from Book 1 g8 and exercised on a **local** hosts-style
  table (g11-04); no live lookup.
- P/T *Histoire de l'informatique* is transversal: carried by `history` boxes (Turing 1936, EDVAC report 1945,
  first stored-program machines 1948, the ARPANET 1969, the web 1989–91, Unicode 1991, IEEE 754 1985, Dijkstra 1959,
  Codd 1970, Diffie–Hellman 1976, RSA 1977, Boyer–Moore 1977 / Horspool 1980), every date through the ledger.
- T *the evolution of the roles of software and hardware*: one `history` box in g11-02 (from wired programs to stored
  programs to systems on a chip designed in software).

## 2. Chapter briefs

Conventions in each brief: **Sections** (3–5 + Exercises + Problem); **Owns** (terms; labels in DEFINITIONS.md);
**Recalls**; **Listings** (stem — what it shows — captured output); **Figures** (S = schematic, P = photograph,
AI = illustration, C = chart from `figures/`); **Exercises** (★/★★/★★★ with kind P/F/W/C); **Problem**; **Ledger**.

### Grade 10

#### g10-01 Specifications, Assertions and Tests — `specifications-and-tests` (~12 pp)
- **Hook**: a function that "works" on the three cases its author tried and fails on a leap year.
- **Sections**: 1 What a function promises (specification, signature, precondition, postcondition, docstring);
  2 Assertions (`assert`, checking a precondition, short-circuit evaluation of `and`/`or` as a guard
  `i < len(t) and t[i] == x`); 3 Choosing test cases (ordinary, boundary, invalid; one test per branch; a passing
  suite is not a proof); 4 Tests run automatically (`unittest` file, `doctest`; a failing test as a bug report;
  `inpractice[pytest]`); 5 Where bugs come from (a catalogue: wrong type, side effect on an argument, index out of
  range, non-exhaustive `if`, `<` for `<=`, float equality, a misleading name).
- **Recalls**: function (Book 1 g7 `functions`), kinds of error and tracing (Book 1 g7 `finding-and-fixing-bugs`),
  Boolean values (Book 1 g6 `if-else`).
- **Listings**: `leap_year.py` (spec + docstring + first faulty version) → output of 3 calls; `leap_year_fixed.py`;
  `guard.py` (short-circuit guard vs crash) → output incl. a staged `IndexError` traceback; `assert_pre.py`
  (precondition assert fires) → staged `AssertionError` (`# capture: exit`); `test_leap.py` (unittest, 8 cases) →
  `python -m unittest` output with one failure on the faulty version then all OK; `doctest_mean.py` → doctest report;
  `bug_catalogue.py` (seven short functions, each with its bug) — NORUN, used by exercises.
- **Figures**: S partition of the input space into classes with boundary points marked (leap-year: ÷4, ÷100, ÷400 as
  nested sets); S the contract picture: caller ↔ function, pre before, post after; S test runner flow (tests → run →
  pass/fail report); C none. AI: none.
- **Exercises**: ★ P doctest output; ★ P short-circuit prints; ★ W docstring + pre/post for `max_of`; ★ C count the
  boundary cases of `clamp(x, lo, hi)`; ★ F `<` vs `<=` in a grade function; ★★ F mutated argument (side effect);
  ★★ W unittest suite for `days_in_month`; ★★ P which tests fail on a buggy `is_sorted`; ★★ C why no finite suite
  proves `is_prime` (argument); ★★ F non-exhaustive `if`; ★★ W precondition asserts for `average(t)`;
  ★★★ C count the paths through nested ifs → minimal branch-covering suite; ★★★ W `roman(n)` to spec with suite;
  ★★★ F float comparison bug, fix with tolerance (forward pointer to g10-04); ★★★ C mutants: which planted
  mutants of `leap_year` survive a given suite.
- **Problem** "The mutants of the leap year": Part I specify `leap_year`; II design boundary suite; III generate the
  single-operator mutants (code) and run the suite on each; IV random suite vs boundary suite. **Named result**: the
  number of mutants killed by the boundary suite vs by 100 random years (counts from a run, `exercises/` file).
- **Ledger**: Gregorian leap-year rule (source: a primary calendar reference, e.g. the papal bull / a standards
  page — or treat as specification given, no row); Python `unittest`/`doctest` docs (PYTHON-DOCS page rows only if a
  version fact is printed).

#### g10-02 Tuples, Sets and Comprehensions — `tuples-sets-comprehensions` (~12 pp)
- **Hook**: two library members ask "which books have we both read?" — a list answer repeats titles and is slow.
- **Sections**: 1 Tuples (packing, unpacking, returning several values, swapping; named tuples as records);
  2 Mutable and immutable values (identity vs value, `is` vs `==`, two names for one list = alias, copying: `list()`,
  slicing, nested copy problem); 3 Sets (membership, union, intersection, difference, no order, no duplicates;
  elements must be immutable); 4 Comprehensions (list, set, dict; with a condition; nested; when a loop is clearer).
- **Recalls**: list (Book 1 g7), dictionary and record (Book 1 g8), sets of the mathematics book named in prose
  (the mathematics book's Year 1 owns sets formally; here the Python type only).
- **Listings**: `swap.py`, `min_max.py` (function returning a tuple) → outputs; `point.py` (namedtuple) → output;
  `alias.py` (alias surprise) → output; `copy_nested.py` (shallow copy trap) → output; `shared_books.py` (town loans:
  sets of book ids per member, intersection) → output; `comprehensions.py` → output; `tuple_key.py` (tuples as dict
  keys; a list as a key raises `TypeError`, staged) → output.
- **Figures**: S memory diagram: names → objects, alias vs copy (cells + `ptr`); S shallow vs deep copy of a list of
  lists; S Venn diagram of two members' reading sets with counts from the run; S comprehension read as
  "for … if … → expression" annotated.
- **Exercises**: ★ P unpacking; ★ P set ops; ★ W `min_max`; ★ P alias; ★ C size of a union from sizes and
  intersection; ★★ F tuple of one element `(x)`; ★★ W `common_books(a, b)` with sets; ★★ F mutable default /
  shared inner list `[[0]*3]*3`; ★★ P dict comprehension; ★★ C number of subsets of a 4-set listed by a comprehension;
  ★★ W `distinct_authors(town books)`; ★★★ C count comparisons: list-based vs set-based intersection (by reasoning,
  then measured in g11-06); ★★★ W `transpose` by nested comprehension; ★★★ F aliasing bug in a grid copy;
  ★★★ W Jaccard similarity of two members.
- **Problem** "Readers alike": I sets of books per member from loans; II intersection and union sizes; III Jaccard
  index for all pairs (comprehension); IV the closest pair. **Named result**: the pair of members with the highest
  Jaccard similarity and its value (from a run on the town).
- **Ledger**: none expected (Python semantics are docs facts: rows only if a version-specific behaviour is printed).

#### g10-03 Integers in the Machine — `machine-integers` (~13 pp)
- **Hook**: an old step counter that showed 0 after a long walk.
- **Sections**: 1 Unsigned integers on n bits (any base b ≥ 2, recalled conversions; range 0…2ⁿ−1; bits needed for a
  number, a sum, a product; 8/16/32/64; overflow as wrap-around modulo 2ⁿ, simulated with `% 2**n`); 2 Signed integers
  in two's complement (range −2ⁿ⁻¹…2ⁿ⁻¹−1; negating = flip and add one; why one adder serves both; overflow of signed
  sums detected by signs); 3 Bitwise operations (`&`, `|`, `^`, `~`, `<<`, `>>`; masks to test, set, clear a bit;
  shifts as ×2 and ÷2; xor swap and parity); 4 Python's integers never overflow (arbitrary size, `int.bit_length`),
  most languages' do (`dated`/`inpractice` box: fixed widths elsewhere, told; the 2038 problem as history).
- **Recalls**: binary, hexadecimal, base conversion, binary addition (Book 1 g8 `binary-and-hexadecimal`); bits and
  bytes (Book 1 g5); powers of two (mathematics, grade 8).
- **Listings**: `to_base.py` (any base) → output; `bits_needed.py` (bit_length of n, a+b, a×b) → output;
  `wrap.py` (simulated 8-bit and 16-bit counters) → output; `twos.py` (encode/decode n-bit two's complement table for
  n = 4) → output; `masks.py` (test/set/clear bits; RGB from a 24-bit colour) → output; `big_int.py` (2**100,
  factorial 30) → output; `toy_wrap.toy` (250 + 10 on the toy machine, flag C) via `python -m toymachine run --dump`
  → output (a first glimpse; the machine is g11's).
- **Figures**: S the 4-bit two's-complement wheel (16 values on a circle, overflow crossing); S bit layout of an
  8-bit byte with weights −128…1; S mask operations as aligned rows (value, mask, result); S RGB 24-bit colour as
  three bytes (bytefield).
- **Exercises**: ★ P `bin`/`hex`; ★ C range of 12-bit unsigned; ★ C two's complement of −5 on 8 bits; ★ P shifts;
  ★ W `to_base(n, b)`; ★★ C bits for a product of a 20-bit and 13-bit number; ★★ F decode bug (sign bit ignored);
  ★★ W `set_bit`, `clear_bit`, `test_bit`; ★★ C signed overflow of 100 + 50 on 8 bits; ★★ P xor swap trace;
  ★★ F mask with wrong shift; ★★★ C prove −x = ~x + 1 on n bits; ★★★ W `popcount` by `x & (x−1)` with a count of
  steps; ★★★ C why sum overflow ⇔ operands same sign, result different; ★★★ W `add_n_bits(a, b, n)` returning
  result and carry/overflow flags.
- **Problem** "The 2038 rollover": I seconds since an epoch, signed 32-bit storage; II largest value; III the date it
  overflows (Python `datetime`); IV the value read after the wrap and the date it shows. **Named result**: the
  overflow instant 2038-01-19 03:14:07 UTC and the wrapped date 1901-12-13 20:45:52 (computed by the code).
- **Ledger**: POSIX epoch definition (1970-01-01T00:00:00Z) — The Open Group Base Specifications ("Seconds Since the
  Epoch"); fixed integer widths of C (`int32_t`) — CPPREF; Python `int` unbounded — PYTHON-DOCS (numeric types).

#### g10-04 Floating-Point Numbers — `floating-point` (~13 pp)
- **Hook**: `0.1 + 0.2 == 0.3` prints `False`.
- **Sections**: 1 Binary fractions (place values ½, ¼, …; 0.25 exact, 0.1 and 1/3 periodic, conversion by doubling);
  2 Sign, exponent and significand (scientific notation in base 2; the 64-bit format: 1 + 11 + 52 bits, bias,
  `float.hex`, `struct` to see the bits; a toy 8-bit format to compute every value by hand); 3 Gaps between neighbours
  (spacing doubles at each power of two, `math.ulp`, `math.nextafter`, machine epsilon, the largest exactly
  representable integer 2⁵³); 4 Rounding error and how it builds up (summing 0.1 ten times; order of summation;
  `math.fsum`; catastrophic cancellation, told on one example); 5 Comparing floats and special values
  (`math.isclose`, absolute and relative tolerance; `inf`, `-inf`, `nan`, `nan != nan`, signed zero).
- **Recalls**: scientific notation (mathematics grade 9 / physics grade 10, named in prose); binary (Book 1 g8);
  g10-03 fixed widths.
- **Listings**: `point_one.py` → output; `to_binary_fraction.py` (doubling method, first 30 bits of 0.1) → output;
  `float_bits.py` (`struct.pack('>d')` fields of 0.1, 1.0, −2.5) → output; `toy_float.py` (all positive values of a
  1+3+4 toy format) → output (and `.dat` for the figure, in `figures/`); `gaps.py` (`math.ulp` at 1, 2**52, 2**53)
  → output; `sum_tenths.py` (sum of 10 / 10⁶ tenths, plain vs `fsum`) → output; `cancel.py` → output;
  `compare.py` (`isclose`, special values) → output.
- **Figures**: C the toy format's values on a number line (uneven spacing) from `figures/toy_float_points.py`;
  S bytefield of the 64-bit layout (1|11|52) with 0.1's bits; S the doubling method laid out as a table;
  S neighbouring doubles around 1 and around 2 (gap doubling).
- **Exercises**: ★ P `0.1*3`; ★ C 0.375 in binary; ★ C 1/3 in binary (period); ★ P `isclose`; ★ F `==` on floats in a
  loop that never stops; ★★ C value of a given 64-bit pattern; ★★ W `binary_fraction(x, n)`; ★★ C gap at 2²⁰;
  ★★ P order of summation; ★★ F accumulating `t += 0.1` vs `t = k * 0.1`; ★★ W `almost_equal` with both tolerances;
  ★★★ C prove 2⁵³ + 1 is not representable; ★★★ C count values of the toy format; ★★★ W solving a quadratic with the
  stable formula vs the naive one (cancellation measured); ★★★ F `nan` in a max computation.
- **Problem** "A clock that drifts": I a tenth of a second stored in a 24-bit fixed-point register (chopped);
  II the error per tick; III error after 100 hours of ticks; IV the distance a target at a given speed moves in
  that time. **Named result**: a drift of about 0.34 s after 100 hours (computed exactly by the code from the
  chopped value), compared with the published figure (ledger).
- **Ledger**: IEEE 754-2019 binary64 widths (1/11/52, bias 1023) — IEEE standard page or Python `sys.float_info`
  docs + a primary description; year of the first IEEE 754 standard (1985); the 1991 clock-drift incident: GAO
  report IMTEC-92-26 (0.34 s after 100 h, 24-bit register) — fetch the report page.

#### g10-05 Text Encodings: From ASCII to UTF-8 — `text-encodings` (~12 pp)
- **Hook**: a town café's name prints as `Lighthouse CafÃ©` on a notice board.
- **Sections**: 1 Code point versus bytes (character, code point, encoding, a text file is bytes); 2 ASCII on 7 bits
  (the table's structure: control characters, digits, letters 32 apart; `ord`/`chr`); 3 One-byte extensions and their
  conflicts (ISO-8859-1, another 8-bit table, the same byte read two ways); 4 Unicode and UTF-8 (U+ notation, planes
  told; UTF-8's 1–4-byte patterns decoded by hand; self-synchronisation; UTF-16 told); 5 Garbled text explained and
  bytes in Python (`str` vs `bytes`, `encode`/`decode`, errors, opening a file with an encoding, converting a file).
- **Recalls**: character code (Book 1 g5), string, `ord` (Book 1 g7 `strings`), hexadecimal (Book 1 g8).
- **Listings**: `ascii_table.py` (32–126 in rows) → output; `ord_chr.py` → output; `latin1_vs_utf8.py` → output;
  `utf8_by_hand.py` (encode a code point with bit operations, check against `.encode`) → output; `mojibake.py`
  (double decoding of "Café") → output; `convert_file.py` (Latin-1 file → UTF-8 file, sizes) → output;
  `decode_error.py` (staged `UnicodeDecodeError`) → output; `town_names.py` (bytes of the place `Lighthouse Café`).
- **Figures**: S the ASCII table as a 8×16 grid (control / printable regions coloured); S UTF-8 byte patterns
  (bytefield rows for 1, 2, 3, 4 bytes) with x-bits; S one string, three encodings: bytes laid out side by side;
  S the mojibake path é → C3 A9 → read as Latin-1 → Ã © ; P a teleprinter of the 1960s (Commons, free licence,
  historic machine) for the history box.
- **Exercises**: ★ P `ord('A')`, `chr(97)`; ★ C bytes of "été" in UTF-8 and Latin-1; ★ P `len` of str vs bytes;
  ★ C letters A and a differ by one bit; ★ W `is_ascii(s)`; ★★ C decode a given UTF-8 byte sequence by hand;
  ★★ W `utf8_length(code_point)`; ★★ F reading a UTF-8 file as Latin-1; ★★ P `errors='replace'`; ★★ C how many code
  points fit in 2-byte UTF-8; ★★ F slicing bytes mid-character; ★★★ W `utf8_encode(cp)` by hand with tests against
  Python; ★★★ C prove a continuation byte can never be taken for a first byte; ★★★ W `fix_mojibake(s)` (one level);
  ★★★ C file sizes of a text in three encodings.
- **Problem** "The notice board": I decode a byte dump; II find which encoding was used; III undo two layers of
  mojibake; IV count bytes of the town's place names in UTF-8 vs UTF-16 vs Latin-1. **Named result**: the size saved
  by UTF-8 over UTF-16 on the town's names (from a run) and the rule "é becomes Ã©".
- **Ledger**: ASCII (ANSI X3.4-1968 / RFC 20) 7-bit, year; ISO/IEC 8859-1 (year, coverage) — via a primary page
  (ISO catalogue or the IANA charset registry); Unicode: code space 0–10FFFF, version 1.0 year 1991, current version
  number (`dated`); UTF-8: RFC 3629 (byte patterns, max 4 bytes, year 2003); UTF-16 surrogates (Unicode ch. 3).

#### g10-06 Digital Images, Sound and Compression — `images-sound-compression` (~13 pp)
- **Hook**: a phone photo of the town square is 4 MB; the same picture sent in a message is 300 KB and looks the same.
- **Sections**: 1 From a scene to pixels (photosites of the sensor vs pixels of the image; the colour filter mosaic
  and demosaicing by averaging neighbours, told + small program; resolution of sensor and image; colour depth;
  raw size = width × height × bytes per pixel); 2 Sound as numbers (sampling a signal at a rate, quantising each
  sample on a bit depth — told, physics named; size per second; a WAV file written with `wave`); 3 Compression without
  loss (run-length coding implemented and measured; a dictionary method told; compressed size depends on the data;
  `zlib` measured on text vs noise); 4 Compression with loss (what is thrown away: fewer colours, fewer samples, fine
  detail — told; a quantisation demo on grey levels); 5 Metadata (a file's own data about itself; EXIF fields as a
  record, told; reading the header of the chapter's own PPM/WAV files).
- **Recalls**: pixel, red–green–blue (Book 1 g5); grid image, plain-text image file (Book 1 g9 `grids-and-images`);
  byte units (Book 1 g4); signals (physics, grade 10, named in prose; sampling theorem not re-taught).
- **Listings**: `raw_size.py` → output; `demosaic.py` (4×4 mosaic → RGB by averaging, printed as grids) → output;
  `make_wav.py` (one second of a 440 Hz tone, 8 kHz, 8-bit; prints header fields and size) → output;
  `samples.py` (first samples; `.dat` written by `figures/`); `rle.py` (encode/decode, ratio on a drawn map row and on
  noise) → output; `zlib_sizes.py` → output; `quantise.py` (256 → 8 grey levels, error) → output;
  `read_header.py` (PPM and WAV headers as records) → output.
- **Figures**: S colour filter mosaic over photosites and the demosaicing neighbourhood; C sampled and quantised sine
  (staircase over the curve) from `figures/samples_plot.py`; S RLE of one image row (pixels → (count, value) pairs);
  S lossless vs lossy pipeline diagram; P an image sensor chip (Commons) or a historic first digital image (if a
  free-licence scan exists, read licence); AI a person photographing a market square with a phone (no brand).
- **Exercises**: ★ C raw size of 4000×3000 RGB; ★ C bytes per second of 16-bit stereo at a given rate; ★ P RLE of a
  string; ★ P `zlib` order of sizes; ★ W `rle_decode`; ★★ F RLE bug on the last run; ★★ C when RLE makes a file bigger
  (worst case 2×); ★★ W grey-level histogram of a PGM; ★★ C colours with 5-6-5 bits; ★★ F demosaic edge index error;
  ★★ W `wav_duration(path)` from header fields; ★★★ C prove no lossless method shrinks every file (counting
  argument, pigeonhole); ★★★ W RLE on a bitmap row-by-row with ratio; ★★★ C quantisation error bound (half a step);
  ★★★ F a sampled tone at the wrong rate (aliasing shown as a measured frequency, told).
- **Problem** "A minute of music": I sampling rate and bit depth of a disc-quality recording; II bytes per second
  and per minute; III a three-minute song's size; IV RLE and zlib on its samples (incompressible) vs on silence.
  **Named result**: one minute of disc-quality stereo is 10,584,000 bytes ≈ 10.1 MiB (computed), and why lossless
  compression barely helps on music.
- **Ledger**: audio CD 44,100 Hz, 16-bit, 2 channels (IEC 60908 — via a primary description); WAV/RIFF header
  layout (a primary spec page: Microsoft RIFF / Library of Congress format description); PPM/PGM format (Netpbm
  docs); EXIF standard (CIPA DC-008, JEITA) — field names printed; DEFLATE RFC 1951 (zlib), year; typical phone
  sensor resolutions in a `dated{2026}` box.

#### g10-07 Processing Data Tables — `data-tables` (~13 pp)
- **Hook**: the town's two weather stations disagree on 14 June; which reading is true?
- **Sections**: 1 A table as records under a header (descriptors vs values, domain of a column, CSV read with `csv`
  into a list of dicts, types converted); 2 Selection, projection, sorting on a key (`sorted(key=…)`, stability
  remarked, several keys); 3 Grouping and aggregating (count, sum, mean, median per group; mean and median recalled
  from the mathematics book); 4 Joining two tables on a shared column (loans ⋈ books ⋈ members; nested-loop join vs
  dict index); 5 Missing and inconsistent data (planted defects of the weather table: missing values, −99.0 error
  codes, a duplicate; consistency tests; duplicates detection) and a nested text format (JSON with `json`).
- **Recalls**: dictionary, record, table of records, text file (Book 1 g8 `dictionaries`, `files-and-data-tables`);
  mean, median, spread (mathematics grade 10).
- **Listings**: `load_weather.py` → output (counts, first rows); `select_project.py` → output; `sort_key.py` →
  output; `group_mean.py` (monthly mean per station) → output; `join_loans.py` (titles of books still out) → output;
  `join_index.py` (same with a dict index; comparison count) → output; `clean_weather.py` (find the 6 missing, 2 −99,
  1 duplicate; corrected means) → output; `to_json.py` (a member with nested loans) → output.
- **Figures**: S a table with header, row, column, cell labelled; S selection vs projection as highlighted rows /
  columns; S join of two small tables with matching key lines; C monthly mean temperature per station from
  `figures/monthly_means.py` (before/after cleaning).
- **Exercises**: ★ P selection result count; ★ P `sorted` with key; ★ W `project(table, cols)`; ★ C size of a join of
  given tables; ★ F `int` conversion forgotten (string sort "10" < "9"); ★★ W `group_count(table, col)`; ★★ F duplicate
  detection misses because of whitespace; ★★ P stable sort on two keys; ★★ W `median_by(table, group, col)`; ★★ C
  nested-loop join comparisons n·m vs index n+m; ★★ F a mean that includes −99.0; ★★★ W `left_join` keeping members
  with no loan; ★★★ C prove sorting by key2 then stably by key1 sorts by (key1, key2); ★★★ W consistency checker
  (due = out + 21 days, return ≥ out) over loans; ★★★ W JSON export and re-import round-trip test.
- **Problem** "The corrected weather record": I load and count; II detect the planted defects; III decide a cleaning
  rule for each; IV recompute the year's mean temperature per station and the warmest month. **Named result**: the
  corrected 2025 mean temperature at Hilltop and the error the −99.0 codes would have caused (from a run).
- **Ledger**: CSV RFC 4180 (year); JSON RFC 8259 (year); data-centre electricity share in a `dated{2026}` box (IEA
  report page) — only if printed; "personal data" definition: GDPR Art. 4(1) (EUR-Lex page) — prose definition
  sourced, no law named beyond "data protection law" if the gate allows; else omit.

#### g10-08 The Web: Clients, Servers and HTTP — `http-clients-servers` (~14 pp)
- **Hook**: typing an address and seeing a page takes a dozen exchanged messages; we read them.
- **Sections**: 1 The parts of an address (scheme, host, port number, path, query, fragment; `urllib.parse`);
  2 A request and its response (request line, headers, blank line, body; status line, status codes by class;
  a server written with `http.server` on 127.0.0.1 logs what it receives; a client with `urllib.request`);
  3 Forms and parameters (GET puts them in the address, POST in the body; which to choose: size, confidentiality,
  repeating a request; percent-encoding); 4 Cookies and sessions (`Set-Cookie`, the client stores and resends; a
  visit counter; session id; `safety` box: browser cookie and privacy settings, described generically); 5 What runs
  where (server code vs browser; events and handlers of a page's buttons described, JavaScript named and told, not
  listed; HTTPS: the transmission is encrypted, the padlock recalled from Book 1 g9, details in g12-12).
- **Recalls**: client and server, packet, address, name system (Book 1 g8 `how-the-internet-works`); browser, web page,
  link (Book 1 g5); HTML and CSS (Book 1 g9 `html-and-css`).
- **Listings**: `parse_url.py` → output; `server_hello.py` (NORUN module: a handler class) + `fetch_once.py` (starts
  the server on 127.0.0.1:42080 as a subprocess with `subprocess.Popen` — one thread per process — fetches, stops
  it) → output with the request lines logged by the server and the response headers;
  `status_codes.py` (200, 404, 303 redirect from our server) → output; `form_get_post.py` → output (two requests,
  where the parameters travel); `cookie_counter.py` → output (three visits, counter in the cookie);
  `percent.py` → output; `page.html` (the form page, NORUN, printed as markup).
- **Figures**: S anatomy of a URL with bracketed parts; S sequence diagram client ↔ server (request, response, then
  CSS and image requests); S a request and a response as annotated text blocks (bytefield-like); S generic browser
  window (`pic {window}`) showing the form page drawn from `page.html`; AI none or a person at a laptop (optional).
- **Exercises**: ★ C split a URL; ★ P status class of a code; ★ P which parameters a GET sends; ★ P cookie after two
  visits; ★ W `query_params(url)`; ★★ F handler forgets the blank line / Content-Length; ★★ W a route returning 404 for
  unknown paths; ★★ C bytes of a request; ★★ F password sent by GET (fix: POST + HTTPS); ★★ P percent-encoding of
  "café & co"; ★★ W a server route that returns the sum of two parameters; ★★★ C count requests and round trips for a
  page with 3 images and 1 stylesheet; ★★★ W session store: id in cookie, data on the server; ★★★ F a redirect loop;
  ★★★ C why a GET must not change data (a crawler follows every link): argue with an example.
- **Problem** "What one page costs": I one page, its resources; II requests and bytes from the server log; III round
  trips with a given latency, sequential vs reusing a connection; IV caching with a validator (told: 304). **Named
  result**: the page's load time in round trips and milliseconds for the given latency (computed from the log).
- **Ledger**: HTTP semantics RFC 9110 (methods, status code classes, 2022); HTTP/1.1 RFC 9112 (message syntax);
  URI RFC 3986 (generic syntax); cookies RFC 6265; IANA ports 80 and 443; the web's development: proposal 1989,
  first site 1991 (CERN pages); HTML form submission (WHATWG-HTML).

#### g10-09 Graphs: Networks of Roads and People — `graphs-first-look` (~13 pp)
- **Hook**: who in Brenmoor can pass a message to everyone fastest?
- **Sections**: 1 Vertices and edges (graph, undirected/directed, weighted; degree; the town's friendships and roads);
  2 Paths and distance (path, length, distance, connected graph, connected components; person 40 alone);
  3 A graph in Python (dictionary of neighbours, a set per vertex; reading `friendships.csv` and `roads.csv`; checking
  symmetry); 4 The shortest route found by hand (on a small weighted map: extending a frontier, by hand only — the
  algorithm is g12's); 5 Radius, diameter and centre (eccentricity by hand on small graphs and by a given function
  on the town; small world as a remark and a `history` box; satellite positioning recalled from the Earth series:
  a receiver gets its position, a map is a graph; one NMEA sentence decoded as an exercise).
- **Recalls**: dictionary (Book 1 g8); satellite positioning (the Earth and space sciences book, grade 9).
- **Listings**: `load_friends.py` → output (vertices, edges, degrees, isolated person 40); `degree_table.py` →
  output; `load_roads.py` (directed for one-way road 1, weights) → output; `check_symmetric.py` → output;
  `distances_given.py` (a provided breadth-first distance function used as a black box, its code in g12) →
  eccentricities, radius, diameter, centre of the largest component → output; `components.py` (given, black box) →
  output.
- **Figures**: S the friendship graph of people 1–40 drawn from the data (layout coordinates from a tested
  `figures/` script; three groups and bridges visible); S a small weighted road map with by-hand shortest route;
  S directed vs undirected edges and degrees; S eccentricity labels on a 7-vertex graph (centre highlighted).
- **Exercises**: ★ C degrees and edges (handshake: sum of degrees = 2|E|, counted); ★ P neighbours dict; ★ C distance
  on a drawn graph; ★ C components; ★ W `degree(g, v)`; ★★ F asymmetric adjacency (edge added one way); ★★ W
  `is_path(g, seq)`; ★★ C eccentricities, radius, diameter of a drawn graph; ★★ P directed in/out degrees; ★★ W
  `edges_from_dict(g)`; ★★ C decode an NMEA position sentence (latitude in degrees and minutes → decimal degrees);
  ★★★ C prove sum of degrees = 2|E| (counting each edge twice); ★★★ C prove radius ≤ diameter ≤ 2·radius;
  ★★★ W `common_friends` / triangle count; ★★★ C rank pages of a tiny web by in-degree vs by a by-hand vote
  (search-engine idea told).
- **Problem** "The six handshakes of Brenmoor": I the graph and its degrees; II components; III eccentricities with the
  given distance function; IV radius, diameter, centre; the effect of removing one bridge. **Named result**: the
  diameter of the largest friendship component (from a run) and how much it grows when the most central bridge goes.
- **Ledger**: Milgram's 1967 small-world letter experiment (Psychology Today 1967 / a primary archive page — year and
  mean chain length printed?); NMEA 0183 sentence format (`$GPGGA` fields) — the standard is not free: gpsd's
  documentation as the accessible primary description (to verify field order; else the exercise uses an invented
  sentence format with a note); GPS/Galileo named only in the Earth recall (no new fact).

#### g10-10 Sensors, Actuators and Control Programs — `sensors-actuators-control` (~12 pp)
- **Hook**: a lift that never moves with its door open — how is that guaranteed?
- **Sections**: 1 A computer inside an object (embedded system; sensors in, actuators out; the control loop that
  never ends; reading, deciding, acting at a period); 2 Measured values turned into numbers (a sensor gives a number on
  n bits; scale and offset to a physical value; noise and averaging; thresholds and hysteresis); 3 A controller as a
  state machine (states, events, transitions, a transition table as a dict; drawing it); 4 Three simulations
  (a thermostat with hysteresis, a traffic light with a pedestrian button, a lift with doors and calls) — all
  simulated with seeded sensor readings; 5 A text interface to the device (a menu that commands the simulated lift:
  the HMI to a given specification).
- **Recalls**: sampling and quantising as data (g10-06); `while` loop (Book 1 g6); conditions.
- **Listings**: `sensor.py` (NORUN module: seeded noisy temperature sensor, 10-bit readings); `convert.py` → output
  (raw → °C); `smooth.py` (moving average) → output; `thermostat.py` (on/off vs hysteresis, switch count) → output;
  `traffic_light.py` (table-driven state machine, an event trace) → output; `lift.py` (state machine + safety check
  that every state with door open has motor off) → output; `lift_menu.py` with `lift_menu.stdin` → output (typed
  session).
- **Figures**: S sensor → controller → actuator loop with the object; S traffic-light state diagram (automata
  library); S lift state diagram; C thermostat temperature and heater state over time, plain vs hysteresis, from
  `figures/thermostat_plot.py`; P a microcontroller board or a temperature sensor (generic, no logo, free licence);
  AI a pedestrian crossing with a traffic light and button (no text).
- **Exercises**: ★ C raw 10-bit reading → °C; ★ P transition table lookup; ★ P moving average of 5 values; ★ C states
  × events table size; ★ W `to_celsius(raw)`; ★★ F missing transition (KeyError on an event); ★★ W hysteresis
  thermostat to spec; ★★ C switch count with/without hysteresis on a given trace; ★★ P traffic light trace for an
  event list; ★★ F lift moves with door open (bad transition); ★★ W `check_safe(table)` over all transitions;
  ★★★ C prove the hysteresis controller switches at most once per crossing of the band; ★★★ W a parking-barrier
  controller with counter; ★★★ C number of reachable states of the lift (exhaustive search by hand on a small
  version); ★★★ F a control loop that blocks on input (fix: poll).
- **Problem** "The lift of the town hall": I states and events of a 3-floor lift; II the transition table; III
  exhaustive check of the safety property over all reachable (state, event) pairs; IV calls served, average waiting
  steps for a given sequence. **Named result**: the number of reachable states and the proof by exhaustion that the
  door is never open while moving.
- **Ledger**: none expected (simulated devices); a sensor's 10-bit range is a chosen invention (no row).

#### g10-11 Project: A Small Web Application — `project-web-application` (~13 pp)
- **Specification (one paragraph)**: a library catalogue served on 127.0.0.1:42110 from the town's `books`, `loans`,
  `members`: a home page, a page per book with its loans, a search form (GET), a "reserve" form (POST) that records a
  reservation in memory, an error page; every route tested; nothing leaves the machine.
- **Milestones** (`\section` each, listings + outputs + tests): M1 routes and a dispatcher (a dict from path patterns to
  functions; 404); M2 pages generated from data (HTML built with escaping — `html.escape` and why: a staged injection
  of `<script>` in a search term shown escaped, the defence taught); M3 forms (search GET, reserve POST, redirect after
  POST); M4 tests (start the server as a subprocess on a port, request every route with `urllib`, check status and a
  line; unittest output captured); M5 improvements (a cookie remembering the last search; a JSON route `/api/book/7`).
- **Recalls**: g10-08 (HTTP, forms, cookies), g10-07 (joins), g10-01 (tests), g10-02 (sets), Book 1 g9 HTML/CSS.
- **Listings**: `app.py` (grows by milestone: separate stems `app_m1.py` … `app_m5.py`, each NORUN module) +
  `run_m1.py` … (start, request, stop) → outputs; `test_app.py` (unittest) → output; `style.css` (NORUN, printed).
- **Figures**: S architecture (browser ↔ server ↔ tables); S route map; S the generated book page drawn generically as
  a window (from the HTML of the output); S request sequence for search → reserve → redirect.
- **Exercises** (15, 5/6/4): ★ P route chosen for a path; ★ P escaped output; ★ W add `/about`; ★ C requests made by
  the test suite; ★ F missing `return` in a handler; ★★ W `/author/<name>`; ★★ F POST handled as GET; ★★ W sorting
  the catalogue by a query parameter; ★★ C count pages generated for n books; ★★ F test leaves the server running
  (fix: `finally`); ★★ W a 405 for wrong methods; ★★★ W pagination with tests at boundaries; ★★★ C why redirect after
  POST (count duplicate submissions on reload); ★★★ W reservation limit per member; ★★★ F a race of two reservations
  (told: one thread here; why a real server needs a database lock — pointer to g12-09).
- **Ledger**: HTTP 303 See Other / 405 (RFC 9110); `html.escape` behaviour (PYTHON-DOCS).

### Grade 11

#### g11-01 From Gates to an Arithmetic Unit — `gates-to-arithmetic-unit` (~13 pp)
- **Hook**: the half adder of Book 1 adds two bits; a processor adds two 64-bit numbers in one clock beat.
- **Sections**: 1 The full adder (three inputs; truth table; built from two half adders and an OR; checked
  exhaustively by a Python gate simulator); 2 Chaining adders (ripple-carry adder on n bits; carry delay grows with n;
  subtraction as a + ~b + 1 through two's complement with the same adder; overflow flag); 3 Choosing and decoding
  (multiplexer, decoder, each as gates and as a truth table); 4 An arithmetic and logic unit (operation code selects
  through a multiplexer among AND, OR, ADD, SUB; flags Z, N, C as the toy machine's); 5 A circuit that remembers (the
  SR latch from two NOR gates with feedback; the D flip-flop on a clock edge, told as behaviour; a register of n
  flip-flops; simulated step by step).
- **Recalls**: Boolean operations, gates, half adder, De Morgan (Book 1 g9 `logic-gates`); two's complement (g10-03);
  the transistor as a switch (Book 1 g9, physics named).
- **Listings**: `gates.py` (NORUN module: `AND`, `OR`, `XOR`, `NOT` on 0/1); `full_adder.py` → truth table output;
  `ripple.py` (n-bit adder from full adders; 8-bit examples incl. overflow) → output; `subtract.py` → output;
  `mux.py` (2:1 and 4:1, decoder 2→4) → output; `alu.py` (4-function ALU on 8 bits, flags) → output; `latch.py`
  (SR latch iterated to a fixed point; the forbidden input) → output; `dff_register.py` → output; `gate_count.py`
  (gates and depth of the ripple adder for n = 1…64) → output.
- **Figures**: S full adder from two half adders (circuitikz ports); S 4-bit ripple-carry adder with the carry chain;
  S 4:1 multiplexer; S ALU block diagram (inputs A, B, op, outputs result + flags); S SR latch from NOR gates; C carry
  path length vs n (optional, from `figures/`); P an early integrated circuit or a relay (Commons, historic).
- **Exercises**: ★ P full adder row; ★ C add two 4-bit numbers through the chain, carries listed; ★ P mux output;
  ★ C decoder outputs; ★ W `half_adder(a, b)`; ★★ F full adder with AND for XOR; ★★ W `mux4(sel, inputs)`; ★★ C gate
  count of an n-bit ripple adder; ★★ C delay in gate levels of the carry; ★★ F subtraction forgetting the +1;
  ★★ W `alu(op, a, b)` returning flags; ★★★ C prove the full adder equations from its truth table (algebra of g9);
  ★★★ C prove a−b = a + ~b + 1 mod 2ⁿ; ★★★ W `comparator(a, b)` from the subtractor's flags; ★★★ C why SR=11 is
  forbidden: trace both latch updates.
- **Problem** "Building a 64-bit adder": I the full adder count; II gates and levels for 8, 16, 32, 64 bits; III the
  carry-select idea (two halves computed both ways, told) and its count; IV comparing delays. **Named result**: a
  64-bit ripple adder needs 320 gates (5 per full adder) and a 128-level carry path; carry-select halves the delay for
  about 1.5× the gates (computed by `gate_count.py`; exact numbers from the run).
- **Ledger**: none required (circuits are definitions); a photo's facts (year of an IC) if captioned: museum page.

#### g11-02 The von Neumann Machine and Assembly Language — `von-neumann-machine` (~14 pp)
- **Hook**: a program is stored in the same memory as its numbers; the machine cannot tell them apart.
- **Sections**: 1 Processor, memory, buses, input and output (the model; address, data and control buses; program
  and data in one memory; single and multi-processor told; the 1945 report in a `history` box); 2 The toy machine
  in full (registers, PC, SP, flags, the 28 instructions, encoding 4 × opcode + r; the fetch–decode–execute step
  recalled and refined); 3 Assembly programs with jumps (labels, `CMP` and conditional jumps; a condition, a loop, a
  sum over an array in `DATA`; tracing with `--trace`); 4 Subroutines and the stack (`CALL`, `RET`, `PUSH`, `POP`,
  the stack pointer; the machine's stack described as last in, first out, with a forward pointer to g12); 5 From a line
  of Python to machine instructions (hand translation of `if`/`while`; Python's own bytecode shown with `dis`, told as
  "another machine's instructions") and the system on a chip (the components a phone's chip gathers; why
  integration saves time and energy; `history` box: software and hardware roles over time).
- **Recalls**: fetch–execute cycle, machine language, registers, program counter, the toy machine traced by hand,
  cores (Book 1 g7 `how-a-processor-runs-a-program`); adder, multiplexer, flip-flop (g11-01).
- **Listings** (all `.toy` run by `python -m toymachine`): `max2.toy` → output; `count_down.toy --trace` → trace
  output; `sum_array.toy` (array in `DATA`) → output; `abs_value.toy` (`JN`) → output; `multiply.toy` (repeated
  addition) → output; `call_square.toy` (subroutine) with `--trace` → output; `asm_listing` via `asm sum_array.toy` →
  machine-code output; `self_modify.toy` (program and data in one memory: a program that changes its own
  instruction — staged, shows the danger) → output; `py_dis.py` (`dis.dis` of a 3-line function) → output.
- **Figures**: S von Neumann model (CPU with ALU, registers, control; memory; I/O; three buses); S the toy machine's
  instruction encoding (bytefield: opcode 6 bits | r 2 bits | operand 8 bits); S memory map of `sum_array.toy`
  (code cells, data cells, stack cells from 255 down); S flow of a loop in assembly (labels and jumps as arrows);
  S a system-on-chip block diagram (cores, cache, GPU, radio, memory controller, power management) generic;
  P a historic stored-program machine (a replica or museum photo of a 1948–49 machine, licence read).
- **Exercises**: ★ P output of a 5-line program; ★ C encode `ADD R1, R2` in two bytes; ★ C decode bytes; ★ P flags
  after `SUB`; ★ W assembly for `max` of three inputs; ★★ F loop that never ends (wrong jump); ★★ W sum of an array of
  length n given in `DATA`; ★★ C steps executed by `sum.toy` for input n (3 + 3n + 2 counted); ★★ P trace of
  `call_square`; ★★ F `PUSH`/`POP` mismatch corrupts the return; ★★ W `multiply` by shift-and-add; ★★★ C prove the
  step count of the shift-and-add multiply is at most a bound; ★★★ W assembly for integer division by repeated
  subtraction with remainder; ★★★ C how many instructions fit before the stack meets the program (memory budget);
  ★★★ W translate a given Python `while` into toy assembly, tested on inputs.
- **Problem** "Multiplication on a machine that cannot": I repeated addition and its step count; II shift-and-add
  (SHL/SHR/JC); III step counts for all inputs 0…255 (code); IV the worst case of each. **Named result**: the
  worst-case step counts of both methods over all 8-bit inputs (from the run) — shift-and-add bounded by a constant
  × 8 versus up to 255 loop turns.
- **Ledger**: von Neumann's "First Draft of a Report on the EDVAC" 1945 (a primary archive/scan page); the first
  stored-program run 21 June 1948 (museum page: Science and Industry Museum Manchester / Univ. of Manchester);
  SoC components — generic, no row unless a figure is quoted; Python `dis` module docs (PYTHON-DOCS).

#### g11-03 Operating Systems and the Command Line — `os-and-command-line` (~14 pp)
- **Hook**: two programs want the same printer and the same file at once; something must decide.
- **Sections**: 1 What the kernel does (processes, memory, files, devices, users and rights; system calls named and
  told; free and proprietary systems, with the meaning of a free licence; `dated` box on families of systems);
  2 The file-system tree (root, absolute and relative paths, working directory, `.` and `..`, hidden files);
  3 The shell (commands, arguments, options; moving, listing, creating, copying, moving, removing; reading the manual;
  `safety`: `rm` has no bin); 4 Users, rights and permissions (owner, group, others; read/write/execute; `ls -l`,
  `chmod` in letters and in octal; why a program should not run as the administrator); 5 Redirection and pipes
  (`>`, `>>`, `<`, `|`; `wc`, `sort`, `uniq`, `grep`, `head`, `cut` on the town's CSV; a small pipeline answering a
  question).
- **Recalls**: program, operating system (Book 1 g4); file, folder, path (Book 1 g3 `files-and-folders`); text file
  (Book 1 g8).
- **Listings** (bash, `# capture: session`, `fixtimes` where `ls -l` shows dates): `tree_moves.sh` (mkdir, cd, pwd,
  ls) → session; `paths.sh` (absolute vs relative) → session; `copy_move.sh` → session; `perms.sh` (ls -l, chmod
  640/u+x, a staged "Permission denied" on a file without r) → session; `redirect.sh` → session; `pipes.sh` (count
  loans per member with cut | sort | uniq -c | sort -n | tail) → session; `manual.sh` (`ls --help | head`) → session.
  Data files copied from `data/town/` into the session directory by the script itself.
- **Figures**: S layers: hardware, kernel, system programs, applications, user; S the file-system tree of the session
  with the working directory marked and a relative path drawn; S permission bits (bytefield: type | rwx | rwx | rwx)
  with 640 decoded; S a pipeline as boxes joined by pipes (stdin/stdout arrows); AI none; P none (no screenshots).
- **Exercises**: ★ P output of `pwd` after `cd ../x`; ★ C absolute path from a relative one; ★ C octal of rw-r-----;
  ★ P `ls` after `mv`; ★ W a command line that counts lines of a CSV without its header; ★★ F `cat f > f` empties f;
  ★★ C which users can read a file with given mode; ★★ W pipeline: top 3 authors by number of books; ★★ F `cd` with a
  space in a name; ★★ P `>>` twice; ★★ W `chmod` to let the group read but not write; ★★★ C number of distinct modes
  and how many let others write; ★★★ C prove every relative path can be rewritten without `..` given the working
  directory (argument); ★★★ W a short shell script with a parameter; ★★★ F a pipeline that sorts numbers
  alphabetically (`sort -n`).
- **Problem** "Who may read the timetable?": I users and groups of a school's server (invented); II modes of six
  files; III who can read, write, enter each directory (execute bit on directories); IV the least privileges that meet
  a policy. **Named result**: the minimal set of `chmod` modes meeting the policy and the count of permission bits
  changed.
- **Ledger**: POSIX `chmod` octal modes and `ls -l` mode string (The Open Group Base Specifications); GNU coreutils
  manual for options shown (`sort -n`, `uniq -c`); the definition of free software (FSF's four freedoms page) and
  of open source (OSI definition page); families of operating systems in a `dated{2026}` box (no market shares).

#### g11-04 Network Layers and Protocols — `network-protocols` (~14 pp)
- **Hook**: a message cut into packets crosses five networks, some of which lose packets; it still arrives whole.
- **Sections**: 1 A protocol is an agreed format and an agreed dialogue (recall of HTTP as one; layers: application,
  transport, network, link; encapsulation: each layer adds a header; a packet dissected as nested headers);
  2 Addresses and the network mask (IPv4 address on 32 bits, dotted notation; network part and host part; mask and
  `/n` prefix; same network or not; `ipaddress` module; IPv6 told); 3 A routing table read by hand (destination,
  mask, next hop; longest prefix match; the default route); 4 Reliable delivery over an unreliable network
  (acknowledgements, timeouts, retransmission, duplicates; the alternating-bit protocol simulated with a seeded lossy
  channel; stop-and-wait throughput); 5 Ports and the transport layer (port numbers name programs on a machine;
  TCP's reliable stream vs UDP's datagrams; reliability without a timing guarantee; peer-to-peer vs client–server
  as a remark; names resolved from a local table, Book 1's name system recalled).
- **Recalls**: packet, address, router, name system, client and server (Book 1 g8); HTTP (g10-08); binary and masks
  (g10-03).
- **Listings**: `encapsulate.py` (application data wrapped in toy headers, printed as bytes with field names) →
  output; `same_network.py` (`ipaddress`, masks) → output; `mask_bits.py` (AND of address and mask by hand vs
  module) → output; `route_lookup.py` (longest-prefix match on a printed table) → output; `lossy_channel.py` (NORUN
  module, seeded); `alternating_bit.py` (event trace: send, lose, timeout, resend, ack) → output; `throughput.py`
  (stop-and-wait utilisation for given rates) → output; `hosts_lookup.py` (local name table) → output.
- **Figures**: S the four layers with encapsulation (nested header boxes); S IPv4 header field layout (bytefield,
  32-bit rows; widths from RFC 791) — simplified: version, IHL, total length, TTL, protocol, addresses; S a small
  internetwork of 3 routers with one routing table beside it; S alternating-bit sequence diagram with a lost packet
  and a lost ack; P a network switch or an Ethernet cable (Commons, generic); AI none.
- **Exercises**: ★ C network address of 192.168.10.37/24; ★ C hosts in a /26; ★ P route chosen for an address; ★ P
  headers in order; ★ W `same_network(a, b, prefix)`; ★★ F mask applied with OR; ★★ W longest-prefix `lookup`;
  ★★ C bytes of headers for a 100-byte message (20 + 20 + 14 framing, sourced); ★★ P alternating-bit trace with a given
  loss pattern; ★★ F receiver accepts a duplicate (bit not checked); ★★ C stop-and-wait utilisation; ★★★ C prove the
  alternating bit suffices when the channel does not reorder (case analysis); ★★★ W a sliding window of 2 (told then
  simulated); ★★★ C counterexample: alternating bit fails if the channel reorders; ★★★ W subnetting a /24 into four.
- **Problem** "Stop and wait across the sea": I a link's rate, packet size, round-trip time; II time to send one
  packet and wait; III utilisation; IV with a window of w packets, the w that fills the line. **Named result**: the
  utilisation of stop-and-wait on the given long link (a fraction of a percent, computed) and the window size that
  reaches full rate.
- **Ledger**: IPv4 RFC 791 (header fields and widths, 1981); CIDR RFC 4632; private ranges RFC 1918 (for examples:
  use 192.168.x.x / 10.x documented addresses, or RFC 5737 documentation ranges 192.0.2.0/24 — preferred for examples);
  TCP RFC 9293; UDP RFC 768; IPv6 RFC 8200 (128 bits); Ethernet header 14 bytes (IEEE 802.3, via a primary
  description); IANA ports registry (well-known 0–1023 range, 80/443/53); ARPANET 1969 first link (a primary history
  page); typical link rates in a `dated{2026}` box.

#### g11-05 Proving Algorithms Correct — `proving-algorithms-correct` (~13 pp)
- **Hook**: a binary search that passed every test and still loops forever on one input.
- **Sections**: 1 Does it stop? (a variant: a whole number that strictly decreases at each turn and stays ≥ 0;
  termination of `while` loops; Euclid's algorithm recalled from the mathematics book as an example); 2 Is the answer
  right? (loop invariant: true at the start, kept by each turn, useful at the end; a method box; asserting an
  invariant in code to test it); 3 The largest element and selection sort (invariants proved); 4 Insertion sort
  (outer and inner invariants); 5 Binary search (the invariant `lo ≤ answer < hi`, termination by the variant
  hi − lo, the classic off-by-one bugs).
- **Recalls**: `while` loop (Book 1 g6); linear and binary search, selection and insertion sort (Book 1 g8
  `searching-and-sorting`); specification, assertion (g10-01).
- **Listings**: `largest.py` (with invariant asserts) → output; `selection_sort.py` (invariant asserts; prints the
  list after each turn) → output; `insertion_sort.py` → output; `binary_search.py` → output; `binary_search_bug.py`
  (`lo = mid` loops; bounded with `timeout=` / an iteration cap that raises) → staged output; `variant_check.py`
  (prints the variant at each turn of Euclid) → output.
- **Figures**: S invariant picture of selection sort (sorted prefix | rest, minimum moved); S insertion sort's inner
  shift; S binary search window shrinking with lo/mid/hi pointers (3 steps); S the variant as a decreasing staircase
  (values from the run).
- **Exercises**: ★ P selection sort after 2 turns; ★ C variant of a countdown; ★ P binary search steps; ★ C invariant
  holds initially?; ★ F `range(1, n)` misses an element in `largest`; ★★ C prove termination of a given loop;
  ★★ W `index_of_min(t, i)` with postcondition assert; ★★ F binary search with `hi = mid - 1` bug; ★★ C invariant for a
  running sum; ★★ C invariant for counting occurrences; ★★ W `is_sorted` with a proved invariant; ★★★ C prove
  insertion sort correct (both invariants); ★★★ C prove binary search finds x if present; ★★★ C a loop with no
  obvious variant (Collatz) — explain why no proof is known (told); ★★★ W `first_true(f, lo, hi)` (lower bound
  search) with invariant.
- **Problem** "The integer square root": I spec of isqrt(n) = largest r with r² ≤ n; II linear search and its
  variant; III search by halving with the invariant lo² ≤ n < hi²; IV correctness and termination proved; step counts
  compared for n up to 10⁶. **Named result**: isqrt by halving is correct, stops, and takes about 20 turns for
  n ≤ 10⁶ (exact maximum from the run; 2²⁰ ≈ 10⁶ counted as halvings, no logarithm).
- **Ledger**: none (proofs); a `history` box on Floyd 1967 / Hoare 1969 assigned meaning — ledger rows from the
  papers' primary pages if printed.

#### g11-06 The Cost of an Algorithm — `cost-of-an-algorithm` (~13 pp)
- **Hook**: two programs give the same answer; on a million names one takes a second, the other a week.
- **Sections**: 1 Counting elementary operations (comparisons, assignments; the input size n; counting with an
  instrumented function); 2 Best and worst case (linear search, insertion sort on sorted vs reversed input);
  3 Constant, linear and quadratic cost (definitions by how the count grows when n doubles; table of n, n², counts);
  4 The cost of halving (the number of times n can be halved until 1: h(n), counted, with 2^h ≤ n < 2^(h+1); binary
  search's worst case h(n) + 1); 5 Measured running times set against the counts (`time.perf_counter`, repetitions,
  median of runs; doubling experiments; measurement noise; `listings/MEASURED.txt`, captions say *laptop*).
- **Recalls**: g11-05 algorithms; Book 1 g8 comparison counting.
- **Listings**: `count_linear.py` → output; `count_insertion.py` (best/worst/random seeded) → output; `doubling.py`
  (counts for n = 1000, 2000, 4000) → output; `halvings.py` (h(n) table) → output; `measure_sorts.py` (MEASURED)
  → output; `measure_search.py` (linear vs binary vs `in` on a set, MEASURED) → output.
- **Figures**: C comparisons vs n for linear and quadratic (from `figures/counts.py`); C measured times of insertion
  sort vs n, log–log avoided at this level (linear axes, doubling marked) from `figures/measured_plot.py` (MEASURED
  data recaptured on a quiet machine); S halving staircase (n, n/2, …, 1 as bars); S best vs worst input arrays for
  insertion sort.
- **Exercises**: ★ C comparisons of linear search, worst case; ★ C h(1000); ★ P instrumented count output; ★ C count
  of a double loop `for i: for j<i`; ★ W `count_comparisons(sort, t)`; ★★ C exact count for selection sort
  n(n−1)/2 (sum argued by pairing, no induction); ★★ F timing that measures printing too; ★★ C what happens to a
  quadratic count when n triples; ★★ W duplicate detection in quadratic time; ★★ P which input is the worst for a given
  code; ★★ W `h(n)` by halving; ★★★ C prove binary search makes at most h(n)+1 comparisons; ★★★ C rank five given
  cost functions by growth (counts at n = 10, 1000, 10⁶); ★★★ W duplicates by sorting then scanning, counted; ★★★ C
  from measured times predict the time at 10× the size and check.
- **Problem** "Two ways to find duplicates": I quadratic pair check, count; II sort-then-scan, count (sort cost as
  measured); III a set, measured; IV the crossover size for the given counts and the measured ratio at n = 10⁵.
  **Named result**: the size from which sort-then-scan wins and the measured speed-up at n = 10⁵ on the author's
  laptop (MEASURED, ratio asserted by shape in the test).
- **Ledger**: none (counts are computed); a `dated{2026}` box with a typical processor clock rate if printed (vendor
  page).

#### g11-07 Greedy Algorithms — `greedy-algorithms` (~12 pp)
- **Hook**: giving change with the fewest coins: take the largest coin that fits — and it works, here.
- **Sections**: 1 Optimisation problems (feasible solution, objective, optimum; exhaustive search on tiny inputs as a
  reference); 2 The greedy choice (a method box; giving change with a canonical coin system; optimal for 1, 2, 5,
  proved by exchange; for 1, 2, 5, 10, 20, 50 an exhaustive check up to the sum of the two largest coins, which a
  theorem stated with `\admitted` (Kozen and Zaks) shows is enough); 3 Choosing activities (earliest end time
  first; proof by exchange: the greedy solution stays ahead); 4 Filling a knapsack (fractional: greedy by value per
  kilogram is optimal; 0/1: greedy fails, counter-example; pointer to g12-07); 5 When greedy fails (non-canonical
  coins 1, 3, 4; the smallest counter-example found by program).
- **Recalls**: sorting with a key (g10-07); cost (g11-06); invariants (g11-05).
- **Listings**: `change_greedy.py` → output; `change_exhaustive.py` (reference by trying all combinations, small) →
  output; `activities.py` (town: room bookings generated in the listing, seeded) → output; `knapsack_fractional.py`
  → output; `knapsack_01_greedy_fails.py` → output; `smallest_counterexample.py` (coin systems up to a bound) →
  output.
- **Figures**: S activity intervals on a timeline with the greedy picks; S fractional knapsack as bars by density;
  S the coins 1, 3, 4 counter-example: greedy 4+1+1 vs optimum 3+3; S exchange argument picture (first difference
  swapped).
- **Exercises**: ★ P change for 87; ★ C greedy vs optimum for 6 with {1,3,4}; ★ P activities chosen; ★ C fractional
  knapsack value; ★ W `greedy_change(amount, coins)`; ★★ F sorting activities by start time; ★★ W `max_activities`;
  ★★ C count combinations explored by exhaustive change for 20; ★★ F knapsack greedy by value instead of density;
  ★★ P greedy 0/1 knapsack result; ★★ W `is_canonical_upto(coins, m)`; ★★★ C prove earliest-end-first is optimal;
  ★★★ C prove greedy change optimal for {1, 2, 5} (case argument); ★★★ W interval colouring (rooms needed) greedy;
  ★★★ C counter-example for "shortest activity first".
- **Problem** "The coins of Brenmoor": I the town's invented coin system; II greedy and exhaustive change for
  1…100; III the amounts where greedy is not optimal; IV changing one coin to make the system canonical. **Named
  result**: the smallest amount greedy gets wrong in the given system and the number of such amounts up to 100.
- **Ledger**: euro coin denominations (ECB page) if named; otherwise use "a system of coins 1, 2, 5, …" invented
  (preferred: no row).

#### g11-08 Classifying by Neighbours: the k-NN Algorithm — `k-nearest-neighbours` (~13 pp)
- **Hook**: the town's sorting office must decide letter, packet or parcel from thickness and mass.
- **Sections**: 1 Learning from labelled examples (example, feature, label/class; a training set; the task: predict
  the class of a new item); 2 A distance between examples (Euclidean distance recalled from the mathematics book;
  scaling features so one unit does not dominate; floating point recalled); 3 The k nearest neighbours vote
  (algorithm as a method; ties; k = 1 vs larger k; decision regions); 4 Measuring the error (examples kept aside: a
  test set; error rate; choosing k by the error on a validation part; why not on the training set); 5 What the method
  cannot do, and its cost (every prediction scans all n examples: cost n·d per query + sorting/selection; no model
  learned; curse of dimension told; the AI series named in prose for further reading).
- **Recalls**: pseudo-random numbers, simulation (Book 1 g9); floating point (g10-04); sorting with a key (g10-07);
  cost (g11-06).
- **Listings**: `parcels.py` (NORUN module: seeded generator of 300 items, 3 classes, overlapping); `show_data.py` →
  output (counts per class, first rows); `distance.py` → output; `knn.py` (predict one item, k = 1, 3, 7; neighbours
  listed) → output; `scale.py` (effect of grams vs millimetres) → output; `error_rate.py` (train/test split seeded;
  errors for k = 1…15) → output; `choose_k.py` → output; `knn_cost.py` (distance computations counted) → output.
- **Figures**: C scatter of the training set by class (three markers) from `figures/parcels_plot.py`; C decision regions
  for k = 1 and k = 7 on a grid (from `figures/regions.py`); C error rate vs k (from `figures/error_vs_k.py`); S a new
  point with its 5 nearest neighbours circled; AI a parcel sorting desk (no labels, no text).
- **Exercises**: ★ C a distance; ★ P class predicted with k = 3 on a tiny set; ★ P neighbours in order; ★ C error rate
  from a confusion table; ★ W `distance(a, b)`; ★★ F forgetting to exclude the item itself (leave-one-out bug);
  ★★ W `knn_predict(train, x, k)`; ★★ C effect of scaling on which neighbour is nearest; ★★ F ties broken
  inconsistently; ★★ P error on training set for k = 1 (always 0, why); ★★ W min–max scaling; ★★★ C cost of predicting
  m items with n examples in d features; ★★★ W leave-one-out error for each k; ★★★ C why a large k tends to the
  majority class (k = n); ★★★ W a weighted vote (1/distance), compared.
- **Problem** "The sorting office": I the data and a baseline (always "packet"); II k-NN for k = 1…15 on a held-out
  test set; III scaling and its effect; IV the chosen k and the final error on untouched data. **Named result**: the
  best k and its test error rate against the baseline's (from the seeded run).
- **Ledger**: Fix & Hodges 1951 / Cover & Hart 1967 for a `history` box (primary page of the paper); no data rows.

#### g11-09 Modules, Interfaces and Libraries — `modules-and-interfaces` (~12 pp)
- **Hook**: a calendar module used by twenty programs is rewritten to be ten times faster; none of them notices.
- **Sections**: 1 Splitting a program into modules (a file is a module; `import`, `from … import`; the module search
  path told; `if __name__ == "__main__"`); 2 The interface and the hidden implementation (what users may rely on:
  names, specifications; a leading underscore by convention; documenting with docstrings and `help()`);
  3 The standard library and how to read its documentation (reading the entries for `random.choice`, `statistics`,
  `datetime`, `collections.Counter`; the parts of a documentation entry; versions); 4 Changing an implementation
  without touching its users (a `dateset` module of dates implemented with a list then with a set; the same tests
  pass; measured speed-up); 5 Libraries outside the standard library told (`inpractice` box: package installers named,
  versions, licences; nothing installed in this book) and how languages share constructions (sequence, assignment,
  conditionals, loops, calls — the same constructions in toy assembly and Python, a short comparison).
- **Recalls**: function (Book 1 g7); specification and tests (g10-01); sets (g10-02); cost (g11-06).
- **Listings**: `geometry.py` (NORUN module) + `use_geometry.py` → output; `main_guard.py` → output; `help_view.py`
  (`help()` of our module captured) → output; `stdlib_tour.py` → output; `dateset_list.py`, `dateset_set.py` (NORUN,
  same interface); `use_dateset.py` (run against both) → output; `measure_dateset.py` (MEASURED) → output;
  `test_dateset.py` (unittest run on both implementations) → output.
- **Figures**: S module dependency graph of a small program; S interface as a wall: public names above, private
  below; S a documentation entry annotated (signature, parameters, return, raises, example) drawn generically;
  C measured time of `contains` for both implementations vs n (from `figures/`, MEASURED, *laptop*).
- **Exercises**: ★ P what `import` makes visible; ★ P `__name__` value; ★ C which names are public; ★ P output using a
  stdlib function after reading its doc; ★ W a module `temperature` with two functions and docstrings; ★★ F circular
  import (staged); ★★ F user relies on a private name; ★★ W rewrite a module's implementation keeping its tests;
  ★★ C cost of the two `dateset` operations; ★★ P `from x import *` shadows a name; ★★ W `Counter`-based word count
  after reading the doc; ★★★ C design an interface for a queue (operations and specs, prose); ★★★ W a module with two
  implementations chosen at import time, one test file; ★★★ C how many lines of user code change when the interface
  changes vs when the implementation changes (argued on the example); ★★★ F a module with side effects at import.
- **Problem** "The calendar module": I a module of dates (leap years from g10-01); II its interface and tests;
  III three implementations (list, sorted list with halving, set); IV measured cost of membership for n = 10³…10⁵.
  **Named result**: the measured speed-up of the set implementation at n = 10⁵ on the author's laptop with the tests
  unchanged (MEASURED; asserted as a shape).
- **Ledger**: Python docs pages for each documented function cited (PYTHON-DOCS rows: page + access date); PEP 8
  naming (python.org PEP page).

#### g11-10 Project: An Assembler and Simulator for the Toy Machine — `project-toy-machine` (~14 pp)
- **Specification (one paragraph)**: write, in Python, a two-pass assembler for the toy machine's assembly language
  (labels, comments, the four number notations, `DATA`) and a simulator of its fetch–execute cycle with the 28
  instructions, flags, the stack, `IN`/`OUT`, a step limit and a trace; check both against the series' shared
  `toymachine` package on every program of g11-02.
- **Milestones**: M1 reading lines (tokens, comments, labels; errors with line numbers); M2 first pass (addresses of
  labels; each instruction 2 bytes; `DATA` sizes) and second pass (encoding 4 × opcode + r, operands); compare bytes
  with `toymachine.assemble`; M3 the simulator core (fetch, decode, execute; registers; PC; HALT; step limit);
  M4 arithmetic flags and jumps, then stack and subroutines; M5 tests (every g11-02 program assembled and run by both,
  outputs equal; error cases) and a trace printer matching the shared tool's format.
- **Recalls**: g11-02 (toy machine), g10-03 (two's complement, flags), g10-05 (strings), g11-09 (modules).
- **Listings**: `tokens.py`, `assembler_m2.py`, `simulator_m3.py`, `simulator_m4.py` (NORUN modules, the reader's);
  `run_m1.py` … `run_m5.py` → outputs; `compare_shared.py` (our bytes vs `toymachine.assemble`, our outputs vs
  `toymachine.Machine`) → output; `test_ours.py` (unittest) → output. The chapter's code imports the shared package
  read-only (`sys.path` set in the listing to `code/shared/toymachine`).
- **Figures**: S two-pass assembly flow (source → symbol table → bytes); S the symbol table and the byte layout of a
  sample program; S decode step: byte0 split into opcode and r (bytefield); S simulator loop state diagram.
- **Exercises** (15, 5/6/4): ★ P symbol table of a program; ★ C bytes of `DATA 1, 2, 3`; ★ P error message for an
  unknown label; ★ C opcode and register of byte 0x51; ★ W `parse_number(s)` for the four notations; ★★ F forward
  label resolved in one pass; ★★ W `NOT` and `SHR` with flags; ★★ F `C` flag of `SUB` inverted; ★★ C memory left for
  the stack after a given program; ★★ W `--dump` output; ★★ P trace rows of a given program; ★★★ W a new pseudo-
  instruction `INC r` expanded by the assembler (to `ADDI r, 1`); ★★★ C prove every 2-byte word with opcode ≤ 27
  disassembles uniquely; ★★★ W a disassembler; ★★★ C count the distinct instructions the encoding allows.
- **Ledger**: none (the machine is the series' own).

### Grade 12

#### g12-01 Recursion — `recursion` (~13 pp)
- **Hook**: a folder holds folders that hold folders; counting every file is easiest by a function that calls itself.
- **Sections**: 1 A function that calls itself (base case, recursive case; factorial, sum of a list, power;
  tracing calls); 2 The call stack (a frame per call holding its arguments and local names; drawn; recursion depth and
  `RecursionError`, staged and bounded; `sys.getrecursionlimit`); 3 Proving a recursive function (correctness by
  induction, recalled from the mathematics book's grade 12; termination by a variant on the argument); 4 Recursion and
  loops (rewriting tail-shaped recursion as a loop; when recursion is the natural form: trees of folders, nested lists);
  5 Three classics (towers of Hanoi with 2ⁿ − 1 moves proved; recursive drawings as figures from computed paths —
  a recursive tree / Koch curve written to `.dat`; the naive Fibonacci and its call count, a pointer to g12-07).
- **Recalls**: function (Book 1 g7); invariant and variant (g11-05); proof by induction (mathematics grade 12);
  folders and paths (Book 1 g3; g11-03).
- **Listings**: `factorial.py` → output; `trace_calls.py` (indented call/return trace) → output; `depth_error.py`
  (staged `RecursionError`, limit lowered) → output; `count_files.py` (walks a small folder tree built by the listing
  itself in a temporary directory) → output; `nested_sum.py` → output; `hanoi.py` (moves for n = 3; counts for
  n = 1…20) → output; `koch.py` (NORUN, writes points; figure from `figures/`); `fib_calls.py` (call counts) → output;
  `loop_version.py` → output.
- **Figures**: S the call stack of `factorial(4)` at its deepest point (frames as stacked boxes); S call tree of
  `fib(5)` (forest) with repeated subtrees shaded; S Hanoi: the three-step decomposition (move n−1, move 1, move n−1);
  C the Koch curve at depth 3 from `figures/koch_points.py`; AI a wooden towers-of-Hanoi toy on a table (no text).
- **Exercises**: ★ P `trace_calls` for n = 3; ★ C Hanoi moves for 5 disks; ★ P a recursive string reversal; ★ C
  frames on the stack at the deepest point of `sum_list` of length 6; ★ W recursive `count_digits(n)`; ★★ F missing
  base case; ★★ F base case never reached for negative input; ★★ W `flatten(nested)`; ★★ C prove `power(x, n)`
  correct by induction; ★★ P call order of a two-call recursion; ★★ W recursive `is_palindrome`; ★★★ C prove Hanoi
  needs at least 2ⁿ − 1 moves (lower bound by induction); ★★★ C count calls of naive `fib(n)` (it equals
  2·fib(n+1) − 1, proved by induction); ★★★ W all subsets of a list, recursively; ★★★ W binary representation of n
  recursively, with a proof.
- **Problem** "The sixty-four disks": I the recursive solution; II moves for n = 1…10; III proof of 2ⁿ − 1 by
  induction and of optimality; IV time for 64 disks at one move per second. **Named result**: 2⁶⁴ − 1 =
  18,446,744,073,709,551,615 moves, about 585 billion years (computed with Python's integers).
- **Ledger**: Lucas 1883 (towers puzzle, a primary page or museum scan) for the `history` box; Python's default
  recursion limit (PYTHON-DOCS `sys.getrecursionlimit`).

#### g12-02 Classes and Objects — `classes-and-objects` (~13 pp)
- **Hook**: a date is three numbers, but adding a day to it is not adding one to a number.
- **Sections**: 1 Grouping data with the functions that act on it (class, instance, attributes, methods,
  `__init__` as the constructor, `self`); 2 Encapsulation and the interface of a class (private by convention,
  methods that keep an invariant — a `Fraction` always reduced, a `Date` always valid; properties told);
  3 Special methods (`__repr__`, `__str__`, `__eq__`, `__lt__`, `__add__`, `__len__`; objects that sort, print and add);
  4 Inheritance, a first look (a subclass, overriding, `super()`; when not to use it); 5 Paradigms (the same task —
  the total of overdue loans — written in imperative style, in functional style (no assignment after creation,
  `sorted`, `map`, `filter`, comprehensions, functions passed as arguments) and in object style; choosing by the field
  of application; mixing paradigms in one program).
- **Recalls**: module, interface (g11-09); mutability (g10-02); the town's loans (g10-07).
- **Listings**: `point_class.py` → output; `fraction.py` (NORUN module: `Fraction` with invariant) + `use_fraction.py`
  → output; `date_class.py` (NORUN) + `use_date.py` → output; `special_methods.py` → output; `shapes.py`
  (inheritance) → output; `paradigms.py` (three versions, same result) → output; `bad_mutation.py` (an object whose
  attribute is changed from outside breaks its invariant — staged) → output.
- **Figures**: S class vs instances (one class box, three object boxes with their attribute values); S memory
  diagram of two names on one object vs two objects; S inheritance diagram (base and two subclasses, overridden
  methods marked); S the three paradigms as three columns of the same computation.
- **Exercises**: ★ P printing an object without `__repr__`; ★ P method calls; ★ W a `Counter` class with `add`,
  `value`; ★ C attributes after a sequence of calls; ★ F forgetting `self`; ★★ W `Fraction.__add__` keeping the
  invariant; ★★ F `__eq__` without `__hash__` used in a set (told); ★★ P `super()` call order; ★★ W `Date.next_day`;
  ★★ C prove `Fraction` stays reduced after `+` (gcd argument, gcd recalled from the mathematics book); ★★ W
  functional rewrite of an imperative loop; ★★★ W a `Stack` class (forward to g12-03) with tests; ★★★ C count
  objects created by a given program; ★★★ F shared mutable class attribute; ★★★ W `Polynomial` with `__add__`,
  `__mul__`, `__call__`.
- **Problem** "Exact fractions": I a `Fraction` class; II the invariant and its proof; III the harmonic sums
  1 + 1/2 + … + 1/n exactly; IV their denominators against the least common multiple of 1…n. **Named result**:
  H₁₀ = 7381/2520 exactly, and the floating-point sum's error (computed).
- **Ledger**: none expected (Python semantics: PYTHON-DOCS data model page cited if a rule is quoted).

#### g12-03 Linked Lists, Stacks and Queues — `lists-stacks-queues` (~13 pp)
- **Hook**: an editor's undo button and a printer's waiting list are the same idea, reversed.
- **Sections**: 1 An abstract data type is defined by its operations (interface with specifications; implementation
  hidden; recall g11-09); 2 The linked list (cells with a value and a link to the next; `None` at the end; built with
  a class; walking, inserting at the head; drawn); 3 The stack (push, pop, top, is_empty; LIFO; implemented with a
  Python list and with linked cells; cost of each operation); 4 The queue (enqueue, dequeue; FIFO; implemented with
  linked cells and a tail pointer, and with two stacks; costs, and the queue-with-two-stacks argument that each element
  moves at most twice); 5 Using them (checking brackets with a stack; evaluating a postfix expression; a waiting line
  simulated with a queue; choosing a structure; finding a value in a list vs in a dictionary, measured).
- **Recalls**: classes (g12-02); module/interface (g11-09); cost (g11-06); dictionary (Book 1 g8).
- **Listings**: `cell.py` (NORUN) + `linked_demo.py` → output; `stack_list.py`, `stack_linked.py` (NORUN, same
  interface); `test_stacks.py` (one unittest suite on both) → output; `queue_linked.py`, `queue_two_stacks.py` (NORUN)
  + `test_queues.py` → output; `brackets.py` → output; `postfix.py` → output; `waiting_line.py` (seeded arrivals) →
  output; `list_vs_dict.py` (MEASURED) → output.
- **Figures**: S a linked list of four cells with pointers and `None`; S push and pop on a stack (before/after);
  S queue with head and tail pointers, enqueue at tail; S queue from two stacks (in-stack and out-stack, a transfer);
  S postfix evaluation stack states step by step.
- **Exercises**: ★ P stack after a sequence; ★ P queue after a sequence; ★ C brackets check trace; ★ P postfix value;
  ★ W `peek` for both stacks; ★★ F pop on empty without check; ★★ W `length` of a linked list, recursive and iterative;
  ★★ F lost tail pointer after the last dequeue; ★★ C moves of the two-stack queue on a given sequence; ★★ W
  `reverse(linked)` in place; ★★ P infix → postfix of a given expression (by hand); ★★★ C prove each element is
  pushed and popped at most twice in the two-stack queue (n operations cost at most 3n moves, counted); ★★★ W a
  queue in a fixed-size array (circular, told by indices); ★★★ W infix → postfix (shunting-yard) for + − × ÷ and
  brackets; ★★★ C prove a bracket string is balanced iff the stack algorithm accepts it.
- **Problem** "The queue at the post office": I a queue ADT; II two implementations; III a simulation of a day of
  arrivals and services (seeded); IV the longest wait and the queue's maximum length, and the operation counts of both
  implementations. **Named result**: the two-stack queue does at most 3 elementary moves per element over the day
  (counted) — the same answers as the linked queue.
- **Ledger**: Łukasiewicz notation history (1924 / Polish notation) only if a `history` box prints it (primary page).

#### g12-04 Trees and Binary Search Trees — `trees` (~13 pp)
- **Hook**: a guess-the-number game played on a sorted list is a tree in disguise.
- **Sections**: 1 Vocabulary (tree, root, node, leaf, parent, child, subtree, depth of a node, height, size; a
  folder tree and an HTML page as trees — recalled); 2 Binary trees (the recursive definition: empty, or a node with a
  left and a right binary tree; a class `Node`; size and height by recursion; bounds: h + 1 ≤ n ≤ 2^(h+1) − 1 proved by
  induction, with the convention height of a single node = 0 stated once); 3 Traversals (preorder, inorder,
  postorder — recursive; breadth-first with a queue; an expression tree evaluated in postorder); 4 Binary search
  trees (the ordering property; search and insertion; cost bounded by the height; inorder traversal gives sorted
  order); 5 Balanced and degenerate trees (inserting sorted keys gives a list; random orders give short trees,
  measured; balance told as an idea, rotations left to the Year 1 volume).
- **Recalls**: recursion (g12-01); queue (g12-03); induction (mathematics grade 12); folder tree (Book 1 g3), page as a
  tree (Book 1 g9).
- **Listings**: `node.py` (NORUN) + `size_height.py` → output; `traversals.py` (four orders on one tree) → output;
  `expression_tree.py` → output; `bst.py` (NORUN) + `bst_demo.py` (town book titles inserted; search; inorder) →
  output; `degenerate.py` (sorted vs shuffled inserts, heights) → output; `random_heights.py` (heights over 1000
  seeded shuffles, n = 1023) → output (+ `.dat` for the chart).
- **Figures**: S a labelled tree (root, leaves, depth levels, a subtree circled); S one binary tree with its four
  traversal orders listed; S the BST of the first 10 book titles (from the run); S degenerate vs balanced BST of 1…7;
  C histogram of heights over random insertion orders (from `figures/heights_hist.py`).
- **Exercises**: ★ C size, height, leaves of a drawn tree; ★ P preorder; ★ P inorder; ★ P BST after inserts;
  ★ W `count_leaves(t)`; ★★ F height off by one (convention); ★★ W `bst_min(t)`; ★★ C minimum height of a binary
  tree with 100 nodes; ★★ P breadth-first order; ★★ F BST insertion that ignores duplicates wrongly; ★★ W
  `is_bst(t)` (with bounds, the classic wrong version as F-style remark); ★★★ C prove n ≤ 2^(h+1) − 1 by induction;
  ★★★ C prove inorder of a BST is sorted; ★★★ W rebuild a tree from its preorder and inorder; ★★★ C how many
  binary trees of size 3 and 4 (counted by listing, recursive count).
- **Problem** "How tall is a search tree?": I BST of n keys; II worst case height n − 1 (sorted input); III the best
  height and its bound; IV measured heights over 1,000 random orders for n = 1,023. **Named result**: the best height
  9 (= halvings of 1023) against the worst 1,022 and the measured mean height of random trees (from the run).
- **Ledger**: none.

#### g12-05 Graph Traversals and Shortest Paths — `graph-algorithms` (~14 pp)
- **Hook**: escaping a maze by always keeping a hand on the wall does not give the shortest exit.
- **Sections**: 1 Representations (adjacency lists as dict of lists, successors and predecessors for directed graphs;
  the adjacency matrix recalled from the mathematics book; converting both ways; costs of each in space and time);
  2 Depth-first search (with an explicit stack and recursively; visited set; reachability; detecting a cycle in an
  undirected graph and in a directed graph (three colours, told then coded)); 3 Breadth-first search (with a queue;
  distances in edges; the BFS tree and rebuilding a path from parents; mazes as grid graphs); 4 Dijkstra's algorithm on
  weighted graphs (method; a simple version that picks the minimum by a scan; invariant: the distances of finished
  vertices are final, proved; cost n² for this version; negative weights break it, counter-example); 5 On the town
  (road network: shortest distance from the station to every place; one-way road 1 respected) — and the graph as a
  class (`Graph` with `add_edge`, `neighbours`).
- **Recalls**: graph, path, distance, components (g10-09); stack, queue (g12-03); classes (g12-02); adjacency matrix
  (mathematics grade 12).
- **Listings**: `representations.py` → output; `dfs.py` (iterative and recursive orders) → output; `cycle.py` →
  output; `bfs.py` (distances and parents) → output; `maze.py` (a seeded maze printed as text; BFS shortest exit;
  hand-on-wall path length) → output; `dijkstra.py` (step table) → output; `dijkstra_town.py` (town roads) → output;
  `negative_weight.py` (staged wrong answer) → output; `graph_class.py` (NORUN) + `use_graph.py` → output.
- **Figures**: S one graph with its adjacency list and matrix side by side; S DFS order numbers on a graph with tree
  edges bold; S BFS layers (distance 0, 1, 2, 3) on a grid maze; S Dijkstra step table on a 6-vertex weighted graph
  with the finished set shaded; S the town map with the shortest-route tree from the station (coordinates from the
  data).
- **Exercises**: ★ P DFS order; ★ P BFS order; ★ C adjacency matrix from a drawing; ★ C distances by BFS; ★ W
  `to_matrix(adj)`; ★★ F DFS marks visited too late (exponential repeat); ★★ W `has_path(g, a, b)`; ★★ P Dijkstra
  table for a given graph; ★★ F Dijkstra picks the last-added instead of the minimum; ★★ C space of list vs matrix for
  the town; ★★ W `shortest_path(parents, t)`; ★★★ C prove BFS distances are shortest in edges; ★★★ C prove the
  Dijkstra invariant; ★★★ W cycle detection in a directed graph; ★★★ C negative-weight counter-example with three
  vertices.
- **Problem** "The shortest exit": I a maze as a grid graph; II DFS exit vs hand-on-wall; III BFS shortest exit and
  its path; IV a maze with doors of different costs (Dijkstra). **Named result**: the length of the shortest exit of
  the seeded maze against the wall-follower's (from the run).
- **Ledger**: Dijkstra 1959 ("A note on two problems in connexion with graphs", Numerische Mathematik — primary page)
  for the `history` box.

#### g12-06 Divide and Conquer — `divide-and-conquer` (~13 pp)
- **Hook**: sorting a pile of 1,000 exam papers by splitting it between two helpers, who split again.
- **Sections**: 1 Split, solve, combine (the method; binary search read again as divide and conquer); 2 Merge sort
  (merging two sorted lists, its invariant; the recursive sort; the count of comparisons ≤ n·h for n = 2^h, proved;
  the logarithm recalled from the mathematics book and log₂ introduced as a notation, n log₂ n); 3 Fast
  exponentiation (xⁿ by squaring; number of multiplications at most 2·⌊log₂ n⌋ + 1, counted; recursive and iterative;
  modular version for g12-12); 4 Rotating an image by quarters (a 2^k × 2^k image rotated by recursive quadrant swaps
  in constant extra memory, against the simple copy; on a small PGM from the town map drawing); 5 When it pays and
  when it does not (a split that leaves one big part; overhead on small inputs; maximum subarray told).
- **Recalls**: recursion, induction (g12-01); binary search (Book 1 g8; g11-05); halvings (g11-06); logarithm
  (mathematics grade 12); grid image (Book 1 g9).
- **Listings**: `merge.py` → output; `merge_sort.py` (with comparison count) → output; `count_vs_nlogn.py` → output;
  `fast_power.py` (multiplications counted) → output; `rotate_copy.py`, `rotate_quadrants.py` → outputs (small
  grids printed); `rotate_image.py` (PGM in, PGM out; checksum) → output; `measure_sorts.py` (merge vs insertion,
  MEASURED) → output.
- **Figures**: S merge sort split/merge tree on 8 numbers; S merging step with two pointers; S quadrant rotation of a
  4×4 grid (cycles of four quadrants, then recursion); C comparisons of merge sort vs n log₂ n and n² (from
  `figures/`); C measured times merge vs insertion (*laptop*, MEASURED).
- **Exercises**: ★ P merge of two lists; ★ C comparisons of merging lengths 3 and 4; ★ P recursion tree of merge sort
  on 6 items; ★ C multiplications for x¹³; ★ W `merge(a, b)`; ★★ F merge drops the tail; ★★ W iterative fast power;
  ★★ C prove merge sort's count for n = 2^h; ★★ P rotate a 2×2 then 4×4 grid; ★★ F mid computed so one half is
  empty; ★★ W `count_inversions` by merge; ★★★ C prove fast power uses at most 2·(halvings of n) + 1 multiplications;
  ★★★ W in-place quarter rotation by layers, tested against the copy; ★★★ C why merge sort's count is the same for
  every input order up to a factor 2; ★★★ W maximum subarray by divide and conquer, tested against brute force.
- **Problem** "Counting inversions": I a ranking of n items compared with another; II brute force count and cost;
  III a merge-sort variant counting inversions, proved; IV its count of comparisons and the measured speed-up at
  n = 10⁵. **Named result**: the number of inversions between two seeded rankings and the measured ratio of the two
  methods (MEASURED, shape tested).
- **Ledger**: von Neumann 1945 merge sort (Knuth's attribution; primary? — `history` box only if sourced, else omit).

#### g12-07 Dynamic Programming — `dynamic-programming` (~13 pp)
- **Hook**: the naive Fibonacci of g12-01 recomputes the same values millions of times; writing them down fixes it.
- **Sections**: 1 Overlapping subproblems (call tree recalled; memoisation with a dictionary; `functools.cache`
  told); 2 The bottom-up table (the same recurrence filled in order; space saving); 3 Change with the fewest coins (the
  recurrence; the table; works where greedy failed in g11-07; rebuilding the coins used); 4 The longest common
  subsequence and the alignment of two texts (recurrence, table as a grid, rebuilding; edit distance between two versions
  of a sentence, shown as an alignment); 5 The 0/1 knapsack (recurrence on items and capacity; the table; rebuilding;
  memory cost n·W and the cost discussion).
- **Recalls**: recursion (g12-01); greedy (g11-07); grid as list of lists (Book 1 g9); dictionary (Book 1 g8).
- **Listings**: `fib_memo.py` (call counts naive vs memo) → output; `fib_table.py` → output; `change_dp.py` (coins
  1, 3, 4 and amount 6; rebuild) → output; `lcs.py` (table printed for two short words) → output; `align.py` (edit
  distance + alignment of two versions of a sentence) → output; `knapsack_dp.py` → output; `table_sizes.py` (memory
  of tables for growing inputs) → output.
- **Figures**: S fib call tree with memoised nodes cut; S change table with arrows of the rebuild; S LCS grid with the
  rebuild path; S knapsack table (items × capacity) with the chosen cells; C calls naive vs memo vs n (from
  `figures/`).
- **Exercises**: ★ P memoised calls count; ★ C change table for amount 7; ★ C LCS length of two short words; ★ P
  knapsack table cell; ★ W memoised `binomial(n, k)` (Pascal's rule); ★★ F memo key missing an argument; ★★ W
  `min_coins` bottom-up; ★★ F table filled in the wrong order; ★★ C number of paths in a 5×5 grid moving right/down;
  ★★ W `lcs_string` rebuild; ★★ P alignment of two given strings; ★★★ C prove the change recurrence; ★★★ W edit
  distance with the operations listed; ★★★ C table size and time of the knapsack for n items, capacity W; ★★★ W
  longest increasing subsequence in n² with rebuild.
- **Problem** "Aligning two versions": I two versions of a paragraph (invented); II LCS of their words; III edit
  distance in words with the alignment; IV the cost of the table and a saving to two rows. **Named result**: the edit
  distance between the versions and the alignment, with the table's memory reduced from n·m to 2·m cells (counts from
  the run).
- **Ledger**: Bellman 1950s "dynamic programming" naming for a `history` box (primary source page or omit).

#### g12-08 Searching in Text — `text-search` (~12 pp)
- **Hook**: finding a word in a long text by checking every position works; it can be made to skip most of them.
- **Sections**: 1 The naive search (every alignment; comparisons counted; worst case (n − m + 1)·m on `aaa…ab`);
  2 Preprocessing the pattern (the bad-character idea: on a mismatch, how far may the pattern jump?);
  3 Boyer–Moore–Horspool (the shift table from the pattern; the method; correctness argued: no occurrence is skipped);
  4 Cost in practice (measured comparisons on generated texts: random letters, a 4-letter alphabet, the town's book
  titles concatenated; worst case of Horspool told); 5 Several patterns at once (told: an automaton / trie idea, pointer
  to the Year 2 volume) and Python's `str.find` (`inpractice` box).
- **Recalls**: string (Book 1 g7; g10-05); cost (g11-06); dictionary (Book 1 g8).
- **Listings**: `naive.py` (positions + comparisons) → output; `worst_naive.py` → output; `shift_table.py` → output;
  `horspool.py` (trace of alignments) → output; `compare_counts.py` (seeded texts) → output; `town_titles.py` →
  output; `measure_find.py` (naive vs Horspool vs `str.find`, MEASURED) → output.
- **Figures**: S naive alignment of a pattern under a text (successive shifts); S Horspool's shift table for one
  pattern; S a Horspool jump: mismatch, last character of window, jump distance; C comparisons per text character vs
  pattern length for naive and Horspool (from `figures/`).
- **Exercises**: ★ P positions found; ★ C comparisons of naive on a small case; ★ C shift table of `"BANANA"`; ★ P
  Horspool alignments; ★ W `count_occurrences(text, p)` naive; ★★ F naive range stops one alignment early; ★★ W
  `shift_table(p)`; ★★ F shift computed with the last character included; ★★ C worst case of naive for n, m; ★★ P
  overlapping occurrences; ★★ W case-insensitive search; ★★★ C prove Horspool never skips an occurrence; ★★★ C a
  text and pattern where Horspool makes m(n−m+1) comparisons; ★★★ W search with a single wildcard `?`; ★★★ C average
  shift for a random text on a 4-letter alphabet, measured and explained.
- **Problem** "Searching a long chain of letters": I a seeded 4-letter text of 10⁶ letters; II naive counts; III
  Horspool counts for m = 4…32; IV the ratio of comparisons. **Named result**: comparisons per text letter of
  Horspool vs pattern length (from the run): the longer the pattern, the fewer letters read.
- **Ledger**: Boyer & Moore 1977 (CACM), Horspool 1980 (Software: Practice and Experience) — primary pages for the
  `history` box.

#### g12-09 Relational Databases and SQL — `relational-databases-sql` (~15 pp)
- **Hook**: the town library's loans kept in one big spreadsheet: a member who moves must be changed in forty rows.
- **Sections**: 1 Why flat files fail (one wide table built from the town's loans: redundancy; insertion, deletion
  and update anomalies, each shown); 2 The relational model (relation, attribute, domain, row; primary key, foreign
  key; relational schema; integrity constraints of domain, relation and reference; structure vs content);
  3 Querying (SELECT … FROM … WHERE; DISTINCT; ORDER BY; aggregate functions COUNT/SUM/AVG/MIN/MAX over a whole
  selection, **no GROUP BY** — left to the Year 1 volume; joins with JOIN … ON; NULL for books still out);
  4 Changing data (INSERT, UPDATE, DELETE; a foreign-key violation refused, with `PRAGMA foreign_keys = ON`);
  5 What a database system guarantees (persistence, concurrent access, efficient queries, access control — described;
  SQL from Python with `sqlite3` and parameters `?`; `safety` box: never build SQL by pasting user text — a staged
  injection on the book's own toy table and its fix).
- **Recalls**: join of two tables, missing data (g10-07); text file, table of records (Book 1 g8).
- **Listings**: `flat_table.py` (builds the wide table, shows the anomalies) → output; `schema.sql` (NORUN; the
  library schema with keys) ; `create.sql` (`-- load: schema.sql`) → output; `select_where.sql` (`-- load: town`) →
  output; `distinct_order.sql` → output; `aggregates.sql` → output; `joins.sql` (titles out with member names) →
  output; `still_out.sql` (`return_date IS NULL`) → output; `changes.sql` (INSERT/UPDATE/DELETE, a refused foreign
  key) → output; `from_python.py` (`sqlite3`, parameters) → output; `injection.py` (staged, then fixed) → output.
- **Figures**: S the flat table with redundant cells shaded; S the schema diagram (tables with primary keys
  underlined, foreign-key arrows) of the town library; S a join drawn as matched rows; S the layers: program →
  SQL → database system → file; AI a library desk with returned books (no text) — optional.
- **Exercises**: ★ P result of a SELECT on a tiny table; ★ C primary key of a given relation; ★ P DISTINCT count;
  ★ W query: books by one author ordered by year; ★ F missing join condition (cross product size); ★★ W query: members
  with a book still out; ★★ C rows of a join; ★★ F `= NULL` instead of `IS NULL`; ★★ W UPDATE of a due date; ★★ P
  which DELETE is refused with foreign keys on; ★★ C anomaly types in a given flat table; ★★★ W schema for a
  timetable with keys and constraints; ★★★ W a Python function that runs a parameterised query, tested; ★★★ C prove a
  relation has at least one key (the set of all attributes); ★★★ F injection in a query built with an f-string, fix.
- **Problem** "The overdue books of Brenmoor": I the schema; II loans still out and overdue at a given date; III the
  members concerned and their streets; IV the total days of delay. **Named result**: the number of books overdue on
  the chosen date and the total days late (from a run on the town).
- **Ledger**: Codd 1970 (CACM) for the `history` box; SQL standard ISO/IEC 9075 (year of first standard 1986/87);
  SQLite docs: foreign keys pragma, NULL handling, `sqlite3` parameter style (SQLITE, PYTHON-DOCS rows).

#### g12-10 Processes and Scheduling — `processes-and-scheduling` (~13 pp)
- **Hook**: a laptop with four cores runs three hundred programs "at once".
- **Sections**: 1 Program and process (a process is a running program with its memory, registers, open files;
  creating a process from Python with `subprocess`; observing processes with a standard tool, `ps`, in a session if it
  captures deterministically — else described); 2 The states of a process (ready, running, blocked; the transitions;
  a state diagram — recalled as a state machine from g10-10); 3 The scheduler (interrupts: the clock interrupts the
  running process; round robin with a quantum; first come first served; a scheduler simulated in Python with a given
  workload; turnaround and waiting times; the context switch and its cost); 4 Two processes and one resource (race
  conditions shown with a deterministic interleaving simulator; critical section; mutual exclusion with a lock; the
  lost update counted); 5 Deadlock (two locks taken in opposite orders; the four conditions; avoiding by ordering
  resources; a resource-allocation graph and its cycle).
- **Recalls**: kernel, shell, permissions (g11-03); state machine (g10-10); queue (g12-03); graph cycle (g12-05).
- **Listings**: `spawn.py` (`subprocess.run` of a child Python; exit status) → output; `ps_session.sh` (`# capture:
  session`, `sleep 2 & ps -o stat=,comm=`; kept only if deterministic) → output; `scheduler.py` (NORUN module);
  `fcfs_rr.py` (one workload, FCFS vs RR q = 2, 4; Gantt rows as text) → output; `interleave.py` (two "processes" as
  generators, every interleaving of `counter += 1` split into load/add/store; lost updates counted) → output;
  `with_lock.py` (same with a lock: no lost update) → output; `deadlock_sim.py` (two processes, two locks, the
  interleaving that blocks; detection by a cycle in the wait-for graph) → output.
- **Figures**: S process state diagram (automata library); S Gantt chart of RR q = 2 from the simulator's output;
  S the interleaving that loses an update (two timelines, shared variable); S resource-allocation graph with a cycle;
  P none; AI none.
- **Exercises**: ★ P FCFS order; ★ C waiting times for FCFS; ★ P RR Gantt for q = 1; ★ C context switches of RR;
  ★ W `turnaround(schedule)`; ★★ F RR forgets to requeue an unfinished process; ★★ C count interleavings of two
  3-step processes (binomial 6 choose 3 = 20, listed by program); ★★ W shortest-job-first scheduler; ★★ F lock released
  on one path only; ★★ P final counter for a given interleaving; ★★ C which of the four conditions a given design
  breaks; ★★★ C prove lost updates are impossible with the lock (case argument); ★★★ W wait-for-graph deadlock
  detector; ★★★ C mean waiting time FCFS vs SJF on a given workload, and why SJF is optimal for it (exchange
  argument); ★★★ F dining-philosophers deadlock, fixed by ordering.
- **Problem** "Choosing the quantum": I a workload of five processes; II FCFS times; III RR for q = 1…8 with a
  context-switch cost; IV the quantum minimising the mean turnaround. **Named result**: the best quantum for the
  given workload and switch cost, and its mean turnaround against FCFS (from the simulator).
- **Ledger**: Coffman, Elphick and Shoshani 1971 (the four conditions, ACM Computing Surveys) for the `history` box;
  `ps` options (POSIX `ps` page); typical context-switch time in a `dated{2026}` box only if sourced (else omit).

#### g12-11 Routing — `routing` (~13 pp)
- **Hook**: a cable between two routers is cut; within seconds, packets take another way.
- **Sections**: 1 A network as a weighted graph (routers as vertices, links as edges, costs from hop count or from
  link speed; a routing table per router; recall of g11-04); 2 Distance-vector routing by exchanged tables (each
  router tells its neighbours its distances; Bellman–Ford update; rounds until stable; simulated); 3 Slow convergence
  (after a failure: counting to infinity, 16 as infinity in the hop-count protocol; split horizon told);
  4 Link-state routing (every router learns the whole map by flooding; runs Dijkstra from g12-05; costs from link
  speeds as reference rate ÷ link rate); 5 A route recomputed after a failure (both methods on the same network; the
  route of a packet read from the tables).
- **Recalls**: protocol, layer, routing table (g11-04); graph (g10-09); Dijkstra's algorithm (g12-05).
- **Listings**: `network.py` (NORUN: an invented 7-router network with link rates); `dv_rounds.py` (tables after each
  round) → output; `count_to_infinity.py` (a 3-router line, a failure, the counts climbing to 16) → output;
  `split_horizon.py` → output; `link_state.py` (Dijkstra per router, tables) → output; `ospf_costs.py` (costs from
  rates) → output; `failure.py` (both methods after a link failure; routes printed) → output.
- **Figures**: S the invented network with link rates and costs; S routing tables of two routers side by side;
  S counting to infinity: three routers and their advertised distances by round (table); S link-state flooding and the
  shortest-path tree of one router.
- **Exercises**: ★ P table after one DV round; ★ C hop count route; ★ C cost-based route; ★ P next hop from a table;
  ★ W `dv_update(table, neighbour_table, cost)`; ★★ F DV update keeps the larger distance; ★★ C rounds to converge on
  a line of n routers; ★★ W `cost_from_rate(rate, ref)`; ★★ P route after failure; ★★ F link-state ignores a one-way
  failure; ★★ C messages flooded in a ring of n routers; ★★★ C prove DV distances after k rounds are shortest among
  paths of ≤ k links; ★★★ C count to infinity: rounds needed to reach 16 from a given start; ★★★ W poison reverse
  (told then coded); ★★★ C why a hop count of 16 limits the network's diameter to 15.
- **Problem** "Counting to infinity": I a line of routers A–B–C; II the stable tables; III the link B–C fails: rounds
  of updates with and without split horizon; IV the same with link state. **Named result**: the number of rounds until
  C is marked unreachable (16) without split horizon vs one round with it (from the simulator).
- **Ledger**: RIP v2 RFC 2453 (metric 1–15, 16 = infinity, 30 s updates if printed); OSPF v2 RFC 2328 (cost =
  reference bandwidth / interface bandwidth; default reference 10⁸ bit/s — check RFC vs implementation docs);
  Bellman 1958 / Ford–Fulkerson 1962 for a `history` box (optional).

#### g12-12 Cryptography and Secure Communication — `secure-communication` (~14 pp)
- **Hook**: a browser and a server that have never met agree on a secret while everyone listens.
- **Sections**: 1 Symmetric encryption and the problem of sharing the key (one key to encrypt and decrypt; recall of
  Book 1 g9's ciphers; XOR with a key stream from a seeded generator as a toy stream cipher — insecure, said so; real
  ciphers named in a `inpractice` box); 2 Agreeing on a key in public (Diffie–Hellman with small numbers: modular
  powers recalled from the mathematics book, fast power from g12-06; what an eavesdropper sees; brute force of the
  discrete logarithm on small numbers, counted); 3 A key pair (public key, private key; the miniature RSA recalled from
  the mathematics book; encrypting with the public key; signing with the private key and checking with the public key);
  4 Hash functions (fixed-size digest, `hashlib.sha256`; small change, large change; integrity; a signature signs a
  digest; storing passwords as salted hashes — `safety` box); 5 Certificates and the steps of a secure web connection
  (a certificate binds a name to a public key, signed by an authority; a toy chain checked; the HTTPS steps: hello,
  certificate, key exchange, symmetric session key, encrypted HTTP — cipher negotiation not studied; why the padlock
  means what it means).
- **Recalls**: cipher, key, frequency analysis (Book 1 g9); HTTP (g10-08); modular arithmetic, fast powers, miniature
  RSA (mathematics grade 12); fast exponentiation (g12-06); bitwise xor (g10-03).
- **Listings**: `xor_stream.py` → output; `xor_reuse.py` (two messages with one key stream: their xor leaks, staged) →
  output; `diffie_hellman.py` (p = 23-style small numbers, then a 61-bit prime) → output; `brute_dlog.py` (steps
  counted for growing p) → output; `mini_rsa.py` (key generation from given small primes, encrypt, decrypt, sign,
  verify) → output; `hashes.py` (sha256 of close messages) → output; `salted.py` → output; `toy_certificate.py`
  (a chain of two toy signatures checked; a forged one rejected) → output; `handshake_steps.py` (the message
  sequence simulated between two local objects, printed) → output.
- **Figures**: S symmetric vs asymmetric: who holds which key; S Diffie–Hellman exchange (Alice, Bob, the listener;
  values from the run); S signing and verifying a digest; S certificate chain (root → intermediate → site); S HTTPS
  handshake sequence diagram (simplified); P an Enigma machine (museum photo, free licence) in a `history` box.
- **Exercises**: ★ C xor of two bytes; ★ P digest lengths; ★ C 5^6 mod 23; ★ P mini-RSA decrypt; ★ W `xor_bytes`;
  ★★ F key stream reused; ★★ W `dh_shared(p, g, a, B)`; ★★ C brute-force steps doubling with each bit; ★★ F signature
  checked against the message instead of its digest; ★★ P which keys each party must keep secret; ★★ W `verify(msg,
  sig, pub)` for mini-RSA; ★★★ C prove Alice and Bob get the same secret (exponent laws, modular); ★★★ C prove
  mini-RSA decryption returns the message on the chapter's example (with the mathematics book's Fermat recalled);
  ★★★ W password check with salt and many rounds (`hashlib.pbkdf2_hmac`); ★★★ C man-in-the-middle on unauthenticated
  Diffie–Hellman: what the attacker needs, and why certificates stop it.
- **Problem** "A secret agreed in public": I a small prime and generator; II the exchange; III the listener's brute
  force, counted for primes of 10…40 bits; IV the time for 2048 bits extrapolated. **Named result**: brute force
  steps double with each bit of the prime (measured counts to 40 bits) — and the extrapolated time for a 2,048-bit
  prime, an astronomically large number of years.
- **Ledger**: Diffie & Hellman 1976 (IEEE Trans. Inf. Theory), Rivest–Shamir–Adleman 1977/78 (CACM) for `history`
  boxes; SHA-256 FIPS 180-4 (256-bit digest); TLS 1.3 RFC 8446 (handshake steps, 2018); X.509 RFC 5280; AES FIPS 197
  named in `inpractice`; recommended key sizes in a `dated{2026}` box (NIST SP 800-57 page); Enigma photo credits.

#### g12-13 What Programs Cannot Do: The Halting Problem — `halting-problem` (~12 pp)
- **Hook**: a tool that would tell, for any program, whether it ever stops would end most testing; it cannot exist.
- **Sections**: 1 A program is data (source text read by programs: an interpreter of the toy machine — the shared
  simulator recalled; a compiler named; Python reading Python with `ast`; programs downloaded as files);
  2 Decidable problems (a decision problem; an algorithm that always stops with yes or no; examples: primality,
  "does this toy program halt within 1,000 steps"); 3 The halting problem (statement; the proof by contradiction with
  the contrarian program, written as Python with the impossible `halts` as a parameter; the diagonal idea); 4 Other
  undecidable questions (told: does a program ever print X, are two programs equivalent; Rice-style statement told
  without proof) and computable does not mean feasible (an exhaustive search that stops after 2^n steps);
  5 One algorithm, several languages (Euclid's algorithm in Python, in toy assembly and as a recursive SQL query, read
  side by side: computability does not depend on the language; `history` box: Turing 1936 and Church).
- **Recalls**: von Neumann model, assembly (g11-02); recursion (g12-01); the toy machine (g11-10).
- **Listings**: `read_program.py` (`ast` counts the loops of a file) → output; `toy_interpreter_use.py` (runs a
  `.toy` program stored as a string) → output; `halts_within.py` (decides halting within k steps for toy programs) →
  output; `contrarian.py` (NORUN: the proof's program, with `halts` as an argument; never run with a real decider);
  `try_contrarian.py` (feeds a candidate "decider" — any concrete function — and shows it is wrong on the contrarian)
  → output; `euclid.py`, `euclid.toy`, `euclid.sql` (`WITH RECURSIVE`) → outputs.
- **Figures**: S program as data: a program box receiving another program's text; S the diagonal table (programs ×
  inputs, the contrarian flipping the diagonal); S the proof's two cases as a flow; S the same Euclid in three
  languages aligned.
- **Exercises**: ★ P `halts_within` on a short loop; ★ C steps of a given toy program; ★ P what `ast` counts; ★ C
  diagonal of a small table flipped; ★ W `count_functions(path)` with `ast`; ★★ C why "halts within k steps" is
  decidable; ★★ F a "decider" that runs the program and waits; ★★ W a toy-machine state repeat detector (halts or
  repeats) for programs without `IN`; ★★ C number of states of the toy machine without input (counted, finite); ★★ P
  output of `try_contrarian` for a given candidate; ★★ C is "does this program print anything" decidable? (reduce
  from halting, argued); ★★★ C prove the contrarian argument fully in your own words; ★★★ C a finite-memory machine
  halts or loops within its number of states (pigeonhole); ★★★ W Euclid in toy assembly with subtraction, tested;
  ★★★ C why Python programs are not finite-memory machines (unbounded integers and lists).
- **Problem** "A machine that can be decided": I the toy machine without `IN` has finitely many states; II the bound;
  III a repeat detector that decides halting for it; IV why the same idea fails for Python. **Named result**: every
  toy program without input halts or repeats a state within 2^2,099 steps (256 bytes of memory + 4 registers +
  PC + SP = 262 bytes, plus 3 flag bits: 8·262 + 3 = 2,099 bits; computed in the solution) — decidable in principle, infeasible in practice.
- **Ledger**: Turing 1936 ("On Computable Numbers", Proc. LMS) and Church 1936 for the `history` box; SQLite
  `WITH RECURSIVE` (SQLITE docs).

#### g12-14 Project: A Route Planner — `project-route-planner` (~14 pp)
- **Specification (one paragraph)**: a program that answers "fastest route from place A to place B" in Brenmoor:
  places and roads stored in an SQLite database built from the town; loaded into a graph with travel times from length
  and speed limit, one-way roads respected; Dijkstra's algorithm returning the route and its time; a `RoutePlanner`
  class with a documented interface; a text interface; every function tested.
- **Milestones**: M1 the database (schema with keys, loading the town, SQL queries for places and roads); M2 the graph
  (class `Graph`; travel time in seconds; one-way roads as single arcs; checks: connected, symmetric except road 1);
  M3 shortest routes (Dijkstra with parents; route rebuilt; distance vs time criteria); M4 the interface (class
  `RoutePlanner`; a text menu with `.stdin`; errors for unknown places); M5 tests and a measure (unittest suite;
  all-pairs times; the slowest pair; a closed road recomputed).
- **Recalls**: g12-09 (SQL), g12-05 (Dijkstra), g12-02 (classes), g11-09 (modules), g10-09 (graphs), g10-01 (tests).
- **Listings**: `db.py`, `graph.py`, `planner.py` (NORUN modules, grown by milestone with stems `*_m1` … as needed);
  `run_m1.py` … `run_m5.py` → outputs; `menu.py` + `menu.stdin` → output; `test_planner.py` → output; `queries.sql`
  (`-- load: town`) → output.
- **Figures**: S architecture (database → graph → algorithm → interface); S the town map with places and roads drawn
  from the data, a computed route highlighted; S the schema of the planner's database; S class diagram of
  `RoutePlanner` and `Graph`; AI a cyclist reading a paper map at a crossroads (optional, no text).
- **Exercises** (15, 5/6/4): ★ P route printed for two places; ★ C travel time of a road from length and speed; ★ P
  query result; ★ C arcs in the graph from 53 roads with one one-way; ★ W `place_id(name)` with error; ★★ F one-way road
  added both ways; ★★ W shortest by distance option; ★★ F times in hours mixed with seconds; ★★ C Dijkstra runs for all
  pairs; ★★ W closing a road and recomputing; ★★ P menu session for a given input; ★★★ W routes avoiding a place;
  ★★★ C prove the route returned is a shortest one (recall of the invariant); ★★★ W the k places reachable within t
  minutes; ★★★ C the slowest pair and why it is slow (read off the map).
- **Ledger**: none (town data invented); the 30 places / 53 roads counts are printed from runs.

## 3. Ledger plan (rows to fetch while writing; ids minted at the chapter)

~150 rows, ~250 fetches. Primary pages only: RFC Editor (RFC 20, 768, 791, 1951, 2328, 2453, 3629, 3986, 4180,
4632, 5280, 5737, 6265, 8200, 8259, 8446, 9110, 9112, 9293), IANA ports, Unicode (code space, 1.0 date, current
version in `dated`), IEEE 754 (binary64 layout; or Python `sys.float_info` + a primary description), The Open Group
Base Specifications (epoch, `chmod`, `ls -l`, `ps`), GNU coreutils manual, FSF and OSI definitions, Python 3.12
docs (`unittest`, `doctest`, `struct`, `math.ulp`, `sys.getrecursionlimit`, `http.server`, `sqlite3`, `hashlib`,
`dis`), SQLite docs (foreign keys, `WITH RECURSIVE`), FIPS 180-4, FIPS 197, NIST SP 800-57 (`dated` key sizes),
GAO IMTEC-92-26 (clock drift), IEC 60908 / a primary description of the disc audio format, Microsoft RIFF/WAVE,
Netpbm, CIPA DC-008 (EXIF), gpsd's NMEA documentation, papers' publisher pages for `history` boxes (Turing 1936,
von Neumann 1945, Manchester 1948, Dijkstra 1959, Codd 1970, Diffie–Hellman 1976, RSA 1978, Boyer–Moore 1977,
Horspool 1980, Coffman 1971, Milgram 1967, Lucas 1883, Cover–Hart 1967), CERN pages (the web, 1989–91).
A fact whose source cannot be fetched is dropped from the text, not printed from memory.

## 4. Open points for the sync (also in the Phase A report)

1. Ownership moves proposed in `DEFINITIONS.md` §D: *protocol* and *port number* to g10-08; *assembly language* stays
   g11-02 (Book 1 must not define it); *tree* to g12-04 (Book 1 has *folder tree*, which is fine); *resolution* is
   Book 1 g5's (Book 2 recalls it; drop g10-06's pair); ASCII to g10-05 unless Book 1 g5 owns it.
2. Shared style: `\omcode` falls back to C++ highlighting for `.pgm`, `.ppm`, `.stdin` (plain text in g10-06, g10-10,
   g12-14): ask the main session to add them to `\om@lstlang`'s plain list (one appended line), or Book 2 prints
   those files with a `.txt` copy. No other style need found; sequence diagrams and Gantt charts are plain TikZ.
3. `ps` in g12-10: kept only if `ps -o stat=,comm=` captures byte-identically; otherwise the observation is told and
   the simulator carries the section.
4. NMEA 0183 is a paid standard: the decoding exercise is kept only if gpsd's public documentation states the field
   order; otherwise an invented "position sentence" is used and the real format is named in prose without detail.
5. The SNT text was read from the pre-publication arrêté copy (the BO and eduscol pages refused or redirected);
   its seven themes and tables match the published programme's structure, but the main session may want to confirm on
   the BO.
