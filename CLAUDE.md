# CLAUDE.md — one-computer-science-book

Five LaTeX books (grades 1–9, grades 10–12, University Years 1–3), 165 chapters, English first. Outline of
record: `OUTLINE.md` (approved 2026-11-19). Conventions: `CONTRIBUTING.md`; family style: `../book_style.md`.

- **State (2026-11-21):** all five English books written (2026-11-20, committed as PP-167) and then read by fresh
  readers and closed **"verified and read"** (2026-11-21): 165 chapters, 2,673 pp (398 / 523 / 523 / 646 / 583),
  each 0/0/0 with gates, code tests (C/C++ under ASan+UBSan) and term links green. The reading-run fixes are
  uncommitted.
- **Run of record:** `sources/BATCH_BOOKS_1-5.md` (one Opus 5.5 agent per book, all five at once,
  2026-11-20; "Sync decisions" and "Closed books" at its end). Traps found while writing are under
  "For the shared docs" in each `sources/book<N>/PROGRESS.md`. Per-book state: `sources/book<N>/PROGRESS.md`. Term ownership: `sources/SERIES_DEFINITIONS.md`.
- The writing run closed "verified, not read" (user, 2026-11-19); the reading run above then brought every book to
  "verified and read".
- **Fresh-reader run (2026-11-21, closed):** `sources/READ_BOOKS_1-5.md`. One Opus reader per book, all five at once,
  reported, then fixed the defects the main session confirmed: 346 found (12 major), 344 fixed, 1 rejected, 2 more found while fixing.
  Reports and Resolution tables: `sources/book<N>/READER_REPORT.md`.
- **Build** with TeX Live 2026 only: `PATH=~/texlive/2026/bin/x86_64-linux:$PATH latexmk <entry>.tex`.
- **Code:** every printed listing is a file under `code/<year>/NN-slug/listings/`, every printed output is
  written by `tools/capture_output.py` and reruns byte for byte; `tools/test_code.sh <year>` runs ruff, pytest,
  C/C++ tests under ASan+UBSan, Rust tests, listing ranges and the outputs. A `# capture:` directive may sit in a
  file's first or last five lines (put it last when the printed program must start at line 1). `code/shared/` (toy machine, town, sqlrun, rv) is frozen.
- **Gates:** `tools/gates.sh <year>` (prose, structure, calibration, ledger, code references) and
  `tools/gates.sh --log <N>`.
- **Weekly limit:** `sources/PAUSE` stops the writers (created at 90 % of the week by default; a run may set another threshold).
- No commits; no dataset download without the user's approval; nothing personal in print (capture prints the
  account as `ada`, the machine as `laptop`); no curriculum or university names in printed text.
