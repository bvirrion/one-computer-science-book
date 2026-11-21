# Book 1 --- progress log

Writer: Book 1 agent (Opus 5.5). Run file: `sources/BATCH_BOOKS_1-5.md`. Briefs: `sources/book1/BRIEFS.md`;
terms: `sources/book1/DEFINITIONS.md` (aligned with the sync rulings 2026-11-20).

## State

- Phase A: done 2026-11-20 (BRIEFS, DEFINITIONS, report).
- Sync applied 2026-11-20: DEFINITIONS.md updated (port removed; authentication kept; never-defined list).
- `code/shared/turtlerec/` written and FROZEN 2026-11-20 (17 tests; `TURTLEREC.md`). Not on the
  PYTHONPATH of `tools/test_code.sh` or `capture_output.py`: tests add it through `tests/conftest.py`.
- Keyboard appended to `styles/onecs.sty` under `% Book 1:` (`\omkeyboard[...]{us|fr|de}`,
  `\omkeyboardkeys`, nodes `kb-<xkb name>`, options unit/fingers/home/highlight/nolegend; legends generated
  from `/usr/share/X11/xkb/symbols/{us,fr,de}`, generator kept in scratch `book1/kbd/gen.py`). Book built
  0/0/0 afterwards.
- AI batch 1 (all 19 illustrations of the book) launched detached 2026-11-20; log in scratch
  `book1/ai/run1.log`.
- Web fetches so far: ~25.

## Chapters

| Chapter | Pages | Listings | Outputs | Tests | Schematics / photos / AI | Ledger rows | Notes |
|---|---|---|---|---|---|---|---|
| g1/01 what-is-a-computer | 6 (5 + ~1 sol.) | 0 | 0 | 0 | 3 / 1 (ENIAC) / 2 | 4 | 11 exercises 8★ 3★★ |
| g1/02 instructions-in-order | 5 (4.5 + ~1 sol.) | 0 | 0 | 0 | 5 / 0 / 1 | 0 | 10 exercises 7★ 3★★; robot paths checked with scratch `robot.py` |
| g2/01 keyboard-and-mouse | 5 | 0 | 0 | 0 | 3 / 0 / 2 | 2 | 11 exercises 8★ 3★★ |
| g2/02 using-a-computer | 5.5 | 0 | 0 | 0 | 4 / 0 / 1 | 0 | text editor vs word processor (sync gap) included |
| g3/01 typing-with-ten-fingers | 6.5 | 0 | 0 | 0 | 4 / 1 (Sholes & Glidden) / 1 | 6 | keyboards from `\omkeyboard` |
| g3/02 inside-the-computer | 5.5 | 0 | 0 | 0 | 3 / 1 (motherboard, CC0) / 1 | 0 | 10 exercises 7★ 3★★; no port standard named, so no ledger rows; no `dated` laptop box (would need a maker's page; skipped) |
| g3/03 files-and-folders | 5.5 | 0 | 0 | 0 | 4 / 0 / 1 | 0 | 11 exercises 8★ 3★★; no format named behind extensions, so no IANA rows |
| typ/01 typing-drills (appendix) | 7.5 | 0 | 0 | 0 | 3 keyboards / 0 / 0 | (typ:layout-*) | 99 drill lines + 9 passages; `code/typing/01-typing-drills/tests` checks every line against xkb us/fr/de and every count, and the keyboard letter legends in onecs.sty (4 tests) |
| g4/01 memory-and-storage | 5.5 | 0 | 0 | 0 | 4 / 2 (opened HDD, IBM 350) / 1 | 6 | no `dated` capacities box (no maker page fetched); remark on 1024 with NIST source |
| g4/02 programs-and-operating-system | 4.5 | 0 | 0 | 0 | 3 / 0 / 1 | 7 | hook child renamed Tom→Lina to match the AI image; dated box names 7 OS families from the makers' pages |
| g4/03 algorithms-repeat-and-decide | 5 | 0 | 0 | 0 | 6 / 0 / 1 | 0 | 11 exercises 8★ 3★★; every robot path checked with a scratch simulator; Tom-vs-Lina comparison counts (15, 1225) computed |
| g5/01 bits-and-bytes | 4.5 | 0 | 0 | 0 | 5 / 0 / 1 | 0 | 11 exercises 8★ 3★★; all binary values checked in Python |
| g5/02 text-pictures-sound-as-numbers | 5.5 | 0 | 0 | 0 | 6 / 0 / 1 | 2 (RFC 20) | no sub-pixel photo (Commons rate-limited the search; drawn sub-pixels instead) |
| g5/03 networks-first-look | 6 | 0 | 0 | 0 | 4 / 1 (first web server, CC BY-SA) / 2 | 5 | address uses example.com (RFC 2606); password advice from the NCSC page |
| g6/01 first-python-program | 7.5 + 1.5 sol. | 0 | 0 | 0 | 2 / 0 / 1 | 3 | 12 exercises 4/5/3; problem 11 q.; 13 listings + 7 exercise files, 5 tests green, 11 outputs |
| g6/02 variables-and-input | 7 + 2 sol. | 0 | 0 | 0 | 4 / 0 / 0 | 0 | 12 exercises 4/5/3; problem 11 q.; 13 listings + 11 exercise files, 5 tests, 13 outputs |
| g6/03 for-loops-turtle | 9 + 3 sol. | 0 | 0 | 0 | 8 / 1 / 0 | 3 | 12 exercises 4/5/3; problem 12 q.; turtle drawings recorded by turtlerec (figures/record_turtle.py, 30 .dat); 9 tests; photo Valiant floor turtle (CC BY-SA 3.0) |
| g6/04 if-else | 8 + 2.5 sol. | 0 | 0 | 0 | 5 / 0 / 0 | 0 | 12 exercises 4/5/3; problem 12 q.; 11 listings + 13 exercise files, 5 tests, 10 outputs; ledger USNO leap years |
| g6/05 while-loops | 8 + 2 sol. | 0 | 0 | 0 | 4 / 0 / 0 | 0 | 12 exercises 4/5/3; problem 12 q.; 12 listings + 15 exercise files, 4 tests, 12 outputs; ledger Lagarias 3x+1 overview (arXiv) |
| g7/01 functions | 8 + 2.5 sol. | 0 | 0 | 0 | 5 / 0 / 0 | 0 | 12 exercises 4/5/3; problem 13 q. (EAN-13); 12 listings + 11 exercise files, 5 tests, 11 outputs; ledger WP-EAN (GS1 pages 403) |
| g7/02 lists | 8 + 2 sol. | 0 | 0 | 0 | 5 / 1 / 0 | 0 | 12 exercises 4/5/3; problem 12 q.; town data via figures/town_tables.py (rain.py, hilltop_2025.py, january.dat; test checks against data/town/weather.csv, exercises/rain.py byte-equal copy); result 11 days, 10-20 August |
| g7/03 strings | 8 + 2.5 sol. | 0 | 0 | 0 | 5 / 1 / 0 | 0 | 12 exercises 4/5/3; problem 12 q. (29 palindrome dates); letter-count figure from figures/letter_counts.py; listings ASCII + é only (listings literate) |
| g7/04 how-a-processor-runs-a-program | 7 + 2 sol. | 0 | 0 | 0 | 4 schematics + 2 photos (CC0 486 in socket, CC BY 4.0 ENIAC function table) | 3 rows (g7:edvac-1945, g7:clock-2026, g7:cores-2026; reuses g1:eniac-programming) | 12 exercises 4/5/3; problem 12 q.; multiply 3b+6 steps (3x50: 156, 50x3: 15; 7x200 prints 120); sum 3n+5; trace shows state BEFORE each step; tests run every .toy with Machine. Outputs of .toy only from listings/ (capture ignores exercises/), so printed exercise programs live in listings/ |
| g7/05 finding-and-fixing-bugs | 9.5 + 2 sol. | 0 | 0 | 0 | 4 schematics + 1 photo (1947 log book, PD US Navy) | 1 row (g7:bug-1947, CHM) | 12 exercises 4/5/3; problem 11 q. (grader 28 lines, 4 bugs; check_grader 66 -> 1 -> 0); staged errors via sessions (missing_colon.txt + hidden mv; grader.txt shown with omcode as .txt) |
| g7/06 project-quiz-game | 7 + 1.5 sol. | 0 | 0 | 0 | 4 schematics | 0 | project: no problem; 12 exercises 4/5/3; quiz_v1..v5 + questions.py (NORUN) + quiz_v3_poor / quiz_v5_worst (NOPRINT) with .stdin; tests monkeypatch input; worst game 32 lines |
| g8/01 binary-and-hexadecimal | 7.5 + 2 sol. | 0 | 0 | 0 | 5 schematics (incl. colour swatches defined from the listing's codes; a test greps the chapter for them) | 1 row (g8:css-hex-colour, W3C-CSS) | 12 exercises 4/5/3; problem 12 q. (2^64 - 1, sixteen F); proposition patterns of n bits with proof; grain weight given as a hypothesis (25 mg), not a fact |
| g8/02 dictionaries | 8 + 2 sol. | 0 | 0 | 0 | 5 schematics | 1 row (g8:python-dict-order) | 12 exercises 4/5/3; problem 12 q. (240/40, 8000/400); library records invented (no real books, no ledger); two return values told in the problem's preamble |
| g8/03 files-and-data-tables | 8.5 + 2 sol. | 0 | 0 | 0 | 5 schematics + 1 pgfplots chart (Hilltop monthly means from figures/out) | 3 rows (g8:csv-rfc4180, g8:python-open-encoding; RFC-EDITOR-4180 source) | 12 exercises 4/5/3; problem 13 q. (wettest month March 84.4 mm; Riverside codes pull mean 12.04 -> 11.43); spreadsheet section (accepted gap) with generic grid; town CSV copies (books, loans, weather) by figures/town_tables.py + tests/test_town_copy.py byte test; write_notes/report use `# capture: scratch`. Brief said weather defects at Hilltop: the -99.0 codes are at Riverside, so Part III is Riverside's and no Hilltop day exceeds 25 C (days above 20: 17) |
| g8/04 searching-and-sorting | 8 + 2 sol. | 0 | 0 | 0 | 4 schematics (linear scan, 16-cell halving brackets, selection and insertion passes on 6 cards) + 1 pgfplots chart (figures/comparisons.py from the listings' own functions, curves labelled directly) | none | 12 exercises 4/5/3; problem 12 q. (worst guesses 4/7/10/14/17/20 for 10..10^6; 1,000 linear searches 500,500 vs selection 499,500 / insertion 252,747 + 8,987 binary); mixed order fixed as 37i mod n; binary_bug loop tested by a 2 s timeout |
| g8/05 how-the-internet-works | 8 + 2 sol. | 0 | 0 | 0 | 4 schematics (packets, two LANs + routers, bytefield address, client/DNS/server timeline) + 1 photo (opened fibre cable, Asurnipal CC BY-SA 4.0) + AI data-centre image | 9 rows (ipv4, ipv6, dns, packet-1500, headers-40, fibre-index 1.468 Corning PI1424, arpanet-1969, broadband-2026 Ofcom CN2025, datacentres-energy IEA) + 9 sources | 12 exercises 4/5/3; problem 12 q. (2,055 packets, 82,200 header bytes; 0.098 s propagation vs 2.466 / 0.247 s sending); example names .example and RFC 5737 documentation addresses only; no listing touches a network. Ledger ids use one colon (g8:ipv4-32bits ...) |
| g8/06 project-data-explorer | 8 + 1.5 sol. | 0 | 0 | 0 | 4 (data flow, menu loop, loan-to-book look-up, pgfplots genre bars from figures/out/genres.dat via loans_by_genre) | none | project: 5 versions, partial listings by line range; 12 exercises 4/5/3; books.csv + loans.csv copied by figures/town_tables.py, byte test; `assert` and triple-quoted strings explained in passing; sort key returns a list [-loans, title] (no tuple, no lambda); data facts: no book and no member never borrowed (answers say so); 35 out on 2025-06-30, 24 on 2025-12-31 (22 never back + 2 back in 2026); busiest month 09 (45); mean loan 17.6 days; best pair 5+47 (3 members) |
| g9/01 html-and-css | 8.5 + 1.5 sol. | 0 | 0 | 0 | 4 (browser window drawn from the HTML, forest tree = show_tree output, box model to scale from style.css, two style sheets side by side) | 3 rows (g9:html-void WHATWG, g9:css-box W3C, g9:web-first-page CERN) + 2 sources | 12 exercises 4/5/3; problem 11 q. (list page n + 6 elements, depth 4). Deviation from the brief: the tree is found by our own tag scanner (`html_tree.py`: find, depth counter, void list) instead of `html.parser`, which needs a subclass (classes are Book 2's); the brackets exercise follows naturally. History box recalls g5/03's first server instead of repeating its photo. Element table uses \hline (booktabs not loaded) |
| g9/02 logic-gates | 8 + 1.5 sol. | 0 | 0 | 0 | 4 circuitikz (four gates with tables, (a AND b) OR (NOT c), half adder, series/parallel switches with lamp) + 1 photo (1947 transistor replica, PD, plaque cropped) | 3 rows (g9:boole-1854 Open Library, g9:shannon-1937 (renamed from g9:shannon-1940 on 2026-11-21, R1-053), g9:transistor-1947 CHM) + 3 sources | 12 exercises 4/5/3; problem 12 q. (pairs = 5 gates, majority = 4 gates, both checked on 8 inputs; 32 rows for five judges); De Morgan proposition proved by the 4-row program; test builds all 16 two-input tables from NAND. No university named in print (Shannon's thesis told without the institution); no transistor-count claim (unsourced) |
| g9/03 grids-and-images | 8.5 + 1.5 sol. | 0 | 0 | 0 | 4 schematics (indexed grid, 4/8/corner neighbourhoods, 3x3 blur window) + a 5-image pgfplots matrix panel drawn from the captured PGM outputs (figures/draw_images.py) | 1 row (g9:pgm-format, Netpbm) + 1 source | 12 exercises 4/5/3; problem 12 q. shape.pgm (16 x 12, lines <= 70 chars) written by figures/make_shape.py, regeneration tested; transformations print PGM text (NOPRINT), no listing writes a file. Brief said whole-level light 'dies out': the captured run shows it stops at 69 cells after 5 blurs and freezes from blur 16 (centre 3); decimal blurs give (2k+1)^2 for k <= 6. Image is 16 x 12, not 24 x 16, so a PGM line fits 64 characters |
| g9/04 algorithms-on-numbers | 9 + 1.5 sol. | 0 | 0 | 0 | 4 (divisor-pair rectangles of 36; sieve grid 1-100 coloured from sieve() via figures/out/primes.tex; Euclid squares 21 x 13; pgfplots of the most Euclid steps per a <= 200 from figures/number_figures.py) | 2 rows (g9:eratosthenes MacTutor, g9:largest-prime-2026 GIMPS) + 2 sources | 12 exercises 4/5/3; problem 12 q.: record pairs (987, 610) 14 steps (captured); primes_timing in MEASURED.txt, caption 'laptop'. Deviations: perfect numbers below 1,000 (not 10,000) to keep the star-1 loop simple; the d*d<n bug's smallest victim is 4, not 49 (brief); the gcd_steps scratch listing became a figure script. Fixed on the way: \code{\%} printed a backslash (detokenize) in g7/05, g7/06, g8/01 solutions and \code{"\n"} printed '\n ' in g8/03: all now \texttt |
| g9/05 randomness-and-simulation | 8 + 2 sol. | 0 | 0 | 0 | 4 (tiny generator's 16-cycle on a circle; frequency of a six vs throws, log x, from frequencies.txt; random walk path; 1,000 points in the quarter disc) + AI dice image, printed cropped (trim right 492 px: the right-hand die showed 5 and 2 together, impossible on a real die) | 1 row (g9:python-mersenne-twister, PYTHON-DOCS) | 12 exercises 4/5/3; problem 12 q. birthday: simulation 0.517 vs exact 0.5073 at 23 (brief's 'agree to two decimals' is false: they agree within 0.01 for every size; printed so). Every listing seeds; exercise outputs (not captured) are pinned by tests. Hook's 4 sixes in 60 (2 % for a fair die) told as 'unusual, but happens', no unsourced figure |
| g9/06 first-cryptography | 9.5 + 2 sol. | 0 | 0 | 0 | 4 (message flow; cipher wheel shift 3; two bar charts of letter counts, plain and shift-3, from figures/letter_counts.py; keyword row lamp) + photo (Swiss Army training cipher wheel, Rama, CC BY-SA 2.0 FR) | 3 rows (g9:caesar-shift Suetonius/Loeb on LacusCurtius; g9:al-kindi and g9:polyalphabetic from Ycart, arXiv:1211.6847) + 2 sources | 12 exercises 4/5/3; problem 12 q.: key found 23/33/46/56/57/100/100 times in 100 for 10..1000 letters (lengths 500 and 1000 added: up to 200 the guess plateaus because t is close behind e). Passage invented (1,517 letters, listings/passage.txt, NORUN). Substitution guess uses paragraphs 1-2 as the known text against 3-4 (al-Kindi's method), 401 -> 514 of 810 letters after two typed swaps. Deviations: no Bellaso 1553 row (no library page found; history box names Alberti, Bellaso, Vigenere without dates); photo is a 20th-century training wheel, not a 15th-16th c. disk (no free photo found quickly); no RFC row (no protocol name printed). Fixed: \code{\{} printed backslashes |
| g9/07 project-grid-game | 8 + 2 sol. | 0 | 0 | 0 | 5 (level 1 grid drawn from its rows; versions timeline; state diagram; one-turn flowchart; tree of 4 and 16 sequences) | none | 12 exercises 4/5/3, no problem (project). maze_v1..v5 + lost_game (stdin win 16 moves / loss), try_all_moves (base-4 enumeration; tiny.txt: first win at 6 moves, 1 of 4,096; level2.txt: 0 of 21,844). No try/except (not taught): check_level returns a message string. Deviations: brief's 'cellular automaton game mode' exercise replaced by a fog mode (the automaton was g9/03 exercise 12; a second game mode would not fit a page); level files are .txt in NORUN. |

## Phase C to-do (found while writing)

- **Short listings and outputs split across pages** (several per chapter from g6 on: a 3-line output with its
  last line and caption on the next page). Plan: append `\RequirePackage{needspace}` under `% Book 1:` in
  onecs.sty and insert `\Needspace*{N\baselineskip}` before short `\omcode`/`\omoutput` in Book 1 chapters
  by script (N from the line count), then rebuild and check. Chapter pages depend only on what precedes
  them, so this can run once, at the end.

## Changes from the briefs

- g6/05: the `for` versus `while` figure is a listing (`for_and_while.py`, captured) rather than a drawing of
  hand-typed code; the staged infinite loop is the silent `coins != 50` loop (a printing one fills the capture
  with millions of lines). Exercise 8 is the digit sum (counting digits is the chapter's own listing).

- g6/03: unused loop variables are named `_` (ruff B007 flags `for i in range(4)` when `i` is unused); the
  for-loop section therefore defines the loop variable together with the loop (count.py first), and
  `row_of_squares.py` uses its outer variable (growing squares). `types.py` of g6/02 became `kinds.py`
  (a listing named like a standard module breaks the capture wrapper).

- Page projection at chapter 10 (2026-11-20): grades 1–5 run 4.5–6.5 pp per chapter (about 5.4 average,
  against ~7 planned), so grades 1–5 come to about 76 pp instead of ~98. The content of each brief is all
  there; the shortfall is in density, not in coverage. Grades 6–9 (code chapters, 12 exercises + weekend
  problem) are expected at ~10–11 pp each; projected book about 330–350 pp against ~380.

- Page projection at chapter 20 (rechecked after chapter 24, 2026-11-20): grade 6 runs 40 pp for 5 chapters
  (8.0 body + ~2 solutions = ~10 with solutions), grade 7 runs 51 pp for 6 chapters (8.5 + ~2 = ~10.5),
  against ~11 planned: 5–9 % under, inside the 15 % margin; no compression. Book projected at ~350 pp
  (grades 1–5 ~76 + 21 code chapters x ~10.3 + appendix ~12 + front/index ~15) against ~380, the shortfall
  being the grades 1–5 band noted at chapter 10.

- g1 chapters run ~5–6 pp instead of ~7 (short sentences, few words per page); grade 1–5 band to be watched
  at the chapter-10 projection.
- g3/01: brief's figure (d) said ``left little finger on right Shift for a capital J'': wrong; the figure shows
  left Shift + J and right Shift + A. No typewriter-patent row: the history box cites Lemelson-MIT (sale 1874,
  QWERTY from Sholes) and the photograph's visible keyboard.

## For the shared docs
- `\code{\{...\}}` prints the backslashes (`\code` is `\texttt{\detokenize{#1}}`); balanced braces need no escape: `\code{{"a": 1}}`.
- `\code{\#...}` prints the backslash, like `\code{\%}`: use `\texttt{\#...}` (fixed by script in Book 1).

- **check_ledger currently fails for every book** because of `sources/ledger/book5.md:30-34` (source keys
  `crossref 10.xxxx/...` not in a Sources table). Book 1's own rows are clean.

- **`\omoutput[ranges]` leaves blank lines at the bottom of its frame** when the last range ends before the
  end of the file (listings `linerange` keeps reading to EOF; a standalone test shows it, and a book page showed
  about six blank lines). Fix in onecs.sty: also pass `lastline=<end of the last range>`. Book 1 works around it
  by ending every range list at the file's last line. Book 2's `parts/grade-10/01-specifications-and-tests.tex:126,168`
  and `bachelor-2/03-cpp-polymorphism.tex:128` may show it.
- **capture_output.py records a crash silently** when a listing exits non-zero without `# capture: exit` (a
  listing named `types.py` shadowed the standard module and every capture of the folder became a traceback,
  rc 0). Proposal: fail on a non-zero exit unless `exit` is declared. Also: a listing named like a standard
  module (`types.py`, `random.py`, `turtle.py`) breaks the wrapper's own imports; a gate could forbid them.

- **tools/echo_input.py** (shared tool, not edited): every `.py` listing runs through `runpy`, so a captured
  traceback shows three wrapper frames (`File "tools/echo_input.py", line 36` and two `<frozen runpy>`) that a
  reader never sees. Book 1 works around it: staged runtime errors are captured through a `# capture: session
  copy=<file> exit` listing that runs `python <file>`, and the erroring file is in `NORUN.txt`. Fix proposal:
  have echo_input strip its own frames (e.g. run the code with `exec(compile(...))` inside a try that prints
  `traceback.print_exception` from the listing's frame on), or let capture_output run plain `python` when there
  is no `.stdin`.
- **ruff on staged syntax errors**: a listing that is meant to fail with a `SyntaxError` cannot be a `.py`
  file (ruff reports `invalid-syntax`, which no `noqa` silences, and `ruff.toml` is shared). Book 1 keeps such a
  file as `listings/<name>.txt` and shows it through a session (`copy=quote.txt`, a `# hidden` `mv` to
  `quote.py`, `cat quote.py`, `python quote.py`). A `ruff.toml` `extend-exclude` for a `staged/` folder would
  be cleaner.
- **`\code{...\%...}` prints the backslash** (`\code` detokenizes): `\code{17 \% 3}` shows `17 \% 3`. Book 1
  uses `\texttt{17 \% 3}` for `%`, `#`, `$` and `^`. Book 2 has one: `parts/grade-10/02-tuples-sets-comprehensions.tex:344`
  (`\code{{n \% 3 for n in range(10)}}`).
- **A `\label` between `\section{Problem: ...}` and `\begin{problem}`** defeats the page-break look-ahead in
  onecs.sty (it peeks only past blank lines): the heading can be stranded at the foot of a page. Book 1 puts no
  label on the problem's section. Book 2 does (`sec:g10:...:problem`).

- `styles/onecs.sty` gained `\omdrill` and `\ompassage` (typing appendix) after the keyboard block. The
  keyboard block's header comment says `typ:layout:us`; the ledger ids are `typ:layout-us` (one colon).
- `code/typing/` holds the appendix test (`01-typing-drills/tests`); `tools/test_code.sh typing` runs it.

- Ledger ids take exactly one colon (`tools/check_ledger.py`: `^[a-z][A-Za-z0-9]*:[A-Za-z0-9][A-Za-z0-9_.+\-]*$`):
  the briefs' `g7:eniac:programming` style becomes `g7:eniac-programming`.

## Phase C (2026-11-20)

- Term links: `tools/term_config/book1_en.py` curated (STOP 15 words incl. clock; DROP move, copy;
  EXTRA_PROTECT for the typing appendix's \omdrill / \ompassage arguments, "index finger", "desktop
  computer", the verbs "links" and "carry", and a broken network "link"). Unwrap + apply: 232 linkable
  terms, 3,848 links in 75 files; `--check` clean. The first apply had linked inside \ompassage (the typing
  test went RED) and linked "index fingers" to the list index; both fixed by the protections.
- Needspace: `\RequirePackage{needspace}` appended under `% Book 1:` in onecs.sty; 256
  `\Needspace*{(n+3)\baselineskip}` inserted by script before top-level \omcode / \omoutput of at most
  10 lines (none inside boxes). +1 page, no underfull boxes (`\raggedbottom`).
- Full per-figure pass over all 396 pages in 30-page tiles: no clipped, overlapping or broken figure.
- No PNG in `images/book1/ai/` (19 JPEG + PROMPTS.md), no grey stub.
- Fresh forced build (`latexmk -g`): 0 errors, 0 undefined, 0 overfull, 396 pp.
- Gates grade-1..9 and typing: OK. `test_code.sh` grade-6..9 and typing: GREEN (grades 1–5 have no code);
  turtlerec 17 tests green; ruff clean on all Book 1 code.

- Verification fix (coordinator, 2026-11-20): g8/05 toy routing table had C -> E although C links to F
  (contradicting "one step closer"); now C -> F, path A, B, C, F in 3 steps (listing, output, test, figure,
  caption). Exercise 3 (from D: D -> E -> F, 2 steps) unchanged. Rebuilt 0/0/0, 396 pp; grade-8 gates OK,
  test_code GREEN.

## Next action

Book 1 closed: Phase D report sent.
