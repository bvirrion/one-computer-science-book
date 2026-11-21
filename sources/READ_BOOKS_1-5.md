# Run file: fresh readers for One Computer Science Books 1–5 (started 2026-11-21)

The five English books closed 2026-11-20 "verified, not read" (`sources/BATCH_BOOKS_1-5.md`). This run gives each
book the fresh-reader pass of `../book_style.md` "Verification first pass", as the economics run did.

**User rulings (2026-11-21):**
- One Opus 5.5 reader at effort high per book, all five at once. A reader works alone: no forks, no subagents.
- The same agent reads, then fixes. It first reports and edits nothing. The main session triages the report
  (three ways; it rejects the reader's own errors) and sends the confirmed list back to the same agent by
  SendMessage. The agent fixes, and then the main session re-verifies. The writers of 2026-11-20 cannot be
  continued.
- **Weekly limit: `tools/usage_watch.sh` creates `sources/PAUSE` at 40 % of the week.** A reader checks for it
  before each chapter, and if it is there it writes its report so far and stops.
- No commits, no dataset downloads, no package installs.

This file belongs to the main session.

| Book | Years | Ch. | Pages | PDF | Report |
|---|---|---:|---:|---|---|
| 1 | `grade-1` … `grade-9`, `typing` | 37 + appendix | 396 | `build/one_computer_science_book_1_primary_middle_school.pdf` | `sources/book1/READER_REPORT.md` |
| 2 | `grade-10` … `grade-12` | 35 | 522 | `build/one_computer_science_book_2_high_school.pdf` | `sources/book2/READER_REPORT.md` |
| 3 | `bachelor-1` | 30 | 520 | `build/one_computer_science_book_3_university_year_1.pdf` | `sources/book3/READER_REPORT.md` |
| 4 | `bachelor-2` | 31 | 643 | `build/one_computer_science_book_4_university_year_2.pdf` | `sources/book4/READER_REPORT.md` |
| 5 | `bachelor-3` | 32 | 581 | `build/one_computer_science_book_5_university_year_3.pdf` | `sources/book5/READER_REPORT.md` |

The PDFs were checked on 2026-11-21: they were built after every source file of their book.

## Closing (per book)

A book closes "verified and read" once:
- every chapter and solution file is logged as read;
- every defect is fixed or rejected, with a reason;
- after the last fix, the build is 0/0/0 under TL2026, and these all pass: `tools/gates.sh <year>` for each
  year, `tools/gates.sh --log <N>`, `tools/test_code.sh <year>` and `tools/link_defined_terms.py --check`.

## Usage

| Time | Week | Event |
|---|---|---|
| 2026-11-21 09:44 | 22 % | watcher started (threshold 40 %); readers launched |
| 2026-11-21 10:25 | 27 % | Book 1 read: 61 defects (1 major, 21 minor, 39 nits), no wrong final answer; all accepted after triage, sent back for fixes. `\code` fixed in `onecs.sty` by the main session (R1-042: straight quotes, no `,,` ligature); trap classes sent to readers 2–5 |
| 2026-11-21 10:35 | 28 % | Book 2 read: 51 defects (1 major: g12-06 solutions quote an older run of a MEASURED output; 23 minor, 27 nits); all accepted, sent back. Main session: `\code` gets `\frenchspacing` (R2-046); `capture_output.py` also reads directives in a file's last five lines (R2-050) |
| 2026-11-21 10:39 | 29 % | Book 3 read: 60 defects (1 major: ch. 2 usual arithmetic conversions miss the third rule; 18 minor, 41 nits); all accepted, sent back. Main session: `test_code.sh` builds C/C++ tests under ASan+UBSan (R3-027; only `list_test.c` failed across Books 2–5) |
| 2026-11-21 10:41 | 29 % | Book 5 read: 63 defects (4 major: phi-placement theorem, release/acquire claimed SC, lambda step counts misquoted, fib CFG edge; 20 minor, 39 nits); all accepted, sent back |
| 2026-11-21 10:55 | 30 % | Book 4 read: 111 defects (5 major: resolution without factoring called complete, CRC merged-frame claim, two C++ solutions against their outputs, a problem answer not in its run; 36 minor, 70 nits; wrong-sense term links book-wide); all accepted, sent back |
| 2026-11-21 11:01 | 31 % | Book 1 fixed (61/61) and closed |
| 2026-11-21 11:06 | 31 % | Book 2 fixed (50 + 2 found while fixing; 1 rejected) and closed |
| 2026-11-21 11:24 | 33 % | Book 3 fixed (60/60) and closed; Book 5 fixed (63/63), main-session tests running |
| 2026-11-21 11:25 | 33 % | Book 5 closed |
| 2026-11-21 12:03 | 33 % | Book 4 closed; run closed; watcher stopped |

## Closed books

- **Book 1** closed 2026-11-21 11:01, verified and read. Reader: 61 defects (1 major, 21 minor, 39 nits), all fixed, none rejected (`sources/book1/READER_REPORT.md`, Resolution table). Main-session re-verification after the fixes: forced TL2026 build 0/0/0, 398 pp; `gates.sh` OK for grades 1–9 and typing; `test_code.sh` GREEN for grades 6–9 and typing; term links clean; the g1/02 grid page checked. Shared follow-ups the reader proposed (not done yet): `\code` spaces that never break; a gate for `\omcode` ranges that stop before the file's last non-blank line; the TikZ `grid`-without-`step` and unit-less radius traps in the shared docs; `link_defined_terms.py --apply` does not unwrap first.

- **Book 2** closed 2026-11-21 11:06, verified and read. Reader: 51 defects (1 major, 23 minor, 27 nits); 50 fixed, R2-042 rejected (Book 4 ch. 25 does teach the many-pattern trie with suffix links), and 2 more found and fixed while fixing (g11-10 Ex 8's carry answer; a wrong-sense "degrees" link). Main-session re-verification: forced TL2026 build 0/0/0, 523 pp; gates OK for grades 10–12; `test_code.sh` GREEN for all three; links clean; p. 104 (friendship graph) checked.

- **Book 3** closed 2026-11-21 11:24, verified and read. Reader: 60 defects (1 major, 18 minor, 41 nits), all fixed, none rejected. Ch. 30 and the C chapters now check every allocation (`realloc` through a temporary); `figures/measure.py` derives `measure.dat` from the printed timing and a test keeps them in step. Main-session re-verification: forced TL2026 build 0/0/0, 523 pp; `gates.sh bachelor-1` OK; full `test_code.sh bachelor-1` GREEN under ASan+UBSan (419 listings, 375 outputs rerun); links clean; the conversions figure (p. 34) checked.

- **Book 5** closed 2026-11-21 11:25, verified and read. Reader: 63 defects (4 major, 20 minor, 39 nits), all fixed, none rejected. R5-044: the SSI claim narrowed, Fekete's read-only anomaly walked through and kept as a test of what the simple check lets through. Main-session re-verification: forced TL2026 build 0/0/0, 583 pp; `gates.sh bachelor-3` OK; full `test_code.sh bachelor-3` GREEN (293 listings, 234 outputs rerun); links clean.

- **Book 4** closed 2026-11-21 12:03, verified and read. Reader: 111 defects (5 major, 36 minor, 70 nits), all fixed, none rejected. R4-080: resolution now includes factoring (`unify.py` `factors()`, `factor_demo.py`, three tests); R4-040/045: Book 2's process and synchronisation terms recalled, not redefined; about 50 wrong-sense link phrases protected in `book4_en.py`. Main-session re-verification: build 0/0/0, 646 pp; `gates.sh bachelor-2` OK; full `test_code.sh bachelor-2` GREEN under ASan+UBSan (485 listings, 494 outputs rerun); links clean; `factor_demo` output checked. `SERIES_DEFINITIONS.md` updated by the main session (process, deadlock, interrupt are Book 2's).

**Run closed 2026-11-21 12:03: all five books "verified and read". Readers found 346 defects (12 major); 344 fixed, 1 rejected (R2-042), plus 2 found while fixing; 398 / 523 / 523 / 646 / 583 pp, all 0/0/0 with gates, code tests and links green. Weekly plan 22 % → 33 %.** Shared changes made by the main session: `\code` (straight quotes, no `,,` ligature, `\frenchspacing`); `capture_output.py` reads directives in a file's last five lines; `test_code.sh` builds C/C++ tests under ASan+UBSan. Proposed and not done: `\code` spaces that never break; a gate for `\omcode` ranges that stop before a file's last non-blank line (Book 1 keeps 12 such ranges on purpose, so it needs an opt-out marker).

**Trap (agents' wait loops):** the Book 4 and 5 readers left three `until ! pgrep -f "latexmk -g …"; do sleep 10; done` shells. `pgrep -f` matches the loop's own command line, so they never end, and the agents stayed "waiting on background work" after their final report. The main session killed them by PID. Run long commands in the foreground (timeout up to 600000 ms), or wait on a PID (`while kill -0 $pid`), never on `pgrep -f` of a string the loop itself contains.

## Reader agents (for SendMessage; main session only)

Book 1 `af9b5781c0b94c4cc` · Book 2 `afbe25e1322077590` · Book 3 `a67112d47edb0dcdf` · Book 4 `a688094b7e0296ebe` ·
Book 5 `ad01804170968ca48`. All five launched 2026-11-21 09:50, Opus 5.5 high, Phase 1 (report only).
