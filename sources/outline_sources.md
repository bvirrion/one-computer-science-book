# Outline sources

Provenance of `OUTLINE.md` (written 2026-11-19). This is the only file, with
source comments, where the source programmes are named. The printed books never
name a programme, a country's school system or a university.

The lists below were written from knowledge of the programmes, not from the
official texts. **Before a book is written, its chapter list is checked against
the published programme texts**, and each chapter brief records the items it
covers.

## The user's frame (2026-11-19)

| Decision | Effect on the outline |
|---|---|
| Python at school; Python, C, C++, Rust and SQL at university | no OCaml and no Java; the preparatory class's OCaml content (algebraic types, pattern matching, functional style, immutable structures) is taught in Rust (Y2 Part II); its C content stays in C (Y1 Part I) |
| No block language; Python directly, after the machine | the middle-school programme's block programming is replaced by Python from grade 6; grades 1–5 teach the machine, typing, files, storage, the operating system, binary and algorithms by hand |
| Family chapter style, tested listings | definitions, methods, theorems, starred exercises, weekend problem; code only from tested files |
| A few machine-learning algorithm chapters | g11 k-NN, Y2 search and games, Y2 decision trees and clustering; the rest is the artificial intelligence series |

## Book 1 — Grades 1–9

| Grades | Source | Notes |
|---|---|---|
| 1–5 | French primary school, cycles 2–3: *questionner le monde* and *sciences et technologie* (digital objects, coding moves on a grid, a first algorithm), and the digital-skills framework (keyboard, files) | The programme is thin here. The user's list (hardware, typing, operating system, program, hard disk, SSD, RAM) sets the content; ordering and depth are this outline's own |
| 6–9 | French collège, cycles 3–4: *algorithmique et programmation* in mathematics and in technology (variables, loops, conditions, events), networks and the Internet in technology | Python replaces the block language; functions, lists, strings and dictionaries come earlier than in the programme, which leaves them to grade 10; `logic-gates`, `how-a-processor-runs-a-program`, `first-cryptography` and `html-and-css` are brought down from the high-school programmes, at a first-look level |

## Book 2 — Grades 10–12

| Grade | Source | Notes |
|---|---|---|
| 10 | SNT (*sciences numériques et technologie*, seconde): the Internet, the web, social networks, structured data, location and maps, embedded computing, digital photography; plus the Python of seconde mathematics | Only the technical content is kept: social networks become graphs, photography becomes image representation. The representation chapters (`machine-integers`, `floating-point`, `text-encodings`) and `data-tables` come from NSI première, moved down to balance the three years |
| 11 | NSI première: representation of data, constructed types, tables, human–machine interaction on the web, architecture and operating systems, language, algorithms (searches, sorts, greedy, k nearest neighbours), proofs by invariant and cost | Web interaction is in g10 `http-clients-servers`; constructed types are in Book 1 |
| 12 | NSI terminale: data structures (lists, stacks, queues, trees, graphs), databases and SQL, processes and scheduling, routing protocols, securing communications, recursion, modularity, object-oriented programming, computability, divide and conquer, dynamic programming, text search | All kept, at one chapter per item |

## Books 3–5 — University Years 1–3

| Book | Source | Notes |
|---|---|---|
| 3 (Year 1) | MP2I (first year of the computer science preparatory class) ∪ first-year computer science licence | C, data structures, algorithm design, propositional logic, induction and termination, databases from the preparatory class; shell, Git and digital circuits from the licence |
| 4 (Year 2) | MPI (second year) ∪ second-year licence | Formal languages and automata, predicate logic and deduction, concurrency, randomised algorithms, search and games, learning algorithms, text algorithms from the preparatory class; object-oriented programming, architecture, systems programming, networks and database design from the licence. C++ and Rust replace the licence's usual Java and OCaml |
| 5 (Year 3) | third-year computer science licence, read across several universities' course lists | Compilers, operating systems, computability and complexity, databases, distributed systems, security, software engineering. NP-completeness and decidability, which the preparatory class meets in its second year, are owned here; `computer-graphics` and `program-verification` are common options, kept as one chapter each |

## Cross-series inventory (2026-11-19)

The cross-series table of `OUTLINE.md` was built from a search of the existing
books' chapter files:

- `one-math-book`: prints no code and no pseudocode. Owns powers of two (g8
  `03-powers`), Euclid's algorithm (g9 `02-arithmetic-gcd`), induction (g12
  `01-sequences`), combinatorics (g12 `08-combinatorics`), modular arithmetic
  with a miniature RSA (g12 `10-arithmetic`), matrices and graphs (g12
  `11-matrices-graphs`), logic and sets (b1 `01-logic-sets-maps`). It has no
  chapter on number bases, Boolean algebra, graph algorithms or complexity.
- `one-physics-book`: owns the circuit chapters (g3–g12), signals (g10
  `08-signals-and-waves`), sampling and analog-to-digital conversion (b2
  `09-feedback-oscillators`), semiconductors and the transistor (b3
  `24-electrons-in-solids`). It has no chapter on logic gates or digital logic.
- `one-earth-and-space-sciences-book`: satellite positioning (g9
  `maps-of-the-earth`).
- `one-artificial-intelligence-book` and `one-quant-book`: extra-shelf series
  for readers who already program; named in prose only.
