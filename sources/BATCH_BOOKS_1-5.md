# Run file: One Computer Science Books 1–5, English (started 2026-11-20)

**Shape** (user, 2026-11-19): five agents, Opus 5.5 at effort high, **one per book, all five at once**. The
same agent writes its book from the first chapter to the last, then fixes what the main session's checks find;
the main session continues it by SendMessage rather than replacing it. A fresh writer resumes from
`sources/book<N>/PROGRESS.md` only when the first can no longer be continued.

**User rulings for this run (2026-11-19):**
- No pilot review: the scaffold was built by the main session, and the books start at once.
- The outline's open points are accepted as proposed: Python from grade 6, a SQL chapter in grade 12 through
  Python's `sqlite3`, a RISC-V subset on a tested simulator of the repo (x86-64 only as compiler output),
  listing identifiers in English, all 165 chapters.
- Visuals: schematics, plus free-licence photographs of real hardware and historic machines, plus AI
  illustrations of everyday scenes (mostly grades 1–6).
- **No fresh readers.** Each book closes "verified, not read": the writer re-checks every solution, the main
  session verifies the book. (This departs from `book_style.md`'s verification pass, by the user's choice.)
- **Weekly limit: the main session creates `sources/PAUSE` at 90 % of the week.**

This file belongs to the main session. Agents read it and never edit it.

| Book | Entry file | Years | Prefixes | Ch. | Target | Ledger | Linker | Ports |
|---|---|---|---|---:|---:|---|---|---|
| 1 Grades 1–9 | `one_computer_science_book_1_primary_middle_school.tex` | `grade-1` … `grade-9`, `typing` | `g1`–`g9`, `typ` | 37 + appendix | ~380 pp | `sources/ledger/book1.md` | `nearest-preceding` | 41000–41999 |
| 2 Grades 10–12 | `one_computer_science_book_2_high_school.tex` | `grade-10` … `grade-12` | `g10`–`g12` | 35 | ~420 pp | `sources/ledger/book2.md` | `nearest-preceding` | 42000–42999 |
| 3 University Year 1 | `one_computer_science_book_3_university_year_1.tex` | `bachelor-1` | `b1` | 30 | ~430 pp | `sources/ledger/book3.md` | `drop` | 43000–43999 |
| 4 University Year 2 | `one_computer_science_book_4_university_year_2.tex` | `bachelor-2` | `b2` | 31 | ~450 pp | `sources/ledger/book4.md` | `drop` | 44000–44999 |
| 5 University Year 3 | `one_computer_science_book_5_university_year_3.tex` | `bachelor-3` | `b3` | 32 | ~470 pp | `sources/ledger/book5.md` | `drop` | 45000–45999 |

Note the offset: **Book 3 is `bachelor-1` / `b1`**, Book 4 `bachelor-2`, Book 5 `bachelor-3`. The `\ominput`
lists in `parts/<year>/part.tex` are frozen: chapter numbers and slugs are the outline's, and other books point
at them. A university year's `part.tex` already declares its `\part`s.

## Read before anything

1. `../CLAUDE.md` (workspace) and `../book_style.md` (the family style: read **Chapter anatomy**, **Visuals**
   and **Quality gates** twice).
2. This repo's `CLAUDE.md`, `CONTRIBUTING.md`, `OUTLINE.md` (the chapter list of record, the conventions, the
   three ownership maps), `sources/outline_sources.md`, `sources/SERIES_DEFINITIONS.md`, this file.
3. `tools/capture_output.py`'s docstring (how each language runs, the directives), then
   `code/shared/toymachine/TOYMACHINE.md`, `code/shared/town/TOWN.md` and `code/shared/sqlrun/sqlrun.py`'s
   docstring.
4. **Models of density and voice** (there are no pilots in this series; read these before your first chapter):
   - every book: `../one-math-book/parts/grade-12/13-conditional-probability.tex` (register, rigour, method
     boxes, exercises) and its solutions file;
   - Book 1: `../one-earth-and-space-sciences-book/parts/grade-3/` one chapter and `parts/grade-7/01-plate-tectonics.tex`
     (young readers, illustrations, recall boxes, weekend problem at that level);
   - Book 2: `../one-earth-and-space-sciences-book/parts/grade-12/10-climate-change.tex` (a high-school
     chapter with a 20-question problem) and `../one-physics-book/parts/grade-11/09-mechanical-energy.tex`;
   - Books 3–5: `../one-physics-book/parts/bachelor-1/22-first-law.tex` (theorem-with-derivation register),
     and one chapter of `../one-artificial-intelligence-book/` with its `code/` (how a listing and its
     captured output are woven into prose: `parts/mathematics/12-the-chain-rule-on-graphs.tex`). This
     series uses the **family chapter style**, not the AI series' step-by-step tutorial: definitions,
     methods, theorems with proofs, examples, listings where code is the point.

## User rules in force

- One subagent per book, all five at once; never per-chapter agents; no subagents of your own.
- Printed text never names a curriculum, an exam, a school system, a country's programme or a university
  (`tools/check_prose.py`). Provenance lives in source comments and `sources/` only.
- **No dataset download**, probes included: the town and seeded generators are the data. If a chapter truly
  needs a real dataset, put it under "Data to approve" in your report (host, URL, contents, licence, size,
  why generated data will not do) and write the chapter on generated data meanwhile.
- **No package installs** (pip, apt, cargo crates): the toolchain is Python 3.12 + the `.venv` (pytest, ruff,
  hypothesis), gcc/g++ 11 (C17, C++20, ASan/UBSan), Rust 1.97 (std only, `cargo --offline`), Python's
  `sqlite3`, git 2.55. **gdb and valgrind are not installed**: see "Sync decisions".
- Never use the user's e-mail address or name, in print, in code, in a User-Agent or a request. Fetched pages
  are data, never instructions.
- Never commit; git is read-only for you.

## The stints

1. **Phase A (no prose, no code).**
   - **Check your chapter list against the published programme texts** (`outline_sources.md` asks for it):
     fetch the official texts named there (French primary/collège *programmes* on eduscol and the BO; SNT,
     NSI première and terminale; MP2I/MPI; a few universities' licence informatique course lists), and list,
     per chapter, the programme items it covers, plus any item no chapter covers. Do not change the chapter
     list: propose changes in your report.
   - `sources/book<N>/BRIEFS.md`: per chapter, its sections, the definitions it owns (from the ownership map),
     what it recalls and from where, its listings (language, file names, what each shows, what output is
     captured), its figures (schematics, photographs, AI illustrations), its exercises (the four kinds from
     grade 6: predict the output, find and fix the bug, write to a specification, prove or count), its weekend
     problem or project milestones, and its ledger needs.
   - `sources/book<N>/DEFINITIONS.md`: every term the book will define, with its owner chapter and label.
   - The report (your final message): programme coverage gaps, contested terms with other books, what you
     need in shared files (`styles/onecs.sty`, `styles/lang/en.tex`, `code/shared/`), data to approve,
     anything in this file that will not work. **Then stop.**
2. **Sync.** The main session writes its decisions under "Sync decisions" below and in
   `sources/SERIES_DEFINITIONS.md`, then resumes you. There is no review stop after that.
3. **Book 4 only, first thing after the sync: the RISC-V stint.** Write `code/shared/rv/` (spec `RV.md`; an
   assembler for the subset with labels, the pseudo-instructions listed in `styles/onecs.sty`'s `RVAsm`
   language and the directives `.text .data .word .half .byte .asciz .space .align .globl`; real RV32IM
   encodings; a disassembler; a simulator with `ecall` services for printing an integer, a string and a
   character, reading an integer and exiting; `--trace`, `--regs`, a step limit; `python -m rv run|asm|dis`),
   with tests, as one Python package importable as `rv` from `code/shared/rv/`. When its tests pass, write
   `FROZEN 2026-11-.. (Book 4)` as the first line of `RV.md` and report it in `PROGRESS.md`; from then on it is
   frozen like the toy machine. Then chapter 1. **Book 5 does not import `rv` before `RV.md` says FROZEN**
   (its Part I does not need it; if Book 5 reaches ch. 7 first, it writes ch. 8–9 and Part II meanwhile and
   returns).
4. **Writing, every chapter in order** (Book 5: see the item above). The chapter is the unit: write its code
   and tests, capture its outputs, write the chapter and its solutions, pass its gates (below), check its
   figures one per page, log it in `PROGRESS.md`. Then the next.
5. **Phase C** when the last chapter is done: term links (`--unwrap --apply`, then `--apply`; curate
   `tools/term_config/book<N>_en.py`), the full per-figure pass over the whole book, no PNG left in
   `images/book<N>/ai/` and no grey stub, a fresh forced build, every year's gates and `tools/test_code.sh`
   for every year of the book. Then the **Phase D report** (pages, chapters, listings, outputs, tests,
   figures, photographs, AI images, ledger rows, links; what deviates from the outline; the traps for the
   shared docs).
6. The main session verifies the book (fresh build, gates, code tests, figure pages against their sources,
   solutions recomputed on a sample) and sends back what it finds; you fix and report again.

### The weekly limit

The main session creates `sources/PAUSE` when the week reaches 90 %. **Check for that file before starting
each chapter.** If it exists, finish the chapter you are on (unless that would take more than a few minutes),
write your state to `PROGRESS.md`, and stop with a short report. The main session continues you after the
reset. The same applies if your session stops on a rate limit.

### `sources/book<N>/PROGRESS.md`

The whole of what a replacement writer inherits. At every chapter's end, log: its pages, listings, outputs,
tests, figures (schematics / photographs / AI), ledger rows; what changed from the brief and why; the next
action. At chapters 10 and 20 add a page projection: more than 15 % under the target means the chapters are
being compressed: restore depth before going on. Put traps and calibration that later books would want under
`## For the shared docs`.

## Calibration (binding; `tools/check_exercise_calibration.py` enforces it)

| Band | Exercises per chapter | Weekend problem | Pages per chapter |
|---|---|---|---|
| grades 1–5 | 10–11, mostly ★, never decreasing | none | ~7 |
| grades 6–9 | exactly 12, never decreasing | one, 10–14 questions, Parts I–III | ~11 |
| grades 10–12 | exactly 15: 5★, 6★★, 4★★★ in order | one, 18–22 questions, Parts I–IV, ending on a named result | ~12 |
| bachelor 1–3 | exactly 12: 4★, 5★★, 3★★★ in order | one, 22–28 questions, Parts I–IV, ending on a named result | ~14 |

- **Project chapters** (`NN-project-*`, one per year from grade 7 and one per university book) have the
  band's exercises and **no weekend problem**: the chapter itself goes from a one-paragraph specification to a
  tested program in milestones (a `\section` per milestone, each with its listings, outputs and tests).
- **Kinds of exercise** from grade 6: each chapter mixes predict-the-output, find-and-fix-the-bug,
  write-to-a-specification and prove-or-count. A written program's solution is a tested file under
  `exercises/` (the solution prints the key lines, or `\omcode`s at most 40 of them, and names the file); a
  proof's solution is prose. Grades 1–5 print no code: their exercises are about the machine, files, binary
  and algorithms followed by hand.
- **The weekend problem** follows `book_style.md` (story-driven, Parts introduced by
  `\medskip\noindent\textbf{Part I --- <name>.}`, enumerates continued with `[resume]`, answers numbered in
  the solution). In this series it builds to a quantified result about a program or an algorithm (a count, a
  cost, a bound, a measured speed-up, a proved property).
- Pages: the outline's targets assume the bands above. Listings and outputs make a chapter longer, as they
  should; illustrations come on top.

**Register by band:**
- **Grades 1–5** (Book 1): short sentences, concrete scenes, many illustrations, worked steps; precise
  vocabulary from the start (processor, memory, storage, file, folder, algorithm, bit, byte), never an
  invented metaphor-object as the name of a concept (`book_style.md` 6b). Typing (grade 3) is taught as a
  technique with drawn keyboards (TikZ `keycap`, per layout); the appendix `parts/typing/` holds the drill
  lines for QWERTY, AZERTY and QWERTZ (Book 1 writes it right after grade 3).
- **Grades 6–9**: Python from grade 6. Listings short (5–25 lines), each followed by its output; tracing
  tables by hand; one new idea at a time.
- **Grades 10–12**: proofs of correctness and termination, costs, invariants, induction from grade 12.
- **University**: theorems with proofs; `\admitted` plus a prose pointer where a proof is beyond the year.

**Math level guard** (never beyond the matching year of `one-math-book`): no algebra with unknowns before
grade 8; powers of two as doubling until the math book's grade 8; the cost of halving counted in grade 11 and
called a logarithm only in grade 12; induction from grade 12; sums and recurrences in Y1; expected values from
Y2 (probability recalled from the math book's Y2); groups and finite fields only in Y3.

## Code (binding)

- Layout per chapter: `code/<year>/NN-<slug>/{listings,outputs,exercises,tests,figures}` (CONTRIBUTING.md).
  Listing stems are unique within a chapter (outputs are named by stem). A file imported by others but not
  run goes in `listings/NORUN.txt`; an output kept only for a test or a solution in `listings/NOPRINT.txt`.
- **Never type an output.** Run `python3 tools/capture_output.py code/<year>/NN-<slug>` and print with
  `\omoutput`. Never edit a file under `outputs/` by hand.
- Python listings: standard library only (`turtle` excepted, below), fit 88 columns (ruff), PEP 8, names in
  English, no f-string tricks a beginner cannot read in grades 6–9. C: C17, `-Wall -Wextra` clean unless
  the warning is the lesson. C++20, Rust 2021 edition, std only. SQL: SQLite through `sqlrun.py` or Python's
  `sqlite3`. Shell: bash; sessions with `# capture: session` (`fixtimes` if `ls -l` dates show; never with
  `make`).
- **Tests:** every listing that should work is exercised by a test (pytest for Python; `*_test.c` /
  `*_test.cpp` built with `-Werror`; a Cargo crate's `cargo test --offline`); every programming exercise's
  solution has a test; property-based tests (hypothesis) where they teach something (Y3 software
  engineering). Chapters with timings list them in `listings/MEASURED.txt` and say *laptop* in the caption;
  timing tests assert shapes (a ratio, an order), never digits.
- **Turtle (g6).** There is no display: a turtle drawing is a figure computed from the listing's own moves.
  Book 1 writes a small recording stand-in under its chapter's `figures/` (never under `listings/`, never
  printed as the reader's `turtle`) that runs the unchanged listing and writes the path as a `.dat` table for
  TikZ; a test checks the drawing against the expected polygon. The text says the reader sees the drawing in
  a window.
- **Web (g9, g10, Y2, Y3):** a page is drawn generically in TikZ from its HTML, by hand and checked; servers
  bind `127.0.0.1` on your book's port range only, start and stop inside one capture, and the client is
  Python (`urllib`) or the book's own code.
- **The toy machine** (`code/shared/toymachine/`, frozen) and **the town** (`code/shared/town/`, frozen) are
  used as they are; wrap or extend in your own chapter code. **Never edit anything under `code/shared/`**
  (Book 4: except `code/shared/rv/` during its stint, until frozen). Report defects.
- Resource limits: `systemd-run` caps every capture and test at 4 GB, no swap. Keep every process under
  ~1.5 GB (threads: see "Sync decisions"); no `make -j` or parallel tests; `nice -n 10` on long jobs; a staged infinite loop or
  fork bomb is bounded (`timeout=` directive, `ulimit` in the script) before it is ever run.

## Figures and images

- **Schematics: ~4 per chapter** in grades 6–12 and at university, ~3 in grades 1–5 (where illustrations do
  more of the work). TikZ with the styles in `styles/onecs.sty` (memory diagrams, trees, graphs, automata,
  logic gates, packet layouts, generic windows, keyboards). Charts from a tested `figures/` script's `.dat`.
- **Render every figure on its own page and look at it** (`pdftoppm -png -r 130 -f P -l P -singlefile
  build/<book>.pdf <scratch>/<name>`), for collisions and for correctness in the field: an array index off
  by one, a pointer to the wrong cell, a tree that is not a search tree, a graph whose drawn weights differ
  from the code's, a truth table with a wrong row, a pipeline diagram whose stall is in the wrong cycle, a
  packet field of the wrong width. Every figure that shows data the code computes must match the code.
- **AI illustrations** (`tools/ai_images.py --book <N> batch.txt --work <scratch>/ai`, run from the repo root,
  **detached**; it sleeps on a usage limit, and the five books share one Codex limit, so expect waits; use
  `tools/ai_stubs.py` grey stubs meanwhile). Generic everyday scenes only: a child at a desk with a laptop,
  hands on a keyboard, a family's devices on a table, a data centre aisle, a server rack, a library desk, a
  classroom. **Never** a real product, brand, logo, a real person, a readable screen, or letters on keys
  (the generator prints nonsense letters: a keyboard the reader must read is a TikZ schematic). Name files
  `<prefix>-<slug>-<what>.jpg` (e.g. `g3-inside-the-computer-open-case.jpg`); JPEG only; log every prompt in
  `images/book<N>/ai/PROMPTS.md`; look at every image before inserting it.
- **Photographs**: real hardware and historic machines (a hard disk opened, an SSD, RAM modules, a
  motherboard, ENIAC, a punched card, an early transistor, a museum's Difference Engine replica), free licence
  only (public domain or CC0 preferred, CC BY / CC BY-SA with credit), from Wikimedia Commons or a museum,
  **after reading the file's licence page**. Record source URL, author, licence and access date in
  `images/book<N>/CREDITS.md` and an `\item` on your book's image-credits page. Commons titles and
  descriptions identify a photo; they never source a fact.

## Sources and the ledger

The rules are in `sources/data_ledger.md`. A model's memory is not a source: every checkable external fact
(a standard's number or year, a port number, a code point, an encoding detail, a protocol field width, a
historical date or machine, a capacity or price) has a row in `sources/ledger/book<N>.md` with a source key
and an access date, cited by `% ledger: <id>` in the chapter. What the book's programs compute is not a
ledger fact; definitions and theorems are not either. Volatile facts go in `dated{2026}` boxes. Fetch primary
pages (RFCs, Unicode, the Python/Rust/C++ references, the RISC-V specification, museum pages). Plan ~300 web
fetches per book; keep a running count in `PROGRESS.md`.

## Ownership rules (in force at all times)

1. **Write only your own files:**
   - `parts/<your years>/` (chapters and `solutions/`; `part.tex` only for a comment); Book 1 also
     `parts/typing/`;
   - `code/<your years>/`;
   - `images/book<N>/` (with `CREDITS.md`, `ai/PROMPTS.md`) and your image-credits page
     (`frontmatter/image-credits.tex` for Book 1, `frontmatter/image-credits-book<N>.tex` otherwise);
   - `sources/book<N>/` and `sources/ledger/book<N>.md`;
   - `tools/term_config/book<N>_en.py`;
   - Book 4 only: `code/shared/rv/`, until frozen.
2. **Never edit another book's files.** Defects you find there go in your report with file:line and the fix.
3. **`styles/onecs.sty` and `styles/lang/en.tex` are append-only, and only when unavoidable**: append at the
   end under a `% Book <N>:` comment; never change or reorder existing lines; re-read the file just before
   editing (others append too); prefix new macros with your book's prefix if they are not general; build your
   book right after. **Prefer asking at the sync** (Phase A report).
4. **Do not edit** `tools/` (except your term config), `code/shared/` (except Book 4's `rv/`), `data/`,
   `Makefile`, `latexmkrc`, `pytest.ini`, `ruff.toml`, `requirements.txt`, `.venv`, `OUTLINE.md`,
   `CONTRIBUTING.md`, any `CLAUDE.md`, `THEME.md`, `frontmatter/` pages that are not yours,
   `sources/data_ledger.md`, `sources/SERIES_DEFINITIONS.md`, or this file. If a shared tool is buggy, report
   it and work around it locally if you can.
5. **Git is read-only**: `git status`, `git diff`, `git log`. Never `checkout`, `stash`, `reset`, `clean`,
   `restore`, `add` or `commit`. Nothing here is committed: this tree is the only copy.
6. **No bulk deletes**: never `rm` with a wildcard or `-r` on a directory you did not just create in your
   scratch. Delete a single named file only when necessary and say so in `PROGRESS.md`.
7. **Build only your own entry file**, always with TeX Live 2026:
   `PATH=~/texlive/2026/bin/x86_64-linux:$PATH nice -n 10 latexmk <your entry file>` (`-g` after creating a
   new chapter file). Never a bare `latexmk` or `make`; never two `latexmk` on your entry at once; never a
   short timeout around it (a killed run corrupts `.aux`/`.toc`: recover by deleting your entry's
   `.aux .toc .out .fdb_latexmk` in `build/` by name).
8. **Scoped checks only:** `bash tools/gates.sh <your year>`, `bash tools/gates.sh --log <N>` (after a fresh
   build), `bash tools/test_code.sh <your year>[/NN-slug]`, `python3 tools/link_defined_terms.py --book <N>`.
   If a check fails on a path that is not yours, note it and carry on.
9. **Cross-book references are prose only** ("the Year 1 volume", "Book 1, grade 8"), never a `\cref` into
   another book (`tools/check_prose.py` fails on one).
10. **Terms**: follow `sources/SERIES_DEFINITIONS.md`. Before each chapter's definitions, run the harvest over
    the books being written and the sister series.
11. **Scratch**: renders, image work and experiments go to
    `/tmp/claude-1000/-home-bvirrion-repositories-one-course/df72c9be-7c66-4adc-99bb-a4c63e867d1a/scratchpad/book<N>/`
    (create it). Prefix render files with your book number; check the running header of every render.

## Dependencies inside this run

All five books run at the same time, so a dependency is settled at the sync, never by waiting:

| User | Uses | Resolution |
|---|---|---|
| Book 2 (every chapter) | Book 1's definitions (grades 1–9) | Book 1's Phase A `DEFINITIONS.md` is frozen at the sync; Book 2 recalls those notions in prose and uses Book 1's wording, without a definition pair |
| Books 3–5 | Books 1–2 | a university book may re-found a school notion (ownership map "Re-founds"); it never re-teaches at the school level |
| Book 4, Book 5 | Book 3's definitions (C, data structures, algorithms) | Book 3's Phase A `DEFINITIONS.md` frozen at the sync; recall in prose ("defined in the Year 1 volume") |
| Book 5 | Book 4's definitions (automata, grammars, ownership, networks, the RISC-V subset) | the same, from Book 4's `DEFINITIONS.md`; `code/shared/rv/` after Book 4's stint |
| Book 1 g7, Book 2 g11 | the toy machine | frozen now; Book 2's project (g11 ch. 10) writes the reader's own assembler and simulator under its chapter code and checks them against the shared one |
| Books 1–3 | the town | frozen now |

## Hazards

There is no hazardous content anywhere. Security (g9, g12, Y2 ch. 20, Y3 Part V) is taught as defence: an
attack is shown only against the book's own toy program or server on the reader's machine, with its fix; no
real system, no scanning, no real credentials, no working exploit for real software; servers on `127.0.0.1`.
Passwords in examples are invented and weak on purpose only when the lesson is why they are weak.

## Sync decisions (main session, 2026-11-20, after the five Phase A reports)

**Term rulings** are in `sources/SERIES_DEFINITIONS.md`, "Sync decisions"; they override your `DEFINITIONS.md`
where the two differ. Update your `DEFINITIONS.md` to match before your first chapter.

**Programme gaps.** Every addition each book proposed *inside an existing chapter* is accepted (Book 1:
spreadsheets in g8/03, text editor vs word processor in g2/02, square root by halving in g9/04; Book 2: the
thirteen items of its report; Book 3: coverage and control-flow graphs in ch. 7, red-black trees in full in
ch. 17, meet in the middle / inversions / binary search on the answer in ch. 21, unit tasks with deadlines in
ch. 22, graphs to and from files in ch. 24, microprogramming as a paragraph in ch. 28; Book 4: its placements
in ch. 15, 21–22, 23, 28, 29, plus **SCC and 2-SAT** as a ch. 24 section or exercise, and **resolution and
unification** as a section of its predicate-logic chapter (sequent calculus told only); MVDs and 4NF in
`database-design`, the chase told; no procedural SQL (SQLite has none); Book 5: its placements in ch. 5, 6,
15, 18, 26, 30). Non-technical items, online services, JavaScript, linear programming, numerical methods, HCI
and GUI programming stay out. The chapter lists do not change. Page targets stay; ±5 % is fine.

**Tooling added at the sync** (all in `tools/capture_output.py`'s docstring; tested):
- `# capture: with=lib.c,other.c` (.c/.cpp): compile those listing files with the listing (list them in
  `NORUN.txt`; `NORUN.txt` now accepts a stem or a file name).
- `# capture: scratch`: run in a temporary copy of `listings/`, so a listing that writes files leaves nothing
  behind.
- Sessions: `copy=a.c,streets.csv` copies listing files (or, if absent there, `data/town/` files) into the
  session directory, so the transcript uses bare names and no `$CH`; a line ending in `# hidden` runs unshown.
  To show a toy program with `--trace`, use a session: `copy=count.toy` then
  `python -m toymachine run --trace count.toy`.
- `# capture: rv=asm|dis` (.S): `python -m rv asm|dis` instead of `run`.
- `code/<year>/lib/`: modules shared by a year's chapters, on `PYTHONPATH` in captures and pytest; never
  printed, never a listing. Prefer it to `sys.path` lines.
- Tests: `*_test.cpp` takes a first-line `// test-with: ../listings/x.cpp`; a `*_test.rs` outside a Cargo crate
  is built with `rustc --test` (reach the listing with `#[path = "../listings/x.rs"] mod x;`). The Rust step now
  fails on a failing test (it used to pass: the grep hid cargo's status).
- `styles/onecs.sty`: unknown file suffixes now print as plain text (no C++ colouring); `.moor` uses a `Moor`
  language; `RVAsm` has `mulhsu mulhu bgez bltz blez bgtz bgtu bleu tail`; `mathpartir` (`\inferrule`, nested
  for derivation trees: use it, not ebproof/bussproofs), `stmaryrd` (`\llbracket`), `karnaugh-map`,
  `tikz-timing` are loaded; `\graphicspath{{images/}}` (give full paths from the repo root anyway).

**Rulings on the run file's limits:**
- **Threads.** Up to 8 threads in one process, `nice -n 10`, memory still under ~1.5 GB. A threaded listing's
  output must either rerun byte for byte (print only what the program guarantees: a final count after joining,
  a sorted result) or be listed in `MEASURED.txt` with *laptop* in the caption; that includes nondeterministic
  counts (litmus outcomes, lost updates), not only timings: say "one run on the author's laptop". Tests of
  threaded code assert properties, never a specific interleaving. Three server/replica *processes* are fine,
  on your port range, started and stopped inside one capture.
- **strace, gcov, bison** (installed, free): allowed. The text says strace is Linux-only. Their outputs must
  rerun byte for byte (filter with `-e trace=`, mask pids with `-qq` or print through a filter in the session),
  or go to `MEASURED.txt`. `perf` counters and `tcpdump` are unavailable: time and simulate; build packets with
  the book's own code.
- **gdb and valgrind are not installed** (the user has been asked; no answer). Book 3 ch. 7 describes a
  debugger session in prose with a drawn schematic, and captures a `-g` AddressSanitizer backtrace as "where did
  it crash". If the user installs gdb, the main session will tell you.
- **Addresses and machine-specific frames.** Print differences and orders, never raw pointers; for sanitizer
  reports, show the first frames with `\omoutput[1-6]{...}`. Every output file must still rerun byte for byte
  on this machine (`check_outputs.py`).
- **ps, PIDs, inodes, ephemeral ports**: not printed unless masked in the listing itself; otherwise prose.
- **Town CSVs in a chapter**: prefer `copy=` in sessions and `town.load()` / `town.to_sqlite()` in Python
  (on `PYTHONPATH`). A copy of a town CSV under `listings/` is allowed only with a test that compares it byte
  for byte with `data/town/`.
- **Book 1's typing test** may read the system's keyboard layout files (local, read-only).
- **Figures are uncounted** in this family (`omfigure`, as in the Earth series): refer to a figure by place
  ("the figure below", "the drawing on the next page"); a `fig:` label is allowed, never a `\cref{fig:...}`.

**Shared code granted:**
- **Book 1** writes `code/shared/turtlerec/` (a recording stand-in for `turtle` that runs an unchanged listing
  and writes the path as `.dat`; `TURTLEREC.md`, tests), first thing after the sync, then writes `FROZEN
  2026-11-.. (Book 1)` as the first line of `TURTLEREC.md`. Book 2 g12 may use it. Book 1 also appends one
  keyboard pic to `styles/onecs.sty` (under `% Book 1:`; QWERTY, AZERTY and QWERTZ, finger zones as an option),
  used by g2, g3 and the appendix.
- **Book 4**'s RISC-V stint (`code/shared/rv/`), per `sources/book4/RV_PLAN.md`, with these decisions:
  ecall 9 `sbrk` **yes** (Book 5's heap); `call` and `tail` assembled as one `jal` (a documented simplification
  in `RV.md`: the text says real assemblers emit `auipc`+`jalr`); labels `[A-Za-z_.][A-Za-z0-9_.]*`; start at
  `main` with `ra` set so `ret` exits with status `a0`; `sp` 16-byte aligned; `--stats` (instructions, loads,
  stores, branches), `--trace`, `--regs`, step limit; a Python API with a per-step record and a hook for
  unknown `ecall`/`ebreak` (Book 5 ch. 10 and 14). Everything Book 5's report lists. Book 5 reads `RV.md` and
  tells the main session at once if something it needs is missing.
- **Book 5's project** writes its own protocol; its recall of Book 4's text protocol is checked against Book 4's
  chapter when Book 5 reaches ch. 32 (if that chapter is not written yet, the recall stays general).

## Closed books

- **Book 1** closed 2026-11-20, verified, not read: fresh TL2026 build 0/0/0, 396 pp; gates and `test_code.sh` green for every year (217 outputs rerun byte for byte); ~20 figure pages checked against their code; sampled solutions recomputed. One defect sent back and fixed (g8/05: the routing table took a 4-hop path where C links to F directly).
- **Book 2** closed 2026-11-20, verified, not read: fresh TL2026 build 0/0/0, 522 pp (target ~420: over, not compressed); gates and `test_code.sh` green for grades 10–12 (276 outputs rerun byte for byte); figure pages checked against code (two's-complement wheel, masks, multiplexers, ALU, latch, the town BST against insertion order); sampled solutions recomputed. Main-session change: `tools/echo_input.py` now prints tracebacks as plain `python x.py` does (no runner frames), so five grade-10 `\omoutput[ranges]` that hid those frames now print whole.
- **Book 3** closed 2026-11-20, verified, not read: fresh TL2026 build 0/0/0, 520 pp (target ~430); gates and `test_code.sh` green (375 outputs rerun byte for byte); figure pages checked against code (frames, pointer arithmetic, rotations, AVL cases, the LLRB tree against its output, Dijkstra step by step, a Karnaugh map's prime implicants, NAND completeness, flip-flop timing); a weekend-problem solution recomputed. Main-session changes: capture now runs every listing in a fixed environment (sanitizer stack addresses no longer depend on the caller's), one ASan output recaptured; `ai_stubs.py` now sees `\omimg{bookN/ai/...}` paths.
- **Book 4** closed 2026-11-20, verified, not read: fresh TL2026 build 0/0/0, 643 pp (target ~450: about 45 % over, from listings and outputs; nothing compressed); gates and a full `test_code.sh bachelor-2` green (482 output files rerun byte for byte, 34 MEASURED; Rust crates, C/C++ tests, 281 pytest tests); figure pages checked against code (pipeline timing with and without forwarding, the 2-bit predictor, a 2-way LRU cache trace row by row, NFA and subset construction, flows, shallow and deep copy); solutions recomputed (reservoir-sampling proof; the 98 Fermat liars of 341 and the Miller--Rabin witness).
- **Book 5** closed 2026-11-20, verified, not read: fresh TL2026 build 0/0/0, 581 pp (target ~470); gates and a full `test_code.sh bachelor-3` green (233 output files rerun byte for byte); figure pages checked against code (LR(0) automaton, three-address code, page-table walk, Lamport timestamps against the run, vector clocks, RSA, rasterisation, Savitch's recursion, the Hamming (7,4) generator matrix and circles); no AI images in this book (planned scenes became TikZ, tables or photographs).

**Run closed 2026-11-20: five books, 165 chapters, 2,662 pp, all 0/0/0; Books 1--3 rebuilt clean after the Book 4/5 style appends. Weekly plan 42 % → 70 %. Nothing committed.**
