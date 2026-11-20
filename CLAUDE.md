# CLAUDE.md — one-computer-science-book

Five LaTeX books (grades 1–9, grades 10–12, University Years 1–3), 165 chapters, English first. Outline of
record: `OUTLINE.md` (approved 2026-11-19). Conventions: `CONTRIBUTING.md`; family style: `../book_style.md`.

- **State (2026-11-20):** all five English books written and closed, 165 chapters, 2,662 pp (396 / 522 /
  520 / 643 / 581), each 0/0/0 with gates and code tests green; uncommitted.
- **Run of record:** `sources/BATCH_BOOKS_1-5.md` (one Opus 5.5 agent per book, all five at once,
  2026-11-20; "Sync decisions" and "Closed books" at its end). Traps found while writing are under
  "For the shared docs" in each `sources/book<N>/PROGRESS.md`. Per-book state: `sources/book<N>/PROGRESS.md`. Term ownership: `sources/SERIES_DEFINITIONS.md`.
- **Closing standard for this run: "verified, not read"** (user, 2026-11-19): the main session verifies each
  book (fresh build 0/0/0, gates, code tests, figure pages, sampled solutions); no fresh-reader agents.
- **Build** with TeX Live 2026 only: `PATH=~/texlive/2026/bin/x86_64-linux:$PATH latexmk <entry>.tex`.
- **Code:** every printed listing is a file under `code/<year>/NN-slug/listings/`, every printed output is
  written by `tools/capture_output.py` and reruns byte for byte; `tools/test_code.sh <year>` runs ruff, pytest,
  C/C++/Rust tests, listing ranges and the outputs. `code/shared/` (toy machine, town, sqlrun, rv) is frozen.
- **Gates:** `tools/gates.sh <year>` (prose, structure, calibration, ledger, code references) and
  `tools/gates.sh --log <N>`.
- **Weekly limit:** `sources/PAUSE` stops the writers (created at 90 % of the week).
- No commits; no dataset download without the user's approval; nothing personal in print (capture prints the
  account as `ada`, the machine as `laptop`); no curriculum or university names in printed text.
