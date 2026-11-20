# Contributing to One Computer Science Book

The authoritative conventions of this series. The cross-subject rules (chapter
anatomy, labels, visuals, quality gates) are in the workspace's `book_style.md`;
what follows adds or overrides them for computer science.

## Project structure

```
one_computer_science_book_<N>_<slug>.tex   one entry file per book (5)
styles/onecs.sty                           every package and macro; chapter files define nothing
styles/lang/en.tex                         UI strings and part titles
parts/<year>/NN-<slug>.tex                 a chapter (grade-1 ... grade-12, bachelor-1 ... bachelor-3)
parts/<year>/solutions/NN-<slug>.tex       its solutions
parts/typing/01-typing-drills.tex          Book 1's appendix of typing drills
code/<year>/NN-<slug>/listings/            every file a chapter prints (Python, C, C++, Rust, SQL, toy, RISC-V, shell, HTML/CSS)
code/<year>/NN-<slug>/outputs/<stem>.txt   what a listing printed, written only by tools/capture_output.py
code/<year>/NN-<slug>/exercises/           tested solution programs of the programming exercises
code/<year>/NN-<slug>/tests/               test_*.py (pytest), *_test.c, *_test.cpp, or a Cargo crate's tests
code/<year>/NN-<slug>/figures/             scripts that write the .dat tables a chart plots (tested)
code/shared/toymachine/                    the series' toy machine (TOYMACHINE.md), frozen
code/shared/rv/                            the RISC-V subset simulator (RV.md), frozen once written
code/shared/town/                          the invented town Brenmoor and its tables (TOWN.md), frozen
code/shared/sqlrun/                        the book's SQL runner over Python's sqlite3, frozen
data/town/*.csv                            the town's tables (python -m town rewrites them; no diff)
images/book<N>/                            photographs + CREDITS.md; ai/ illustrations (JPEG) + PROMPTS.md
sources/                                   outline provenance, ledgers, definition map, run files
tools/                                     gates, capture, term linker, ledger and calibration checks
```

Years and books: `grade-1`…`grade-9` → Book 1 (`g1`–`g9`); `grade-10`…`grade-12`
→ Book 2 (`g10`–`g12`); `bachelor-1/2/3` → Books 3/4/5 (`b1`–`b3`). Book 1's
appendix uses the prefix `typ`.

## Building and testing

```sh
make venv
PATH=~/texlive/2026/bin/x86_64-linux:$PATH latexmk one_computer_science_book_2_high_school.tex
bash tools/gates.sh grade-11           # the prose and structure gates of one year
bash tools/gates.sh --log 2            # 0 errors / 0 undefined / 0 overfull in the last build of Book 2
bash tools/test_code.sh grade-11       # ruff, pytest, C, C++, Rust, listing ranges, outputs rerun
python3 tools/capture_output.py code/grade-11/02-von-neumann-machine     # (re)capture a chapter's outputs
python3 tools/link_defined_terms.py --book 2 --unwrap --apply && python3 tools/link_defined_terms.py --book 2 --apply
```

## Code in the books

- **Code is never typed into a chapter.** A listing is `\omcode{path}{first}{last}{Caption}\label{lst:...}`
  (or `\omcodes{path}{a-b,c-d}{Caption}` for several ranges) from a file under
  `listings/`, at most 40 lines. Output is `\omoutput{path}{Caption}\label{out:...}`
  (or `\omoutput[1-4,9-12]{...}` for some lines) from `outputs/`, written only by
  `tools/capture_output.py`. A word or a short expression in prose is
  `\code{...}` (it prints exactly what is typed, braces must balance). No
  `lstlisting`, `verbatim` or `\lstinline` in a chapter (`tools/check_prose.py`).
- **Every printed output is real** and reruns byte for byte (`tools/check_outputs.py`).
  A listing that prints timings is listed in `listings/MEASURED.txt`, and its
  caption says ``on the author's laptop'' (the gate looks for *laptop*).
- **Every listing that is meant to work is tested**, and every programming
  exercise's solution is a file under `exercises/` with a test. A staged error
  (a compile error, a crash, a sanitizer report, a wrong answer) is printed on
  purpose, and the text says so.
- **How each language runs** is in `tools/capture_output.py`'s docstring:
  Python 3.12, `gcc -std=c17`, `g++ -std=c++20`, `rustc --edition 2021`, SQL
  through `code/shared/sqlrun/sqlrun.py`, toy assembly through
  `python -m toymachine`, RISC-V through `python -m rv`, shell sessions with
  `# capture: session`. Directives (`cflags=`, `args=`, `exit`, `fixtimes`,
  `<stem>.stdin`) are in the same docstring.
- **Listings stay in English** (identifiers, comments, printed strings) in this
  first edition; a language edition decides later what to translate.
- **Free tools, offline, on any operating system.** No account, no paid
  product, no online service, no package download in a listing (Python's
  standard library; Rust and C++ standard libraries; no crates.io dependency).
  Interfaces are drawn generically in TikZ; no screenshot of a real product.
- **Data is generated.** The town (`code/shared/town/`) or a seeded generator
  in the chapter's code. No dataset is downloaded.
- **Security is taught as defence**, on the book's own toy programs and
  servers on the reader's machine, never against a real system. Servers bind
  to `127.0.0.1` only.
- Nothing personal in print: the capture tool prints the account as `ada` and
  the machine as `laptop`; git sessions commit as Ada Lovelace
  `<ada@example.org>` on a fixed date.

## Statement environments and boxes

`definition`, `theorem`, `proposition`, `lemma`, `corollary`, `method`,
`example`, `remark`, `notation`, `exercise`, `problem`, `solution`, `proof`,
`\admitted`, as in the family. An algorithm is stated as a `method` (its
steps in prose or as a listing), its correctness and cost as a `theorem` or
`proposition` with a proof. Boxes: `recall` (*You already know*),
`history[title]`, `dated{year}`, `safety` (*Safe use*), `inpractice[title]`.
`\key{Ctrl}` draws a key, `\menu{File > Save}` a menu path.

## Figures

TikZ schematics (`omfigure`), with the styles of `styles/onecs.sty`: `cell`,
`ptr`, `frame box` (memory diagrams), `tnode`/`leafbox` and `forest` (trees),
`gnode`/`gedge`/`wedge` (graphs), the `automata` library, circuitikz logic
ports, `bytefield` (packet and instruction layouts), `pic {window}` with
`\omwindow{w}{h}{title}` (a generic window), `keycap` (a drawn keyboard).
Charts are pgfplots (`omrecord`) over `.dat` tables written by a tested script
in the chapter's `figures/`. Photographs: free licence only, credited per file
in `images/book<N>/CREDITS.md` and on the image-credits page. AI illustrations
(`tools/ai_images.py`, JPEG): generic everyday scenes, never a real product,
brand, logo, person or a screen the reader is meant to read. Every figure is
checked on its own rendered page, for collisions and for correctness.

## Labels

`<type>:<prefix>:<chapter-slug>:<name>`: `ch:`, `def:`, `thm:`, `prop:`,
`lem:`, `cor:`, `met:`, `ex:`, `rem:`, `not:`, `exo:`, `pb:`, `sec:`, `fig:`,
`tab:`, `lst:` (a listing), `out:` (an output). Reference with `\cref`;
across books, in prose only.

## Licensing of contributions

One Computer Science Book is free for everyone under the licences in the [README](README.md#license). Contributing
means agreeing to the following.

1. **Same licence in as out.** Your contribution is licensed under the same terms as the part of the
   repository it changes: CC BY-NC-SA 4.0 for book content ([`LICENSE`](LICENSE)), MIT for the
   software — `code/`, `tools/`, `.github/`, the `Makefile` and the build scripts ([`LICENSE-CODE`](LICENSE-CODE)).
2. **Sign off every commit** with `git commit -s`, which adds a line such as
   `Signed-off-by: Your Name <you@example.com>`. It certifies the
   [Developer Certificate of Origin 1.1](https://developercertificate.org): you wrote the change or
   have the right to submit it. For this project, "the open source license indicated in the file"
   in the certificate means the licences named in point 1.
3. **Relicensing grant.** You grant Benjamin Virrion a perpetual, worldwide, non-exclusive,
   royalty-free and irrevocable right to use, modify and relicense your contribution under other
   terms, including commercial ones (print editions, licences for schools, publishers or companies,
   paid app versions). You keep the copyright in your contribution and may use it as you wish.

**By signing off your commits you certify the DCO and agree to this whole section, including the
relicensing grant in point 3.** Why the grant exists: the books stay free under CC BY-NC-SA for
every reader; the grant only lets the author fund the project through commercial editions without
having to trace and ask every past contributor. Commits without a sign-off cannot be merged.
