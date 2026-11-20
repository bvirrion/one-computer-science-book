# Book 2 (grades 10–12) — progress

## 2026-11-20 — Phase A done

- Programme texts read (SNT seconde: pre-publication arrêté copy; NSI première: eduscol document 30007; NSI
  terminale: eduscol document 30010; seconde mathematics, algorithmique section). Coverage table and uncovered items:
  `BRIEFS.md` §1.
- `BRIEFS.md`: book-wide decisions, 35 chapter briefs (sections, recalls, listings, figures, 15 exercises with kinds,
  weekend problem with its named result, ledger needs), ledger plan, open points for the sync.
- `DEFINITIONS.md`: owned terms per chapter with labels, Book 1 recalls, other-series recalls, contested terms,
  one-sense-per-word plan for the Phase C term config.
- Web fetches so far: 16 (programme texts and searches). Ledger rows: 0.
- Nothing written under `parts/` or `code/`; no shared file touched.

Sync applied to `DEFINITIONS.md` (2026-11-20).

## Chapters

| Ch. | Pages (body + sol.) | Listings | Outputs | Tests | Figures S/P/AI | Ledger rows | Notes |
|---|---|---|---|---|---|---|---|
| g10-01 specifications-and-tests | 13 + 4 | 12 (9 printed) | 8 | 10 pytest | 3/0/0 | 3 | done 2026-11-20 |
| g10-02 tuples-sets-comprehensions | 11 + 3 | 10 printed + 10 exercise files | 10 | 11 pytest | 4/0/0 | 0 | done 2026-11-20 |
| g10-03 machine-integers | 12 + 3 | 7 printed + 6 exercise files | 7 | 9 pytest | 4/0/0 | 5 | done 2026-11-20 |
| g10-04 floating-point | 13 + 3 | 8 printed + 6 exercise files, 1 figure script | 8 | 9 pytest | 3/1 chart/0 | 10 | done 2026-11-20 |
| g10-05 text-encodings | 12 + 3 | 7 printed (+1 NOPRINT) + 6 exercise files | 8 | 7 pytest | 4/0/0 | 7 | done 2026-11-20 |
| g10-06 images-sound-compression | 10 + 3 | 7 printed + 6 exercise files, 1 figure script | 7 | 9 pytest | 3/1 chart/0 | 4 | done 2026-11-20 |
| g10-07 data-tables | 10 + 3 | 8 printed + 5 town CSV copies + 4 exercise files, 1 figure script | 8 | 10 pytest | 3/1 chart/0 | 2 | done 2026-11-20 |
| g10-08 http-clients-servers | 11 + 3 | 8 printed (library_site in 3 ranges, page.html) + serve.py helper + 4 exercise files | 7 | 6 pytest (local servers 42095-42096) | 4/0/0 | 8 | done 2026-11-20 |
| g10-09 graphs-first-look | 11 + 3 | 6 printed + 3 town CSV copies + 3 exercise files, 1 figure script; `code/grade-10/lib/given_graphs.py` (black box) | 6 | 8 pytest | 4/0/0 | 1 | done 2026-11-20 |
| g10-10 sensors-actuators-control | 10 + 3 | 6 printed (+ `sensor.py` NORUN module, `lift_menu.stdin`), 2 exercise files, 1 figure script | 6 | 5 pytest | 4/0/0 (P, AI deferred to Phase C) | 0 | done 2026-11-20 |
| g10-11 project-web-application | 12 + 3 | 13 printed ranges over 11 files (+ `data.py`, `client.py`, CSV copies), 1 exercise module | 5 | 4 pytest (incl. the unittest suite against the real server) | 4/0/0 | 2 | done 2026-11-20 |
| g11-01 gates-to-arithmetic-unit | 12 + 3 | 8 printed (+ `gates.py` NORUN), 1 exercise file | 8 | 5 pytest (ALU checked against the shared toy machine on 305 pairs x 4 ops) | 5/0/0 (P deferred to Phase C) | 0 | done 2026-11-20 |
| g11-02 von-neumann-machine | 14 + 4 | 10 printed (8 .toy, `py_dis.py`, `step_counts.py`; `asm_listing.sh` output only), 9 exercise .toy | 10 | 4 pytest (every .toy run through `toymachine` on many inputs) | 5/0/0 (P deferred to Phase C) | 3 | done 2026-11-20 |
| g11-03 os-and-command-line | 12 + 3 | 9 printed (7 shell sessions, `timetable.py`, `policy.py`), 2 exercise scripts | 9 | 4 pytest (pipelines on the town CSV, shell traps, modes, policy) | 4/0/0 | 7 | done 2026-11-20 |
| g11-04 network-protocols | 15 + 4 | 9 printed (`lossy_channel.py` NORUN), 1 exercise module | 9 | 4 pytest (masks for all 33 prefixes, lookup vs listing, alternating bit on 200 seeds at 40 % loss, windows) | 4/0/0 (P deferred to Phase C) | 13 | done 2026-11-20 |
| g11-05 proving-algorithms-correct | 12 + 4 | 7 printed, 1 exercise module | 7 | 4 pytest (sorts on 300 random lists, search on 300 lists x 102 targets, isqrt to 3000, exercises) | 4/0/0 | 4 | done 2026-11-20 |
| g11-06 cost-of-an-algorithm | 12 + 4 | 9 printed (3 MEASURED), `duplicates.py` NORUN module, 1 exercise module, 2 figure scripts | 7 | 4 pytest (counts, h(n) and binary bound to 5000/300, exercises, measured shape) | 4/2/0 (2 charts from figures/) | 0 | done 2026-11-20 |
| g11-07 greedy-algorithms | 12 + 4 | 7 printed, 1 exercise module | 7 | 4 pytest (change vs exhaustive to 120, activities and rooms vs all subsets on 200 random sets, knapsacks, Brenmoor) | 4/0/0 | 1 | done 2026-11-20 |
| g11-08 k-nearest-neighbours | 12 + 4 | 8 printed + 1 NORUN module, 1 exercise module, 3 figure scripts | 8 | 4 pytest (data split, knn vs exercise on 100 random sets, results, exercises) | 4/0/0 (AI parcel desk deferred to Phase C) | 2 | done 2026-11-20 |
| g11-09 modules-and-interfaces | 11 + 4 | 12 printed (5 NORUN modules, 1 MEASURED, 1 shell session), exercise modules incl. staged circular import and import side effect, 1 figure script | 9 | 5 pytest (geometry rewrite, three dateset implementations agree on 300 random ops, exercises, chosen at import, staged faults) | 4/0/0 | 10 | done 2026-11-20 |
| g11-10 project-toy-machine | 14 + 3 | 7 printed + 6 NORUN modules (tokens, assembler_m2, simulator_m3/m4, trace_m5, ours_tests), 1 exercise module | 8 | 4 pytest (traces identical to the shared tool on all 8 g11-02 programs, 300 random memories stepped against the shared Machine, disassembly of all 28 672 words, exercises) | 4/0/0 | 0 | done 2026-11-20 |
| g12-01 recursion | 13 + 4 | 10 printed (1 NORUN), 1 exercise module, 1 figure script | 9 | 4 pytest (factorials, Hanoi moves legal and minimal n <= 10, Koch size, fib calls = 2 fib(n+1) - 1, exercises) | 4/0/0 (AI Hanoi toy deferred) | 3 | done 2026-11-20 |
| g12-02 classes-and-objects | 12 + 4 | 8 printed + 2 NORUN modules (fraction, date_class), 1 exercise module | 8 | 4 pytest (Fraction invariant on 500 random pairs, Date next/previous day against datetime on 1200 days, listing results, exercises) | 3/0/0 | 0 | done 2026-11-20 |
| g12-03 lists-stacks-queues | 13 + 4 | 9 printed (1 MEASURED) + 5 NORUN modules (cell, stack_list, stack_linked, queue_linked, queue_two_stacks), 1 exercise module | 9 | 6 pytest (both queues against deque on 3000 random operations, two-stack moves <= 3 per enqueue and = 3n when emptied, brackets against a reduction oracle on 2000 strings, post office numbers, exercises) | 5/0/0 | 0 | done 2026-11-20 |
| g12-04 trees | 12 + 4 | 6 printed + 2 NORUN modules (node, bst), 1 exercise module, 1 figure script | 9 | 3 pytest (BST against sorted sets on 200 random key lists: inorder, size, search, is_bst, size bounds, rebuild; listing numbers incl. 16/31/21.13; exercises) | 4 S + 1 C/0/0 | 0 | done 2026-11-20 |
| g12-05 graph-algorithms | 15 + 5 | 11 printed + 1 NORUN module (graph_class), 1 exercise module, 1 figure script | 11 | 4 pytest (BFS and Dijkstra against Floyd on 60 random graphs; DFS stack = recursive, has_path, undirected cycles against edges > n - components, directed cycles and topological order against all permutations; maze and town numbers; exercises) | 4 S + 1 C/0/0 | 1 | done 2026-11-20 |
| g12-06 divide-and-conquer | 13 + 6 | 10 printed (2 MEASURED), 1 exercise module, 2 figure scripts (1 measures itself) | 10 | 5 pytest (merge sort vs sorted with n h/2 <= count <= n h; power vs ** with the exact multiplication count; quadrant and layer rotation vs copy; inversions brute = merging on all lengths < 60 and the 10^5 count; exercises) | 3 S + 2 C/0/0 | 0 | done 2026-11-20 |
| g12-07 dynamic-programming | 15 + 5 | 9 printed, 1 exercise module, 1 figure script | 9 | 5 pytest (fib naive/memo/table and the 2n - 1 count; change table and top-down vs trying every combination for 4 systems; LCS vs every subsequence, alignment consistency and two-row distance on 150 random pairs; knapsack vs every subset on 60 random cases; exercises incl. diff and LIS) | 4 S + 1 C/0/0 | 2 | done 2026-11-20 |
| g12-08 text-search | 15 + 6 | 8 printed (1 MEASURED), 1 exercise module, 1 figure script | 8 | 3 pytest (naive = Horspool = regex on 400 random cases; exact worst cases of both; shift tables; exercises incl. wildcard and the measured mean jump of ex. 15) | 3 S + 1 C/0/0 | 2 | done 2026-11-20 |
| g12-09 relational-databases-sql | 15 + 5 | 11 printed (8 SQL through sqlrun, 3 Python; schema.sql NORUN), 1 exercise module | 11 | 4 pytest (exercise answers on the town db; timetable constraints refuse 3 bad rows; injection and parameter; problem counts) | 4 S/0/0 | 1 | done 2026-11-20 |
| g12-10 processes-and-scheduling | 12 + 3 | 8 printed (scheduler NORUN; ps_session.sh a deterministic session), 1 exercise module | 7 | 6 pytest (schedulers on 300 random workloads; listing and problem numbers; interleavings, lock, deadlock; exercises incl. SJF optimal over all orders) | 4 S/0/0 | 2 | done 2026-11-20 |
| g12-11 routing | 11 + 3 | 7 printed (network NORUN), 1 exercise module | 6 | 5 pytest (DV = Dijkstra on 100 random graphs; after k rounds = best with <= k links; listing numbers incl. flooding 2e-(n-1); exercises; triangle still counts with split horizon) | 4 S/0/0 | 5 | done 2026-11-20 |
| g12-12 secure-communication | 13 + 3 | 9 printed, 1 exercise module | 9 | 5 pytest (RSA round trip on all 3233 values, signatures; DH agrees on 3 primes; exercises incl. pbkdf2 and MITM; brute force and chain; problem numbers) | 5 S/0/0 (Enigma photo box deferred) | 5 | done 2026-11-20 |
| g12-13 halting-problem | 11 + 2 | 11 printed (contrarian, programs NORUN; .toy and .sql through the shared runners), 1 exercise module | 9 | 5 pytest (repeat detector = running on 4 programs and 200 random ones; every candidate wrong on its contrarian; exercises; bound) | 4 S/0/0 | 3 | done 2026-11-20 |
| g12-14 project-route-planner | 13 + 4 | 8 printed + 4 NORUN modules (db, graph, planner, planner_tests; `menu.stdin`; `queries.sql` with `-- load: town`), 1 exercise module, 1 figure script | 7 | 3 pytest (the unittest suite; Dijkstra = slow method from all 30 places; every exercise number) | 4/0/0 (AI cyclist optional, Phase C) | 0 | done 2026-11-20 |


### g10-01 notes
- Changes from the brief: unittest file named `leap_tests.py` (a `test_*.py` listing would be collected by pytest);
  the runner's timing line is removed with `grep -v '^Ran '` (explained in the text); the problem's mutants
  program is `exercises/mutants.py` (14 mutants; boundary suite kills 14, random suite 7). Figures: contract,
  nested kinds of year, decision diagram (no test-runner flow figure).
- `\code{}` cannot hold `\%` (detokenize prints the backslash): use `\texttt{year \% 4}` for code with a percent.

### g10-02 notes
- Problem result (run on the town): among the 49 members with at least 5 books, members 40 and 55 (Dara Reedfield,
  Umar Daleton) have the highest Jaccard index, 5/12 = 0.417; over all 60 members a degenerate 1/2 (1 and 2 books).
- `swap.py`/`point.py` of the brief folded into `tuples.py`/`named.py`; `immutable.py` added. A set literal with a
  repeat is flagged by ruff B033: built with `set([...])` instead.
- `\code{}` prints exactly what is typed: write braces and `&` bare (`\code{{1, 2}}`, `\code{a & b}`), never `\{`.
- A TikZ style must not be called `name` (pgf key clash): use `nm`.

### g10-03 notes
- Problem result: 2038-01-19 03:14:07 UTC, wrapping to 1901-12-13 20:45:52 UTC (exercises/rollover.py, tested).
- New source key POSIX (Open Group Base Specifications Issue 8). Rust overflow behaviour left out (no row).
- Appended to `styles/onecs.sty` (`% Book 2:`): `\DisableLigatures[<,>]{encoding = T1, family = tt*}` under
  `\ifpdftex`, because `\code{a << 2}` printed a guillemet in every book (reported).

### g10-04 notes
- Problem result: a tenth chopped after 23 binary places loses 0.8 x 2^-23 = 9.54e-8 s per tick; after 100 h
  (3.6 million ticks) the drift is 0.3433 s, and the program reproduces all six rows of the GAO report's
  Appendix II table (0.0034 ... 0.3433 s); 24 places would give 0.1287 s. GAO PDF read with pdftotext (copy in
  scratch). Sources GAO-PATRIOT, IEEE-754 added. The 1/11/52 split and bias come from the run (struct), not a row.

### g10-05 notes
- Problem result: the town's 30 place names take 301 B in UTF-8, 600 B in UTF-16, 300 B in Latin-1 (UTF-8 saves
  299 B, 49.8 %); rule: UTF-8 read as Latin-1 turns é (C3 A9) into Ã©.
- Listings and outputs may hold only ASCII plus é, ê (the `om` listings style has literate for those two only):
  mojibake is shown with `ascii()` and hex; the euro sign is written `\u20ac`; Ã, © appear only in prose/TikZ.
- No teleprinter photograph (brief had one): left for Phase C if time allows.
- `\code{can't}` prints a curly apostrophe (T1 tt position 39): avoid `'` in `\code`; reported.

### g10-06 notes
- Problem result: one minute of disc-quality stereo is 10,584,000 B = 10.09 MiB; zlib ratio 1.09 on synthetic music
  (three tones + noise, seeded) vs 909 on silence.
- Deferred to Phase C: the brief's photograph (sensor chip) and AI image (market square), and the `dated{2026}` box on
  phone sensor resolutions (needs a ledger row). Chapter is 10 pp without them.
- `\code{'x'}` apostrophes replaced by double quotes in g10-02, 03, 05 solutions (curly-quote defect).

### g10-07 notes
- Problem result: Riverside's corrected 2025 mean is 12.016 C over 360 days; the two -99.0 codes would give 11.402
  (error 0.614); the raw file (codes + duplicate) gives 11.430. The brief said "Hilltop"; the planted codes are at
  Riverside, so the result is Riverside's. Hilltop is 10.628 raw and clean.
- The listings read copies of five town CSVs in `listings/` (cwd); a test checks they equal `data/town/` byte for byte.
- Every member borrowed and every book was lent in 2025 (left joins are full); exercise 12 says so.
- TikZ `grid` steps in cm whatever x/y are: draw grids with explicit lines when x or y is not 1cm.
- No `\enquote` in this preamble: use ``...''.

### g10-08 notes
- Problem result: the library page is 5 requests, 1129 bytes of content (~1.8 KB with headers); at 50 ms latency
  10 round trips = 500 ms with a new connection per request, 6 = 300 ms with one reused connection.
- Ports used: listings 42080-42084, page_cost 42090, tests 42095-42097; all bound to 127.0.0.1.
- The site module is `library_site.py` (a module named `site` shadows Python's own `site`).
- The server is a class (BaseHTTPRequestHandler); classes are owned by grade 12, so the text says "read it as a set
  of functions"; the `serve.running` helper is not printed (NORUN), only described.
- `\code` cannot hold `\r\n` (prints a space after each backslash word): written with `\texttt{\textbackslash r...}`.

### g10-09 notes
- Problem result: the largest friendship component has 29 people, radius 4, diameter 7, centre {1, 28}; without the
  friendship 1-28 it stays connected but its diameter grows to 9 (centre {5, 37}).
- Components are 29 / 10 / 1 (the 15-27 group minus 18, 20, 25 is a component of its own); TOWN.md's "three groups
  joined by a few bridges" is about the numbering groups, not components. The problem is "Handshakes across Brenmoor".
- `distances` and `components` are given as a black box in `code/grade-10/lib/given_graphs.py` (grade 12 writes BFS).
- NMEA: gpsd's "NMEA Revealed" gives the GGA field order and checksum; the exercise sentence is invented, its
  checksum computed and tested.
- Milgram small-world history box dropped: the paper's scans are image-only, no verifiable primary text; the remark
  stays without numbers.

### g10-10 notes
- Problem result: the 3-floor lift has 12 reachable states (of 72 tuples), none with the door open and the motor
  running; the closure argument (every event maps the set into itself) is the proof. Calls 2, 0, 1, 2, 1 need
  3, 4, 3, 3, 3 events, mean 3.2.
- Simulated room (seed 4, 6 h): plain thermostat 214 switches, hysteresis band +-0.5 77 switches.
- `lift.step` is a function, not a dict table (72 tuples x 6 events); the traffic light keeps the dict table.
- The brief's "two states per actuator" photo (board/sensor) and the AI crossing image are deferred to Phase C,
  like g10-05/06's.
- Figure trap: the lift diagram needed three rows (closed / moving / open) and sloped call labels; open/close
  arrows are named in the caption instead of labelled.

### Page projection at chapter 10
- Chapters 1-10 take pp. 2-106 of text: 10.5 pp per chapter against the ~12 target (12.5 % under, inside the
  15 % margin), plus about 3 pp of solutions each.
- Projection: 35 chapters x 13.5 pp + front matter about 480 pp against the ~420 planned; grade 11 and 12 chapters
  are longer in the briefs, so depth is not being compressed. No action.

### g10-11 notes
- Project shape: `server.py` (given, NORUN) turns a request into a dict and calls `app.dispatch`; apps return
  `(status, type, text, headers)`, so tests call `dispatch` directly and also through the real server.
  Milestones are separate modules `app_m1/2/3/5.py`, each importing the previous one and replacing routes; the
  dispatcher of M1 is reused unchanged. Ports: 42110 (reader), 42111-42115 runs, 42116 the unittest suite.
- Brief's `test_app.py` renamed `app_tests.py` (pytest's `test_*.py` pattern would collect it); its output is
  captured through `run_tests.sh` with the `Ran ... in Xs` line filtered out, as in g10-01.
- Exercise 15 (race): the given server is threaded (`ThreadingHTTPServer`), so the race is real; the solution
  uses a `threading.Lock` and points to the databases chapter for several processes.
- Ledger: g10:http-405-allow, g10:html-escape (both fetched). No photo or AI planned for a project.
- Traps: a TikZ `\foreach` variable named `\path` silently draws nothing (it is a TikZ command); `\code` prints
  `#` doubled, so `&#x27;` needs `\texttt{\&\#x27;}`; `\code{\fun}` inside a foreach prints `\fun` literally.
- Shared: `tools/gates.sh grade-10` currently fails only on `sources/ledger/book5.md` rows 30-34 (Book 5's
  crossref source keys); not mine, left alone.

### g11-01 notes
- Problem result (from `gate_count.py`, which runs the adders on levels instead of bits): 64-bit ripple adder 320
  gates, 129 levels (2n + 1, the carry out last); carry-select of two halves 580 gates (9n + 4), 68 levels (n + 4):
  1.81x the gates for 0.53x the levels. The brief's "128-level carry path" is the c_in -> c_out path; the printed
  figure is the longest path from the inputs, 129.
- The ALU's C flag follows the toy machine (borrow for SUB = NOT carry out; 0 for logic ops); the tests run the
  gate ALU, a Python-integer reference and `toymachine` side by side.
- Induction is grade 12 only: problem Q5 is phrased as "two levels per column, deduce".
- Traps: in circuitikz, a coordinate like `(4.0 |- x1.out)` must be `(4.0,0 |- x1.out)`; `\code` cannot hold `%`
  (a whole build died with "File ended while scanning use of \code"), use `\texttt{... \% ...}`.
- Draft circuit figures in a scratch standalone file first: a full build costs a minute, a standalone two seconds.

### g11-02 notes
- Problem result (`step_counts.py`, b = 0..255, a = 13): repeated addition 8 + 3b steps, worst 773 (b = 255), mean
  390.5; shift and add 7 + 7L (L = bits of b), worst 63 (all b >= 128), mean 56.0. Repeated addition is faster only
  for b in 1..6 and 8 (at most 8 steps).
- `shift_multiply.toy` moved from the brief's exercise 11 into the problem (Part II); exercise 11 became
  `times_ten.toy` (10x = 8x + 2x with shifts). The brief's "sum of an array" exercise became `max_array.toy`, since
  `sum_array.toy` is a listing.
- `bad_return.toy`: a missing POP makes RET jump to R2's 40, an empty cell, i.e. HALT: the program prints nothing.
- `self_modify.toy` stores 80 over a HALT, which becomes OUT R0 (trace shows it).
- `py_dis.py` output is CPython 3.12 bytecode; the text says so (ledger g11:py-dis). Toy capture directive works in
  a `; capture: args=--trace` comment line (printed as line 2).
- Ledger: g11:edvac-1945 (CHM timeline, year only; the MIT PDF of the report is an image scan), g11:baby-1948.
- No booktabs in the preamble: tables use `\hline`.

### g11-03 notes
- Problem result (`policy.py`, all 512 modes per file, parents first): marks 755 -> 770, exam 644 -> 600, timetable
  666 -> 664, g11.csv 644 -> 660 (8 modes fit; the others' bits never apply once students cannot enter marks),
  /school and news unchanged; 8 permission bits change. Every other file has a unique fitting mode.
- Town facts printed: books.csv 81 lines (80 books); member 55 has most loans (12); 22 loans not returned; top authors
  Zoe Stoneton 7, Elif Ashworth 6, Quinn Ivymore 6.
- `cat f > f`: GNU cat refuses with "input file is output file" (exit 1) after the shell has emptied the file; the
  solution says "empty or refuses".
- Found a family of `\code{\...}` misuses: `\code` detokenizes, so `\code{\%}`, `\code{\{...\}}`, `\code{\$}`
  print the backslash. Fixed in g10-02 ex., g10-11 sol., g11-02 problem and sol. (now `\texttt{...}`), and here.
  Phase C: grep `code{[^}]*\\` across the book again.
- GNU philosophy pages answered 429 three times: free software sourced from fsf.org's "What is free software?" page
  (freedom to share, study, modify), not the four-freedoms list.

### g11-04 notes
- Problem result (`sea_link.py`, invented cable: 6000 km, 2e8 m/s, 1 Gbit/s, 1500-byte packets): T = 12 us,
  RTT = 60 ms; stop and wait busy 0.0200 % (one in 5001), 0.2 Mbit/s; smallest full window 5001 packets, 7.5 MB in
  flight. A 10 Gbit/s line leaves the useful rate at 0.2 Mbit/s.
- IP address is Book 1 g8's term: g11-04 defines only network mask and prefix (DEFINITIONS.md row updated; label
  `def:g11:network-protocols:ip-address` kept as mapped).
- All example addresses from RFC 5737's documentation blocks; names in `.example` (RFC 2606). Router table has no
  real public address (the default-route example is 203.0.113.5).
- Alternating-bit seeds 10/3 at 30 % loss give one lost ack and one lost packet over four messages (6 sends).
- No `dated` box on link rates (brief's ledger item): it would need sourced typical rates and adds nothing to the
  problem; the throughput table uses illustrative round numbers, said so by the listing's names.
- Also: the Baby box (g11-02) no longer names a university ("built in Manchester, England").

### g11-05 notes
- Problem result (`isqrt.py`): halving isqrt agrees with `math.isqrt` for 0 <= n <= 10^6, at most 20 turns, first at
  n = 555007 (bound: n + 1 <= 2^20); counting up takes 1000 turns at 10^6. No logarithm, no "induction" word (the
  bound in Q16 is argued by repeated halving).
- Staged bug output catches the RuntimeError and prints it (avoids the capture wrapper's traceback frames).
- Collatz exercise: ledger g11:collatz-open (Lagarias's annotated bibliography, arXiv abstract "remains unsolved").
- History: Floyd 1967, Hoare 1969 via Crossref metadata.
- Found and fixed: `\code{lo=\lo}` inside TikZ printed the macro name; `\code{...}` spans broken over two source
  lines in g11-02 caption, g11-03 text and solutions (now on one line); `\mid` used as a foreach variable shadowed
  the math macro (renamed `\md`); gate check_prose flags straight quotes inside `\pgfmathsetmacro` strings.

### g11-06 notes
- Problem result: on shuffled lists of distinct numbers (seed 2026), sort-then-scan needs fewer comparisons than all
  pairs for every n from 7 to 100; at n = 10^5, 1,628,843 against 4,999,950,000 (formula). Measured on the laptop
  (MEASURED, `dup_measure.py`): sort then scan 20.2 ms, set 5.1 ms, pairs predicted 81 s from n = 4000 x 625:
  speed-up about 4,000. Solutions quote these printed digits: **if MEASURED outputs are recaptured in Phase C,
  update g11-06 solutions (ex. 15, problem 11-16, 20) and `figures/measured_plot.dat`'s dashed-line heights.**
- Hook corrected to "takes hours" (pairs at 10^6 extrapolate to about 2 h on this laptop, not a week).
- Exercise 13's table shows n*h(n) below 100n at 10^6 (constants matter); test asserts that order.
- No `dated` clock-rate box (brief: only "if printed").
- Index: the build now ends with two `Overfull \vbox` (8.2 pt, 6.6 pt) on the index pages (multicol balancing, the
  known trap the entry file's comment on `\indexspace` mentions). Not caused by a chapter page; depends on the number
  of index entries. Recheck after each chapter; if it persists at Phase C, report (entry file not mine).

### g11-07 notes
- Problem result (`brenmoor.py`, invented coins 1, 2, 5, 12, 25, 40): greedy first wrong at 36 (25+5+5+1 against
  12x3), 17 failures up to 100; 100 is the only amount losing two coins. One-coin changes that make the system
  canonical (checked below c_m + c_{m-1}): 12 -> 10, 25 -> 3, 19 or 26.
- Kozen and Zaks stated as a theorem with `\admitted` (ledger g11:kozen-zaks, from the DAIMI report abstract via
  Crossref: smallest counterexample in c3 + 1 < x < cm + cm-1).
- Coins 1, 2, 5, 10, 20, 50 used as an unnamed system (no currency named, no ledger row).
- Index overfull of g11-06 gone after this chapter's entries (length-dependent, as suspected).

### g11-08 notes
- Invented data `parcels.py` (seed 2026; letter/packet/parcel, 100/130/70; split 180/60/60). Problem result:
  scaled k-NN, k = 5 chosen on validation (5.0 %, tie with 7, 8, 9, 11), test error 6.7 % (4/60) against the
  always-packet baseline 68.3 % (41/60). Test errors for k = 3, 4 are 3/60: used in the problem to teach not choosing
  on the test set.
- History box: Fix and Hodges given only as a report printed in 1989 (Crossref gives the 1989 printing, not the
  original 1951 date, so no 1951 in print); Cover and Hart January 1967 (both via Crossref).
- AI image (parcel sorting desk) deferred to Phase C.

### g11-09 notes
- Problem result (MEASURED, `measure_dateset.py`): at n = 10^5, contains is about 7,900 times faster with the set
  than with the list (0.06 against 501 us per lookup on the author's laptop); the same unittest file passes on all
  implementations. If MEASURED outputs are recaptured, update solutions pb 14-17 and 20.
- Ten ledger rows from the Python 3.12 docs (tutorial/modules, random, statistics, collections, datetime, math) and
  PEP 8 (new source PEP-8). `test_dateset.py` renamed `dateset_tests.py` (pytest collected it).
- Overlap with g11-06 (list/bisect/set lookups) is deliberate per the brief; framed as the interface lesson.

### g11-10 notes
- Project chapter: no weekend problem (calibration tool), milestones M1-M5. State kept in a dict, instructions as
  functions in an opcode table (no classes before g12-02); M4 imports M3 and extends its table (recalls g11-09).
- Agreement with the frozen `code/shared/toymachine`: same bytes, same final state, same trace text on every g11-02
  program; the shared package is imported read-only through `sys.path`.
- `parse_number`, the logic/shift functions are left unprinted for exercises 5 and 7. `\code` cannot hold `%`:
  lines with `%` use `\texttt{... \% ...}`.

### Page projection at chapter 20
- Chapters 12-21 (grade 11) take pp. 120-233: 11.4 pp per chapter against the ~12 target (5 % under), solutions
  about 2.8 pp each. Chapters 1-21 average 11.1 pp. Projection: 35 chapters x 11.5 + 3 pp of solutions each, about
  510 pp with front matter. Inside the 15 % margin; no compression. No action.

### g12-01 notes
- Problem result: 2^64 - 1 = 18,446,744,073,709,551,615 moves, about 585 billion years at one move per second
  (365.25-day years). The age of the universe was left out (it would need a ledger row); question 19 asks for the
  disks movable in 80 years instead (31).
- History box from MacTutor (published in Paris 1883, N Claus de Siam, legend of 64 discs). The docs do not state
  the default recursion limit: the text says the limit is 1000 "in this run".
- AI image (wooden Hanoi toy) deferred to Phase C.

### g12-02 notes
- Problem result: H10 = 7381/2520 exactly; the floating-point harmonic sum to n = 1000 is off by 1.8e-15 (about
  2 ulp, 2.4e-16 relative); 0 at n = 10 and 100. Numerator of H1000 has 434 digits.
- paradigms.py reads a copy of the town's loans.csv (400 loans, 87 returned late, 1371 days late in all).
- `>=open triangle 60` is not loaded; use `-{Stealth[open]}` (arrows.meta).

### g12-03 notes
- Problem result: 114 customers, longest line 5, longest wait 13 min (seed 2026, p = 0.3 per minute, service 1-5 min,
  served after closing); linked queue 228 moves (2 per customer), two-stack queue 342 (exactly 3 per customer).
- MEASURED list_vs_dict: scan of 10^5 pairs 1057 us against 0.012 us for the dictionary; caption quotes only "about
  0.01 microseconds" and "ten times with n", so a recapture will not falsify it.
- Unit tests printed through a small TestResult loop (no timing line), so the output reruns byte for byte.
- No history box (Lukasiewicz would need a ledger row); no fetch.

### g12-04 notes
- Problem result: 1023 keys, best height 9, worst 1022; 1000 random orders (seed 2026) give heights 16 to 31, mean
  21.13 (20 most frequent, 211 trees).
- `degenerate.py` stages the recursive `height` failing with RecursionError on the sorted 1023-key tree; insert and
  search loop for that reason.
- Height convention: single node 0, empty tree -1 (stated once in def:g12:trees:height).

### g12-05 notes
- Problem result: seeded maze 8 x 14 (seed 12, 12 extra walls of which 8 new): shortest exit 32 steps, hand on the
  wall 58, DFS visits 92 squares before the exit; 5 shortest exits (counted in the tests). With 30 doors (seed 5,
  6 s each): fewest steps 32 steps / 57 s (5 doors), fastest 34 steps / 54 s (4 doors).
- Town from the Station: 30 places reached, farthest Bus Depot 4640 m; one-way road 1: Town Square -> Library
  1360 m, back 2630 m.
- Ledger: g12:dijkstra-1959 (CROSSREF-DIJKSTRA, one Crossref fetch).
- TikZ: a `\foreach` variable cannot be used as an option key (`\p=2pt` fails); colour key `black` on a node also sets
  its fill: use `text=black`.

### g12-06 notes
- Problem result: two seeded random rankings of 100,000 items differ on 2,488,902,981 of 4,999,950,000 pairs
  (0.4978); measured brute/merging ratio 11 -> 70 from n = 1000 to 8000 (MEASURED: the solutions quote 0.013/0.054/
  0.209/0.856 s, 11/20/36/70, 134 s, about 700; recheck if outputs are recaptured; also the 0.19 s, the merge/insertion
  ratios 2.4 to 34.8 and the chart caption's 8 ms / 490 ms).
- Merge sort: 8 numbers 17 comparisons, 1000 random 8705; sorted input exactly n h / 2; fast power 3^1000 in 14
  multiplications = (bits - 1) + (ones - 1); arrow.pgm 16 x 16 turned by quadrants, same as the copy.
- No history box (no sourced date for merge sort); no ledger rows.
- `inversions.py` is 48 lines: printed in two ranges (1-37, 39-48) for the 40-line rule.

### g12-07 notes
- Problem result: the two library notices (53 and 49 words) share 40 words and are 15 word changes apart (7
  replacements, 6 deletions, 2 insertions); full table 2700 cells, two rows 100. Without punctuation: 13.
- fib(30): 2,692,537 naive calls, fib(2) called 514,229 times; memo 2n - 1. Change {1,3,4}: 6 = 3 + 3; Brenmoor
  36 = 12 + 12 + 12. LIBRARY/LITERARY: LIRARY. Pack of 8 objects in 15 kg: 240.
- The rebuild of `align.py` keeps, then deletes, then inserts, then replaces: with a replacement-first order the
  alignment of the notices paired unrelated words. The new notice text was trimmed ("quiet" dropped) so that the
  printed alignment reads naturally.
- Ledger: g12:bellman-1954 (CROSSREF-BELLMAN, one Crossref fetch); the history box claims only the 1954 article.
- TikZ: `grid` with a negative y unit and a shift drew lines through the cells; explicit `\foreach` lines work.

### g12-08 notes
- Problem result: on a million random letters from A, C, G, T (seed 2026, five patterns per length), naive 1.33
  comparisons per letter; Horspool 0.514 / 0.412 / 0.363 / 0.398 for m = 4 / 8 / 16 / 32, ratio 2.6 to 3.7, mean jump
  2.75 / 3.60 / 4.25 / 3.80: it levels off. On 26 letters Horspool falls like 1/m (0.057 at m = 32).
- Ex. 15's numbers (table mean 3.25, 61,343 jumps, mean 3.26) are pinned by a test (`mean_jump_measured`).
- MEASURED: measure_find.py (str.find under a millisecond; captions quote no exact factor).
- Ledger: g12:boyer-moore-1977, g12:horspool-1980 (two Crossref fetches).
- TikZ: `fill=\ifnum\j=6 ...\fi` inside a node option inside `\foreach ... [count=\j]` failed ("Missing = inserted");
  draw the special node separately.
- Coordinator mid-run note handled: `code/grade-10/lib/given_graphs.py` E501 fixed (docstrings shortened, line count
  unchanged); every `\code{}` body in grades 10-12 scanned by a brace-matching script: no backslash left; problem
  headings: every one is `\section{Problem: ...}\label{...}` on one line, then `\begin{problem}`, and a scan of the
  PDF finds no heading alone at a page foot.

### g12-09 notes
- Problem result: on 1 September 2025, 18 loans overdue (4 returned later in September), 14 members on 10 streets,
  1696 days late in all, longest 222 (loan 3, due 2025-01-22). Pinned by `test_problem_numbers`.
- SQL listings are printed through their outputs only (`sqlrun.py` echoes every statement); schema.sql and overdue.sql
  are also printed as listings. Overdue output printed in two `\omoutput[ranges]` pieces.
- Domain is recalled from g10-07 (not re-defined), per the DEFINITIONS ruling.
- `\code{...}` with an apostrophe prints a curly quote: every such body in g12-09 was rewritten as `\texttt{}` with
  `\textquotesingle{}` by a scratch script (quotefix.py). To do in Phase C: the same pass over all Book 2 chapters.
- Ledger: g12:codd-1970 (CROSSREF-CODD, one fetch). No SQL-standard row: the box does not mention it.

### g12-10 notes
- Problem result: on the five-process workload (A 20 units, then 3, 6, 2, 4) with a switch of one unit, round robin
  with q = 6 gives the smallest mean turnaround, 20.2, against 27.4 for FCFS and 32.8 for q = 1. Every number quoted
  in the solutions that the output does not print (q = 1 turnarounds, switch-free means 17.4/17.0, SJF 24.0, the
  finishing times for q = 4/5/6, q >= 20 = FCFS) is pinned by a test.
- `ps` session: `ps -o stat=,comm= -p $!` / `-p $$` after `sleep 30 &; sleep 1` is byte-stable over three captures
  (the whole-session `ps` was not: it lists the capture tool's own processes). State letters sourced from ps(1).
- No context-switch time or timer frequency printed: neither was sourced, so the text says "many times a second" and
  Q18 uses stated assumptions (4 ms, 4 us).
- Figure trap met again: `\ifnum` in a node option inside `\foreach` (interleaving figure) replaced by a colour in
  the foreach list before the first build.
- Ledger: g12:coffman-1971 (CROSSREF-COFFMAN), g12:ps-state (MAN7).

### g12-11 notes
- Problem result: on A - B - C after B - C fails, distance vectors need 15 rounds before A and B both hold 16 (7.5 min
  at RIP's 30 s per round); with split horizon B knows at round 1 and A at round 2; link state needs one message.
  The brief's "(16) vs one round" became "15 rounds vs 2 rounds (B at 1)" because that is what the simulator gives.
- failure.py shows counting with an alternative route: after D - F fails, D and E point at each other for F during
  nine rounds, +20 every two rounds, until E's figure passes 110 (its real route via G); 13 rounds for A in all.
- OSPF: RFC 2328 leaves the interface cost to the administrator; no default reference bandwidth is printed (none
  sourced in the RFC). The chapter's reference 10 000 Mbit/s is stated as its own choice.
- Model artifact found and kept out of print: in the triangle with split horizon, entries at 16 keep circulating, so
  `new == tables` never holds; the test bounds that case at 16 rounds.
- Ledger: g12:rip-2453-metric/-update/-split/-diameter, g12:ospf-2328 (RFC-EDITOR, two fetches).

### g12-12 notes
- Problem result: brute force of the discrete logarithm takes about p/2 tries (counted 10 to 24 bits, 12 seeded
  secrets each: 426 to 8.2 million steps, 0.30 p to 0.51 p), so it doubles with each bit; at an assumed 1e9 tries per
  second a 2048-bit prime needs about 5.1e599 years (test-pinned), against about 4096 multiplications for Alice.
  The brief said "counts to 40 bits": 40 bits would need about 1e12 Python steps, so the count stops at 24 bits
  (4 s) and the rest is extrapolated in Part IV.
- Every listing is deterministic: seeded `random.Random` stands in for `secrets` (said in the comments and the text,
  sourced by Book 1's g9:python-mersenne-twister row); string seeds are hash-independent.
- Deferred to Phase C: the Enigma photo `history` box (P), with its credit. No key-size `dated` box (not sourced).
- Ledger: g12:dh-1976, g12:rsa-1978 (Crossref), g12:sha-180-4, g12:aes-197 (NIST CSRC), g12:tls13-8446 (RFC).
- `\code{...\% n}` in exercise 9 caught before the build; written with `\texttt`.

### g12-13 notes
- Problem result: a toy program without IN halts or repeats a state within 2^2099 (about 7e631) steps (262 bytes +
  3 flag bits), so its halting is decidable by a repeat detector, which is not a toy program; at 1e9 steps per second
  the bound is about 2e615 years (test-pinned). Detector on 4 programs: COUNTDOWN halts (12), FOREVER loops (1),
  WRAP halts (513), SPIN loops (513, cycle 512: the all-zero-flags start never recurs).
- `try_contrarian.py` runs each contrarian under `sys.settrace` with a budget of 100 000 lines, so the looping case is
  observed, not assumed; deterministic.
- Brief changes: the toy Euclid is the chapter's listing (subtraction and a PUSH/POP swap), so the 3-star W
  exercise became toy multiplication by repeated addition; the repeat detector is the problem's listing, so the
  2-star W exercise became `first_repeat` (cycle length). Stems: euclid.py, euclid_asm.toy, euclid_sql.sql (capture
  refuses two listings with one stem).
- Ledger: g12:turing-1936 (Crossref gives the volume as 1937; printed as "volume dated 1937"), g12:church-1936,
  g12:sqlite-with-recursive.

### g12-14 notes
- No weekend problem (project chapter); five milestones, each a section with listings and outputs; no definitions
  (DEFINITIONS.md: the route planner defines nothing new).
- Dijkstra uses the scan of g12-05, not `heapq`: heaps belong to Book 3 (OUTLINE Year 1 ch. 18), and g12-05 says the
  faster structure comes in a later volume. **Phase C: g12-11 `link_state.py` imports `heapq` in a printed listing;
  replace it by the scan or say one line about it.**
- Brief changes: the 2-star W "shortest by distance" is a milestone-3 feature (the `criterion` argument), so the
  exercise became "fewest roads" (7 roads, 8420 m, 770 s vs the fastest 10 roads, 9130 m, 675 s); the 1-star P query
  became `COUNT(*), MAX(length_m)` at 30 km/h, predictable from two printed outputs.
- Measured numbers (deterministic): 870 ordered pairs, mean 303 s; slowest Old Mill -> Post Office 675 s, 10 roads;
  road 2 closed 444 s, road 6 closed 394 s (Station -> Library 276 s).
- The schema figure first underlined the keys with `\underline{\code{}}`, which printed no line; it now says
  "primary key" in the type column.

## Phase C (2026-11-20) — done

- **g12-11**: `link_state.py` now picks the minimum by a scan, as g12-05 does (heaps are Book 3's); output unchanged
  byte for byte; ranges 1-20 and 23-44.
- **Apostrophes in `\code`**: 12 occurrences in 8 files rewritten as `\texttt{...\textquotesingle{}...}`
  (scratch quotefix.py); no `\code{...\...}` left.
- **MEASURED**: no MEASURED output was recaptured, so every digit quoted in the solutions (g11-06, g11-09, g12-03,
  g12-06, g12-08) still matches its printed output.
- **Photographs (7)**, Wikimedia Commons, licence read through the file's metadata, downscaled to 900 px JPEG,
  recorded in `images/book2/CREDITS.md` and `frontmatter/image-credits-book2.tex`: ASR-33 teleprinter (g10-05),
  camera image sensor (g10-06), temperature sensor (g10-10), relay (g11-01, public domain), Manchester Baby replica
  (g11-02, the photo without visitors), network switches (g11-04), Enigma (g12-12, in a new `history` box). New ledger
  rows g12:enigma-working (Crypto Museum page) and g12:rejewski-1981 (Crossref).
- **AI images (5)**, `tools/ai_images.py` one batch, all looked at: market square with a phone (g10-06), pedestrian
  crossing with its button (g10-10), parcel sorting desk (g11-08), wooden towers of Hanoi (g12-01), cyclist with a
  paper map (g12-14). No PNG, no stub in `images/book2/ai/`.
- **Term links**: `tools/term_config/book2_en.py` curated (STOP of ~150 homographs: cost, path, set, state, route,
  class, method, header, frame, length, label, join, group, layer, interface, Library...). 3,294 links inserted;
  `--check` clean; no link inside a TikZ picture.
- **g12-10**: `ps -o stat=` printed `SN` under `nice` (the N is the niceness flag), so the outputs check failed when
  the tests run niced; the session now uses `-o state=` (one letter; ledger row g12:ps-state extended).
- Fresh forced build 0/0/0, 522 pages; gates OK for grade-10, grade-11, grade-12 and `--log 2`; `tools/test_code.sh`
  GREEN for all three years; `check_ledger` OK.

Web fetches: 148. Ledger rows: 106.

**Next action**: Phase D report sent; wait for the main session's verification.

## For the shared docs

- `tools/check_prose.py`'s curriculum pattern flags the English word *college* (``coll[eè]ge``): writers must say
  *university* or *school*.
- `.toy` listings take tool flags through the `args=` directive (`; capture: args=--trace` → `python -m toymachine run
  f.toy --trace` works); `asm`/`dis` need a `.py` listing calling `toymachine.assemble` or the module.
- A staged Python traceback captured by `tools/capture_output.py` shows five frames of the wrapper
  (`tools/echo_input.py`, `<frozen runpy>`) that a reader's own run would not show; print it with
  `\omoutput[1-3,9-15]{...}` to skip them (reported to the main session).
- `\code{...}` with `\%` prints a backslash (`\detokenize`): write `\texttt{a \% b}` instead.
- A printed unittest file must not be named `test_*.py` under `listings/` (pytest would collect it); the runner's
  `Ran N tests in 0.000s` line varies: filter it in a session and say so.
- `\code{...}` with an apostrophe prints a curly quote (T1 typewriter position 39 is quoteright); `\code{"}` is
  fine. A fix would be `\textquotesingle` via a literate-like replacement in `\code`, or upquote-like handling.
- `ps -o stat=` adds `N` when the capture or the test runs under `nice`; use `-o state=` (one character) in printed
  sessions.
- Term links: STOP is case-sensitive, so a place name that is also a term (the town's *Library*) needs its
  capitalised form in STOP too; in a book that names roads and places, *length*, *label*, *join*, *layer* and
  *interface* all need STOP.
