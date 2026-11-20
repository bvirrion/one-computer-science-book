# Book 3 (University Year 1, `bachelor-1`, prefix `b1`) --- chapter briefs

Phase A, written 2026-11-20 by the Book 3 writer. Binding inputs: `OUTLINE.md` (chapter list of record, frozen
`part.tex`), `sources/BATCH_BOOKS_1-5.md`, `sources/SERIES_DEFINITIONS.md`. Nothing here is printed; programme
names appear in this file only (provenance).

Target: ~430 pp, 30 chapters, ~14 pp each (body ~600--700 source lines with listings and outputs, solutions
~250). Band: 12 exercises (4 one-star, 5 two-star, 3 three-star, in that order), one weekend problem of 22--28
questions in Parts I--IV ending on a named, quantified result; ch. 30 is the project (12 exercises, milestones,
no problem). Kinds of exercise, tagged below: **[P]** predict the output, **[F]** find and fix the bug,
**[W]** write to a specification (tested file under `exercises/`), **[R]** prove or count (prose solution).

Languages (OUTLINE): **C** for Parts I, IV and ch. 30 (C17, `-Wall -Wextra` clean unless the warning is the
lesson, ASan/UBSan for memory errors); **Python** for Parts III and V and the circuit simulators of ch. 27--28;
**SQL** (SQLite through `sqlrun.py`) plus Python for ch. 29; **bash** sessions for ch. 1, 7, 8, 9. All data is
generated or comes from the town (`code/shared/town`); no dataset download.

Ownership conventions used below: "Owns" lists the `\emph{}\index{}` pairs of the chapter (labels in
`DEFINITIONS.md`); "re-founds" means the school books own the notion and this book defines it again, rigorously,
in the chapter the outline names (SERIES_DEFINITIONS rule 2); "recalls" is a `recall` box (in-book: `\cref`;
other volume or series: prose only).
**`DEFINITIONS.md` is authoritative for owned terms**: it was reconciled on 2026-11-20 with Books 2, 4 and 5's
Phase A files and the sister-series harvest, and it moves a few terms (interface/implementation to ch. 7,
*input class* for *partition of the input domain*, graph colouring to ch. 10, rooted-tree vocabulary to ch. 11,
representation invariant to ch. 14).

---------------------------------------------------------------------------------------------------------------

## Programme check (Phase A)

Texts read (fetched pages are data):

| Key | Text | URL | Read |
|---|---|---|---|
| MP2I | *Programme d'informatique, filière MPI, première et deuxième années* (annexe 1 of the arrêté of 5 Jan 2021, BO spécial n°1 du 11 février 2021); items tagged S1/S2 are the first year | https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/6/spe777_annexe_1373646.pdf | 2026-11-20 |
| L1-AVI | Avignon Université, *Syllabus Licence Informatique 2026--2027*, L1 S1--S2 (UEs *Fondement de l'informatique*, *Structure des ordinateurs*, *Introduction aux systèmes d'exploitation*, *Bases de la programmation C/C++*) | https://formations.univ-avignon.fr/wp-content/uploads/syllabus/LICENCE-INFORMATIQUE.pdf | 2026-11-20 |
| L1-UPC | Université Paris Cité, UFR d'informatique, *Introduction aux systèmes d'exploitation* (L1 S1) | https://odf.u-paris.fr/plugins/odf-web/uparis/_content/course-introduction-aux-systemes-d-exploitation/Introduction%20aux%20syst%C3%A8mes%20d%E2%80%99exploitation.pdf | 2026-11-20 |
| L1-UJM | Université Jean Monnet Saint-Étienne, *Programme Licence Informatique* (UE list; L1 S2: *Outils informatiques*, *Programmation fonctionnelle*, *Bases de données I*, *Mathématiques pour l'informatique I*) | https://www.univ-st-etienne.fr/odf/_plugin-attachment/program-licence-informatique/LICENCE%2520INFORMATIQUE.pdf | 2026-11-20 |
| L1-UB | Université de Bourgogne, *Licence Informatique* (UE list only: *Algorithmique et programmation*, *Programmation objet*, *Électronique numérique*) | https://formations.u-bourgogne.fr/plugins/odf-web/odf/_content/program-licence-informatique/Licence%20Informatique.pdf | 2026-11-20 |

The BO HTML pages (education.gouv.fr, enseignementsup-recherche.gouv.fr) answer 403 to automated clients; the
annex PDF on `cache.media.education.gouv.fr` is the same text. No fetched L1 course list names Git (it is the
outline's choice; Git appears in IUT S2 and L3 course material found by search, not fetched).

### Coverage, item by item (MP2I first-year items, S1/S2)

| MP2I item | Chapter(s) |
|---|---|
| 1.1 program as an algorithm's implementation; paradigms observed (imperative, functional, logic) | 1 (remark), 10, 29 (remark: a query language as a declarative/logic paradigm) |
| 1.1 compiled vs interpreted; source → object → executable; interface vs implementation files | 1, 7 |
| 1.1 representation of floats, precision problems, comparisons with tolerance | 2 (recall of Book 2 g10 `floating-point`; the C side: `double`, tolerant comparison) |
| 1.1 termination, partial and total correctness, variant, invariant | 11, 12 |
| 1.1 complexity: worst case, average case, amortised cost | 13, 14, 19 |
| 1.2 specification of inputs/outputs; signatures; pre/postconditions and invariants as comments | 12 (and every chapter's listings) |
| 1.2 defensive programming, assertions, exit on failed assertion; weak typing of C vs strong typing | 7, 2 (remark) |
| 1.3 test sets, partition of input domains, boundary tests | 7, 12 |
| 1.3 **control-flow graph, feasible paths, statement/branch/path coverage; exhaustive testing of a compound condition** | 7 (claimed here; see contested terms) |
| 2 recursion, mutual recursion, tree of activations; usual recurrences | 3, 11, 13 |
| 2 ordered sets, predecessor/successor (immediate), minimal element, product and lexicographic order, well-founded order | 11 |
| 2 inductive sets, induced order, structural induction | 11 |
| 3.1 base types, pointer, array, compound type, static arrays, `malloc`/`free` | 2, 4, 5, 6 |
| 3.1 abstract data structure: type + operations (constructor, accessor, transformer); interchangeable implementations | 14 (re-founds Book 2 g12), 15 |
| 3.1 mutable vs immutable | recalled (Book 2 g10); persistent structures are Year 2 |
| 3.2 list by array and by links; stack, queue (array and links) | 15 (and 14) |
| 3.2 associative array by hash table | 16 |
| 3.2 **serialisation of a hierarchical and of a relational structure** | 17 (a tree, preorder with markers), 24 (a graph as an edge list file) |
| 3.3 binary tree defined inductively; vocabulary; height of the empty tree is −1; complete tree in an array | 11, 18 |
| 3.3 arbitrary-arity tree converted to a binary tree | 11 (left-child right-sibling) |
| 3.3 traversals pre/in/postorder; link with the call stack | 11 (recalled from Book 2 g12, proved), 17 |
| 3.3 associative array by a binary search tree; **red-black tree** | 17 (red-black upgraded from "told" to height bound proved + insertion; see report) |
| 3.3 heap property; priority queue; heapsort | 18 |
| 3.4 graphs: directed/undirected, degrees, path, cycle, connectivity, strong connectivity, DAG, tree as acyclic connected graph, forest, bipartite, weights, labels; matrix and list representations | 24 |
| 4.2 brute force, backtracking (sweep line mentioned) | 20 (21 for the strip of closest pair) |
| 4.3 greedy exact: Huffman, activity selection, unit tasks with deadlines and penalties on one machine | 22 |
| 4.3 divide and conquer, **meet in the middle**, dichotomy (merge sort, inversions, closest pair, subset sum by meet in the middle, binary search, **dichotomy on the answer**) | 19, 21 (meet in the middle, inversions, dichotomy on the answer added to the brief) |
| 4.3 dynamic programming: optimal substructure, overlapping subproblems, bottom-up and memoisation, rebuilding (subset sum, weighted scheduling, LCS, edit distance) | 23 |
| 4.4 text search (Boyer--Moore, Rabin--Karp); Huffman, LZW | Huffman in 22; text algorithms are Book 2 g12 (Horspool) and Book 4 `text-algorithms` (not this book) |
| 4.5 traversals, BFS/DFS, traversal tree, cycles, bipartiteness, unit-distance shortest paths; reachability, topological sort by DFS, connected components | 24 |
| 4.5 Dijkstra with a priority queue, Floyd--Warshall | 25 |
| 4.5 (S3-4 there) Kosaraju, Kruskal; union--find (3.3, S3-4) | 24, 26 (the outline puts them in Year 1; kept) |
| 5.1 stack and heap of a compiled program, globals, activation record; scope and lifetime; locals and parameters on the stack; dynamic allocation, NULL, `void *`, casts, link with arrays, segmentation fault | 1, 3, 4, 5 |
| 5.2 file interface (size, sequential access); blocks and inodes; hard and symbolic links; namespace; access rights; standard streams, redirections, pipes; mounting removable media | 6 (C files), 8 (shell: links, rights, streams, pipes; mounting told, it needs root); inodes are Book 4's (used, not defined) |
| 6.1 propositional variables, connectives, formulas by induction, trees, subformula, size, height | 10 |
| 6.1 quantifiers, free and bound variables, scope, substitution | **not in this book**: Book 4 `predicate-logic` (gap relative to the year only) |
| 6.2 valuations, satisfiability, model, tautology, antilogy, equivalence, consequence, CNF/DNF, normalisation and exponential blow-up, SAT, n-SAT, Quine's algorithm, modelling | 10 |
| 7 databases: vocabulary, primary key, entity--association, foreign key, 1--1/1--*/*--*, SELECT/WHERE/AS, DISTINCT, LIMIT, OFFSET, ORDER BY, UNION/INTERSECT/EXCEPT, product, JOIN, LEFT JOIN, aggregates, GROUP BY, HAVING, nested queries | 29 (the licence adds relational algebra, which this programme excludes; kept) |
| Annex A (C): fixed-width integers, overflow, `char`, `double`, `bool`, `const`, static and multidimensional arrays, `struct`/`typedef`/`->`, strings (`strlen`, `strcpy`, `strcat`), control flow, pointers, `NULL`, `malloc`/`sizeof`/`free`, `void *`, dynamic arrays and their linearisation, `assert`, `printf`/`scanf`, headers and include guards, `argc`/`argv`, `atoi`, initialisers, designated initialisers, separate compilation, `fopen`/`fclose`/`fscanf`/`fprintf` | 2--7 (linearisation of 2-D arrays in 5; designated initialisers in 6); pthreads are Book 4 |

### Licence L1 items (L1-AVI, L1-UPC, L1-UJM, L1-UB)

| Item | Chapter(s) |
|---|---|
| Boolean algebra, truth tables, Karnaugh maps, combinational circuits, integer operations and their circuits | 27 |
| two's complement, IEEE 754 | Book 2 g10 (recalled in 2 and 27) |
| ALU, routing of information (multiplexers), flip-flops, counters, registers, memories, control unit, sequencing | 27, 28 |
| **micro-programming** | 28 (told, one remark; not in the outline description) |
| Unix shell: command syntax, manual, file system (inodes, links, directories, rights), special characters, expansion, quoting, processes and signals, standard streams, redirections, pipes, filters, scripts, `find`, `sed` | 8 (inodes and signals used at the user level; Book 4 owns them) |
| OS structure, scheduling, paging | Book 2 g12, Book 5 (not this book) |
| C/C++ programming basics; object-oriented programming; web design; discrete mathematics; analysis | 1--7; OOP and C++ are Book 2 g12 / Book 4; web is Books 1--2; mathematics is the mathematics series |
| databases I | 29 |
| functional programming (L1-UJM) | Book 4 Part II (Rust); recursion and induction here in 11 |

### Items no chapter of this book covers (none is a hole in the series)

1. Quantifiers, free/bound variables, substitution (MP2I 6.1, S2) → Book 4 `predicate-logic`.
2. Text search (Boyer--Moore, Rabin--Karp) and LZW (MP2I 4.4, S2) → Book 2 g12 `text-search`, Book 4 `text-algorithms`.
3. Exceptions "not only for errors" (MP2I 1.2) → C has none; Book 4 (C++ exceptions, Rust `Result`).
4. Blocks and inodes as an implementation (MP2I 5.2, S1) → Book 4 `files-pipes-signals`, Book 5 `file-systems`;
   ch. 8 shows `ls -i`, hard and symbolic links at the user level.
5. Mutable/immutable as a language feature (MP2I 3.1) → Book 2 g10; persistence in Book 4 `functional-programming`.
6. Typical sizes of real graphs (MP2I 3.4 asks for them): needs sourced numbers; one `dated` box in 24 if the
   ledger can source two of them (web graph, a road network), otherwise left out.

---------------------------------------------------------------------------------------------------------------

## Shared conventions of this book (decided here, apply to every chapter)

- **C listings**: `#include` lines are printed only the first time a header is met in a chapter, then
  `\omcodes` skips them. Every C library file (`vec.c`, `list.c`, ...) has a `tests/*_test.c` linked with
  `// test-with: ../listings/<file>.c`. Demo programs with a `main` are exercised by their captured output.
  Multi-file demos need the capture directive requested in the report (`with=`); until then they run as
  `# capture: session` scripts.
- **Addresses** are printed only as differences or orders ("the heap block is above the globals"), never raw:
  raw addresses depend on the kernel, the loader and libc, even with `setarch -R`.
- **Sanitizer reports** are printed with `\omoutput[ranges]` showing the first frame lines only (later frames
  carry libc offsets that change with the C library).
- **Python listings** in Parts III and V use dataclasses and type hints where they help reading; tests use
  pytest, hypothesis where a property is the lesson (ch. 11, 12, 19).
- **Counts before clocks**: where a cost is the point, the program counts operations (deterministic, testable);
  timings (`MEASURED.txt`, caption says *laptop*) only where the lesson is the machine (1, 13, 14, 15, 16, 19,
  21, 30).
- **Height of the empty tree is −1** (MP2I convention), size and height defined in ch. 11 and used throughout.
- **Indices from 0**, half-open intervals `[lo, hi)` for array algorithms (ch. 12 justifies it).
- **History boxes** (one or two per chapter) carry a ledger row for every date, name and place.
- Schematics ~4 per chapter (the band's budget); photographs where a real historic machine or part is the
  subject (ch. 1, 8, 19, 27, 28, and one or two more); AI illustrations sparingly (university band): ch. 9 (a
  team at a shared table), ch. 30 (a desk with paper folders), perhaps ch. 16 (a library card catalogue drawer),
  no screen to read, no letters.

---------------------------------------------------------------------------------------------------------------

# Part I --- C and the machine model

## 1 `compilation-pipeline` --- From Source Code to a Running Program (~14 pp)

Programme: MP2I 1.1 (compiled/interpreted; source → object → executable; interface vs implementation), 5.1
(stack, heap, globals); Annex A (headers, `#include`); L1-AVI C basics.

Hook: the same eight-line program typed twice, once as `hello.py`, once as `hello.c`; one runs at once, the
other needs a command first. What happens between the text and the running program?

Sections:
1. *The four stages* --- preprocessing (`gcc -E`: `#include` and `#define` expanded; line count of the
   expansion), compiling to assembly (`gcc -S`: a few lines of the x86-64 output read, only as compiler output),
   assembling to an object file (`gcc -c`), linking to an executable. A method box: the commands of each stage.
2. *Object files, symbols and the linker* --- a two-file program (`main.c` calls `square` defined in `square.c`);
   `nm` shows `T square` and `U square`; the linker resolves; staged `undefined reference` and `multiple
   definition` errors; static linking vs shared libraries (told; `ldd` not printed, machine-specific); the
   executable format named (ELF, told).
3. *Warnings as a tool* --- `-Wall -Wextra` on a program with an uninitialised variable, a `printf` format
   mismatch, an assignment in a condition; each warning read, the bug fixed; `-Werror` in tests.
4. *The memory of a running process* --- code, static data (initialised and zero-initialised), call stack,
   heap; a program printing which object lies above which (orders and differences only); lifetime of each
   region (whole run vs call vs programmer-chosen); forward pointers to ch. 3 (stack) and 5 (heap).
5. *Interpreted and compiled* --- the same sieve in Python and C; Python compiles to bytecode (`dis` on a
   three-line function) that an interpreter loop runs; measured times on the author's laptop (MEASURED);
   what each approach buys (portability, start-up, speed, error detection before running).

Owns: source file, preprocessor, compiler, object file, symbol (of an object file), linker, executable file,
compiler warning, interpreter, bytecode, memory layout of a process (code segment, data segment). Re-founds
nothing. Recalls: program and operating system (Book 1 g4), machine language (Book 1 g7), assembly language
(Book 2 g11), process (Book 2 g12, prose).

Listings (`code/bachelor-1/01-compilation-pipeline/listings/`): `hello.c`; `hello.py`; `stages.sh`
(session: `gcc -E hello.c | wc -l`, `gcc -S`, `head` of `hello.s`, `gcc -c`, `nm hello.o`, link, run);
`main.c`, `square.c`, `square.h`; `linking.sh` (session: separate compilation, `nm`, success, staged undefined
reference, staged multiple definition); `warnings.c` (staged warnings, `exit`); `warnings_fixed.c`;
`regions.c` (order of a global, a static, a local, a heap block, a string literal and a function's code);
`sieve.c`, `sieve.py` + `timing.sh` (MEASURED); `bytecode.py` (`dis`).
Outputs captured for all; `hello.s` excerpt via a session `head -n 20`.
Tests: `tests/square_test.c`; `tests/test_sieve.py` (both sieves agree to 10^5).

Figures: (S1) the pipeline: files and tools from `.c` to a running process; (S2) two object files' symbol tables
and the linker's resolution arrows; (S3) the memory of a running process, regions in address order with their
lifetimes; (S4) interpreter loop vs compiled code (bytecode fetched and dispatched). Photograph: a PDP-11 (the
machine of early Unix and C) in a `history` box on C (Commons, licence read). AI: none.

Exercises: 1★[P] which stage reports each of four errors; 2★[P] read an `nm` listing: defined, undefined,
data; 3★[P] in which region does each of six objects live; 4★[P] what `gcc -E` makes of a macro;
5★★[F] `multiple definition` from a variable defined in a header (fix: `extern` + one definition);
6★★[F] `if (x = 0)` found by a warning; 7★★[W] split a one-file program into a module and a header, give the
commands; 8★★[R] count how many times a header without guards is read in a diamond of includes; 9★★[P] value
of a static local vs an automatic local across calls; 10★★★[R] after editing one of k source files, how many
compiler runs does separate compilation need, and the total for a sequence of edits; 11★★★[W] a function
`region_of(const void *p)` that classifies a pointer by comparing with markers (tested on this machine only,
with a reasoned caveat); 12★★★[R] given three symbol tables, decide whether linking succeeds; state and prove
the condition (every undefined symbol defined exactly once among the inputs).

Weekend problem --- *One program, four files, one process* (24 q.): Part I preprocessing (expansion sizes, macro
traps), Part II compiling and object files (symbols, sizes from `size`), Part III linking (resolution, two
errors, a static function), Part IV the running process (which object in which region, which lives longest).
Named result: *the placement table* --- each of the program's ten objects placed in its region with its
lifetime, checked against `regions.c`'s run.

Ledger: `b1:c-origin` (C, Bell Labs, early 1970s; Ritchie, *The Development of the C Language*, HOPL-II 1993);
`b1:c17` (ISO/IEC 9899:2018 is C17; ISO page); `b1:gcc-stages` (`-E -S -c`, GCC 11 manual); `b1:elf` (ELF named;
System V ABI / refspecs); `b1:pyc` (Python compiles to bytecode, `dis` module, Python 3.12 docs); photo credit.

## 2 `c-types-and-control` --- C: Types, Operators and Control Flow (~15 pp)

Programme: MP2I 1.1 (floats, precision), 1.2 (weak typing in C), Annex A (`int8_t`... `uint64_t`, overflow,
`char`, `double`, `bool`, operators, `const`, `if`, `while`, `for`, `break`); L1-AVI.

Hook: a loop counting down to zero with an unsigned counter that never stops.

Sections:
1. *Integer types and their widths* --- `char`, `short`, `int`, `long`, `long long`; the minimum widths the
   standard promises vs the widths on this machine (LP64); `<stdint.h>` exact widths; `<limits.h>`; unsigned
   arithmetic is modulo 2^N; signed overflow is undefined. Two's complement recalled (Book 2 g10).
2. *Floating types and characters* --- `float`, `double` (binary64 recalled from Book 2 g10); `0.1 + 0.2 != 0.3`
   in C; comparing with a tolerance (absolute and relative); `char` as a small integer, character constants,
   `'\0'`; `bool` from `<stdbool.h>`.
3. *Conversions and their traps* --- integer promotions, the usual arithmetic conversions; `-1 < 1u` is false;
   truncation on assignment; `double` to `int`; explicit casts; the warning `-Wsign-compare`; C's weak typing
   compared with Python's checks (remark).
4. *Operators and order of evaluation* --- precedence and associativity (an expression drawn as its tree);
   short-circuit `&&` and `||`; integer division truncates toward zero and `%` follows; side effects and
   sequencing: `i = i++ + 1` is undefined; `const`.
5. *Control flow and undefined behaviour* --- `if`, `switch` with fall-through (and `-Wimplicit-fallthrough`),
   `while`, `do while`, `for`, `break`, `continue`; undefined behaviour: what the standard does not promise, why
   the optimiser may assume it never happens (`x + 1 > x` folded at `-O2`), unspecified and
   implementation-defined behaviour; UBSan catches signed overflow.

Owns: integer type, width (of an integer type), integer overflow, integer promotion, usual arithmetic
conversions, cast, short-circuit evaluation, side effect, undefined behaviour, unspecified behaviour,
implementation-defined behaviour, switch statement (named in words), fall-through. Recalls: two's complement,
floating-point representation (Book 2 g10), Boolean value (Book 1 g6), character code (Book 1 g5).

Listings: `sizes.c` (`sizeof`, limits); `wrap.c` (unsigned wrap); `overflow.c` (`cflags=-O0 -fsanitize=undefined`,
staged UBSan report); `conversions.c` (staged `-Wsign-compare` + surprising results); `floats.c` (`0.1+0.2`,
tolerant comparison); `division.c` (`-7/2`, `-7%2`); `precedence.c`; `days.c` (switch, staged fall-through
warning, then fixed); `fold.sh` (session: the same `fold.c` at `-O0` and `-O2`, different answers); `countdown.c`
(staged unsigned infinite loop bounded by `timeout=2` and a printed count cap); `collatz_steps.c` (loops).
Tests: `tests/saturating_test.c` (exercise), `tests/test_reference.py` (Python reference for the problem's
checksum).

Figures: (S1) the 8-bit circle: unsigned 0..255 and signed −128..127 on one wheel, wrap points marked;
(S2) the conversion ladder (ranks, signed/unsigned) as a small lattice; (S3) the expression tree of
`a + b * c > d && e` with evaluation order of `&&`; (S4) a `switch` as a jump table with fall-through arrows.

Exercises: 1★[P] sizes and limits printed; 2★[P] `-7/2`, `-7%2`, `7/-2`; 3★[P] four mixed-sign comparisons;
4★[P] trace a `do while`; 5★★[F] `for (unsigned i = n - 1; i >= 0; i--)`; 6★★[F] `(lo + hi) / 2` overflow →
`lo + (hi - lo) / 2`; 7★★[W] `int32_t sat_add(int32_t, int32_t)` without undefined behaviour; 8★★[P] a `switch`
with fall-through; 9★★[R] count the `uint8_t` values with `x * x % 256 == 1` (modular arithmetic recalled);
10★★★[R] prove `x + (~x + 1) == 0` for N-bit unsigned; 11★★★[W] `bool mul_overflows(int64_t, int64_t)` checked
before multiplying; 12★★★[R] `for (int i = 0; i <= n; i += 2)` --- for which `n` is behaviour undefined, prove,
and fix.

Weekend problem --- *The checksum that lied* (24 q.): a 16-bit checksum over the town's weather file computed by
two colleagues' programs that disagree. Part I widths and the specification; Part II arithmetic modulo 2^16 and
its laws (proofs); Part III promotions: `uint16_t a * b` is computed in `int`, and `65535 * 65535` overflows a
32-bit `int` (undefined); Part IV the corrected, undefined-behaviour-free version agrees with a Python reference
on every record. Named result: *the promotion trap* --- the exact smallest operands whose product overflows, and
the agreement count of the fixed program (731/731 records).

Ledger: `b1:c-min-widths` (C17 5.2.4.2.1 minimum magnitudes; cppreference); `b1:lp64` (LP64 on x86-64 Linux:
`int` 32, `long` 64, pointers 64; x86-64 psABI); `b1:c-div-trunc` (C99+ division truncates toward zero;
C17 6.5.5); `b1:c-stdint` (`<stdint.h>` exact-width types optional, present here); `b1:ubsan` (GCC 11
`-fsanitize=undefined`); binary64 row shared with Book 2 if it has one, else `b1:binary64` (IEEE 754-2019).

## 3 `c-functions-and-stack` --- Functions and the Call Stack (~14 pp)

Programme: MP2I 2 (recursion, mutual recursion, tree of activations, machine-level memory and context saving),
5.1 (activation record, scope and lifetime, locals and parameters on the stack, globals); Annex A (declaration,
definition, passing by value).

Hook: a `swap` function that swaps nothing.

Sections:
1. *Declaring and defining functions* --- prototype, definition, why the order matters; passing by value
   (the failed `swap`); return values; `void`.
2. *The call stack and its frames* --- what a call does at the machine level (told: return address pushed,
   saved registers, locals); the stack frame; frames observed by printing the differences between the addresses
   of a local at depths 0--4; the frame popped on return.
3. *Recursion on the stack* --- the frames of a recursive call (factorial avoided per the programme: sum of
   digits, binary representation, power); the tree of activations of a doubly recursive function (binomial
   coefficients by Pascal's rule) and its count; mutual recursion (`is_even`/`is_odd`; a tiny expression
   evaluator); depth and stack overflow (staged, with a bounded stack); tail calls and what `-O2` does (one
   captured session; the theory is the Year 2 volume's).
4. *Scope and lifetime* --- block scope, shadowing, automatic vs static storage duration, static locals,
   global variables and internal linkage (`static` at file scope); returning the address of a local (staged
   warning `-Wreturn-local-addr`).

Owns: function declaration (prototype), function definition, parameter passing by value, call stack, stack
frame, return address, tree of activations (call tree), mutual recursion, stack overflow, scope, lifetime
(storage duration), automatic variable, static variable, global variable. Re-founds: call stack, stack frame
(Book 2 g12 `recursion`). Recalls: recursion, base case (Book 2 g12), induction (mathematics).

Listings: `swap_value.c`; `frames.c` (address differences of locals, `cflags=-O0`); `digits.c`;
`calltree.c` (prints the indented activation tree of `binom(4, 2)` and the call count); `even_odd.c`;
`evaluator.c` (mutual recursion over a tiny grammar of digits, `+` and parentheses); `depth.sh` (session:
`ulimit -s 512`, a recursive counter, staged crash with exit status, printed depth); `tail.sh` (session: the
same tail-recursive function at `-O0` crashes, at `-O2` does not); `counter_static.c`; `shadow.c`;
`dangling_local.c` (staged warning). Tests: `tests/binom_test.c`, `tests/evaluator_test.c`.

Figures: (S1) three frames `main → f → g` with parameters, locals, return addresses (frame box); (S2) the tree of
activations of `binom(4, 2)`, leaves marked, with the live frames at one instant highlighted (depth vs count);
(S3) lifetimes on a time axis: a global, a static local, two automatic locals, a returned dangling address;
(S4) stack depth growing to the limit (overflow) for a deep recursion vs a loop.

Exercises: 1★[P] the failed swap; 2★[P] which `x` is printed (shadowing); 3★[P] a static counter over three
calls; 4★[P] draw the frames at a marked line; 5★★[F] function returning the address of a local array; 6★★[F]
recursion with no base case for negative input; 7★★[W] an iterative version of a recursive digit sum (no
depth limit); 8★★[R] number of calls of naive `binom(n, k)`: `2 binom(n, k) − 1`, proved; 9★★[P] trace mutual
recursion on 7; 10★★★[R] naive Fibonacci: at most n frames alive at once but `2F(n+1) − 1` calls, proved;
11★★★[W] Hanoi printing moves and the maximal depth reached; 12★★★[R] with a measured frame of s bytes and a
stack of S bytes, bound the depth, and compare with the crash depth of `depth.sh`.

Weekend problem --- *How deep can a program go?* (24 q.): Part I frames measured (sizes from address
differences, `-O0`); Part II trees of activations for three recursion shapes (linear, binary, Hanoi): calls
vs depth, counted and proved; Part III mutual recursion and tail calls; Part IV the stack budget. Named result:
*the depth bound* `d_max = ⌊S / s⌋` (to within the start-up frames), predicted and checked against the crash
depth under `ulimit -s`.

Ledger: `b1:psabi-frame` (x86-64 System V psABI: `call` pushes the return address, 16-byte stack alignment at a
call); `b1:linux-stack-default` (default 8 MiB stack limit; `dated{2026}`; getrlimit man page / this machine's
`ulimit -s` is not a source, the man page is); `b1:gcc-return-local-addr` (GCC 11 warning).

## 4 `pointers-and-arrays` --- Pointers and Arrays (~15 pp)

Programme: MP2I 3.1 (pointer, static arrays), 5.1 (relation with arrays, segmentation violation), Annex A
(`&`, `*`, NULL, passing a pointer, array parameters, multiple results); L1-AVI.

Hook: `scanf("%d", n)` crashes; `scanf("%d", &n)` works. What is the `&` for?

Sections:
1. *Addresses and pointers* --- memory as numbered bytes (recalled Book 1 g4); `&`, pointer types, `*`;
   `sizeof` a pointer (8 here); the null pointer; `%p` (printed once, then only differences).
2. *A pointer passed to change the caller's data* --- `swap` fixed; several results through pointer
   parameters (`divmod`); `scanf` explained; `const` pointers (read-only views).
3. *Arrays and pointer arithmetic* --- arrays are contiguous; `a[i]` is `*(a + i)`; pointer differences
   (`ptrdiff_t`); the one-past-the-end pointer; array-to-pointer conversion; arrays as parameters (the length
   travels separately; the `sizeof` trap, staged warning); two-dimensional static arrays in row-major order.
4. *Out of bounds* --- the language does not check; an off-by-one write that changes a neighbour; ASan reports
   for stack and global buffers (staged); a segmentation fault from a NULL dereference.
5. *Pointers to functions* --- a comparator for `qsort`; a table of operations; `void *` as "address of
   anything" (first look, ch. 5 uses it).

Owns: address, pointer, dereferencing, null pointer, pointer arithmetic, array (C), array-to-pointer
conversion, out-of-bounds access, row-major order, function pointer, `void` pointer (generic pointer).
Re-founds nothing (pointer is owned here). Recalls: memory and addresses (Book 1 g4/g7), list (Book 1 g7).

Listings: `addr.c`; `swap_ptr.c`; `divmod.c`; `read_number.c` + `.stdin`; `array_layout.c` (differences);
`decay.c` (staged `-Wsizeof-array-argument`); `rowmajor.c`; `neighbour.c` (`cflags=-O0`, off-by-one changes a
neighbour, behaviour shown and then the ASan version `oob_asan.c` with `cflags=-O0 -g -fsanitize=address`);
`nullderef.c` (`exit`, segmentation fault status); `sort_people.c` (`qsort` with comparators on the town's
people loaded from a small embedded table); `ops_table.c`. Tests: `tests/minmax_test.c`, `tests/reverse_test.c`,
`tests/generic_max_test.c`.

Figures: (S1) cells with addresses, a variable and a pointer to it, after `*p = 7` (cell/ptr styles); (S2) an
`int` array with `a`, `a+1`, ... and byte addresses stepping by 4; one-past-the-end marked; (S3) row-major
layout of a 3×4 array, index formula `i*4 + j`; (S4) caller and callee frames during the fixed `swap`, pointers
from the callee's frame into the caller's. Photograph (optional): a memory module (DIMM), if Book 1 does not
already print the same file.

Exercises: 1★[P] values after a sequence of pointer assignments; 2★[P] draw the memory diagram; 3★[P] pointer
differences in an array of `double`; 4★[P] `sizeof` in `main` vs in a function; 5★★[F] `scanf` without `&`;
6★★[F] `for (i = 0; i <= n; i++)` with its ASan report; 7★★[W] `min_max(const int *a, size_t n, int *min, int
*max)`; 8★★[W] in-place reversal with two pointers; 9★★[P] `a[i]` and `i[a]`; 10★★★[R] the two-pointer
reversal is correct and makes ⌊n/2⌋ swaps; 11★★★[W] a generic `max` over `void *` with a comparator;
12★★★[R] count the pairs of valid pointers `p ≤ q` into an array of n elements (one-past-the-end included):
`(n+1)(n+2)/2`.

Weekend problem --- *A spreadsheet in a flat array* (24 q.): a grid of cells stored row-major in one block.
Part I the index map `(i, j) ↦ i·w + j` and its inverse, proved a bijection; Part II walking rows and columns
with pointers (strides); Part III in-place transpose of a square grid; Part IV an off-by-one in the transpose
found by ASan, fixed. Named result: *the in-place transpose makes exactly n(n−1)/2 swaps*, proved and counted.

Ledger: `b1:ptr-size` (8-byte pointers in LP64; psABI); `b1:c-one-past-end` (C17 6.5.6; cppreference);
`b1:qsort` (C17 7.22.5.2); `b1:asan` (AddressSanitizer in GCC 11 docs).

## 5 `dynamic-memory` --- Dynamic Memory (~14 pp)

Programme: MP2I 3.1 (`malloc`/`free`), 5.1 (dynamic allocation, NULL, `void *`, casts, link with arrays,
memory protection); Annex A (dynamic arrays, linearisation of multidimensional arrays).

Hook: a program reads a file of unknown length; how big should its array be?

Sections:
1. *`malloc` and `free`* --- the heap; `void *` and `sizeof *p`; checking for NULL; `calloc`; `realloc` and why
   its result goes to a new variable; a lifetime chosen by the programmer.
2. *Errors and the tools that find them* --- leak, double free, use after free, dangling pointer, reading
   uninitialised memory; each staged and its AddressSanitizer / LeakSanitizer report read (first lines);
   a debugger is described in ch. 7.
3. *Who frees what* --- conventions: the function that allocates documents who frees; create/destroy pairs;
   borrowed pointers that must not be freed; the convention written in the interface comment (the word
   *ownership* and its compiler-checked form are the Year 2 volume's; here it is a convention).
4. *A growable array written by hand* --- `push` with `realloc`; growth by one vs doubling; element copies
   counted (deterministic); the proof that doubling copies fewer than 2n elements, with the general amortised
   theory left to ch. 14.
5. *Two-dimensional arrays of unknown size* --- an array of row pointers vs one linearised block; index
   formula; freeing each.

Owns: heap (memory region), dynamic allocation, memory leak, dangling pointer, use after free, double free,
growth factor (of an array), linearised array. Recalls: pointer, `void *` (ch. 4), row-major (ch. 4).
Avoids defining *ownership* (Book 4 `rust-ownership` owns it) and *dynamic array* (ch. 14 owns it).

Listings: `alloc_basic.c`; `leak.c`, `double_free.c`, `uaf.c`, `uninit.c` (each `cflags=-O0 -g
-fsanitize=address` or `undefined`, staged); `nullcheck.c`; `intvec.h`, `intvec.c` (NORUN, tested),
`intvec_demo.c` (needs `with=intvec.c`, see report; fallback: session); `copies.c` (copies for +1 and ×2
growth, n = 10^3..10^6); `grid_rows.c`, `grid_flat.c`; `read_all.c` (reads an unknown number of integers from
stdin into a growing array) + `.stdin`. Tests: `tests/intvec_test.c`, `tests/strdup_test.c`,
`tests/grid_test.c`, `tests/pool_test.c`.

Figures: (S1) stack frame pointing into heap blocks, one freed block greyed; (S2) lifetimes: automatic vs heap
block on a time axis; (S3) a dangling pointer before and after `free`, and a double free; (S4) growth by
doubling: capacities 1, 2, 4, 8, 16 with copied elements shaded; (S5, optional) row pointers vs one flat block.

Exercises: 1★[P] which error do four snippets contain; 2★[P] bytes requested by `malloc(n * sizeof *p)` for a
given struct; 3★[P] values after a `realloc` that moves; 4★[P] where is the leak; 5★★[F] `p = realloc(p, ...)`
losing the block on failure; 6★★[F] freeing a chain of nodes using a freed node; 7★★[W] `my_strdup`;
8★★[W] free a row-by-row 2-D array; 9★★[R] copies made when growing by a constant k to n elements (≈ n²/2k);
10★★★[R] doubling makes fewer than 2n copies, proved; 11★★★[W] a fixed-size block pool with a free list
(tested with ASan); 12★★★[R] peak memory during a doubling `realloc` that moves (≤ 3n slots), proved.

Weekend problem --- *The leaky phone book* (24 q.): a contact-list program with five planted memory errors and a
growth policy. Part I reading the sanitizer reports; Part II fixing them under a written convention of who
frees; Part III growth policies (+k, ×2, ×1.5): copies counted and measured; Part IV the memory budget. Named
result: *the growth-factor trade-off* --- with factor r > 1, at most n/(r−1) copies and at most (r−1)n unused
slots, proved, and the counts of Part III checked against the bounds.

Ledger: `b1:malloc-spec` (C17 7.22.3 `malloc`, `calloc`, `realloc`, `free`; cppreference);
`b1:lsan` (LeakSanitizer enabled with ASan on Linux; GCC/sanitizers docs).

## 6 `c-strings-structs-files` --- Strings, Structures and Files (~15 pp)

Programme: MP2I 5.2 (file interface, sequential access, access modes, standard streams), 3.2 (serialisation,
first look), Annex A (strings `strlen`/`strcpy`/`strcat`, `struct`, `typedef`, `->`, `fopen`/`fclose`/
`fscanf`/`fprintf`, `atoi`, initialisers, designated initialisers, `argc`/`argv`).

Hook: a twelve-letter name copied into a ten-byte array changes the age stored next to it.

Sections:
1. *Null-terminated strings* --- a string is an array of `char` ending in `'\0'`; `strlen` is linear;
   `strcpy`, `strcat` and the buffer overflow (staged, ASan); bounded copies (`snprintf`); string literals are
   read-only; command-line arguments (`argc`, `argv`), `atoi` vs `strtol`.
2. *Structures, unions and enumerations* --- `struct` and `typedef`; designated initialisers; `.` and `->`;
   passing a structure by value or by pointer; `enum` as named constants; a tagged union (a shape: circle or
   rectangle) and why the tag must be checked (Year 2's sum types point back here).
3. *Layout and alignment* --- `sizeof` and `offsetof`; alignment requirements; padding; reordering fields;
   arrays of structures.
4. *Text files and binary files* --- streams, `fopen` modes, `fprintf`/`fscanf`/`fgets`; `fwrite`/`fread`;
   the same numbers as text and as bytes (`od -A d -t x1`); byte order (little-endian here); file position and
   sequential access; closing and checking errors.
5. *Reading input robustly* --- `scanf`'s traps; `fgets` + `strtol` with every error checked; the standard
   streams `stdin`, `stdout`, `stderr` and why errors go to `stderr`; reading the town's CSV.

Owns: null-terminated string, buffer overflow, structure (C `struct`), union, tagged union, enumeration,
alignment, padding, stream, standard streams, text file, binary file, byte order (little-endian, big-endian),
file position. Recalls: text file and records (Book 1 g8), character codes and UTF-8 (Book 2 g10).
Contested: *byte order* (Book 4 `sockets` uses it; earliest need is here; see report).

Listings: `strlen_demo.c`; `overflow.c` (staged ASan); `safe_copy.c`; `args.c` (`args=` directive);
`point.c`; `shapes.c` (tagged union); `layout.c` (`sizeof`/`offsetof`, two field orders); `write_text.c`,
`write_binary.c`, `bytes.sh` (session: run both, `ls -l` sizes with `fixtimes`, `od` dumps); `read_numbers.c` +
`.stdin` (with bad lines); `weather_csv.c` (reads `data/town/weather.csv` passed by `args=`: counts rows,
missing values, the −99.0 error codes). Tests: `tests/safe_copy_test.c`, `tests/parse_test.c`,
`tests/record_io_test.c`.

Figures: (S1) a string in memory with `'\0'`, and an overflow into the neighbouring field; (S2) `bytefield`
layout of a structure with padding bytes, before and after reordering; (S3) a tagged union: tag + shared
storage; (S4) the same three numbers as a text file (bytes of digits and newlines) and as a binary file
(little-endian words).

Exercises: 1★[P] `strlen` and `sizeof` of a literal and an array; 2★[P] `sizeof` of two structures; 3★[P] what
`fscanf` returns on a bad line; 4★[P] bytes of `0x12345678` as written by `fwrite` here; 5★★[F] `strcat` into a
too-small buffer; 6★★[F] a loop `while (!feof(f))` that processes the last line twice; 7★★[W] a bounded
`str_append(char *dst, size_t cap, const char *src)` that reports truncation; 8★★[W] a function reading
`key=value` lines into an array of structures; 9★★[R] minimum size of a structure with given fields over all
orders, with proof (sort by decreasing alignment); 10★★★[W] portable serialisation of a record byte by byte
(independent of byte order), round-trip tested; 11★★★[R] number of bytes `strcat` reads and writes when building
an n-word sentence word by word (quadratic), and the linear fix; 12★★★[W] a robust `read_int` that rejects
overflow, trailing garbage and empty input (tested on a table of cases).

Weekend problem --- *A binary file for the weather station* (24 q.): the town's 731 daily readings stored as
records. Part I designing the record (`struct` with date, station, temperature, rain, wind), its size and
padding; Part II writing and reading text vs binary (file sizes computed then checked); Part III byte order and
a portable format; Part IV robust reading of the CSV (missing values, error codes, the duplicated day). Named
result: *the size of the archive* --- text, padded binary and packed portable sizes in bytes, computed by
formula and equal to the files written.

Ledger: `b1:c-fopen-modes` (C17 7.21.5.3); `b1:x86-little-endian` (x86-64 is little-endian; Intel SDM vol. 1 or
psABI); `b1:strtol` (C17 7.22.1.4); `b1:snprintf` (C17 7.21.6.5); `b1:ascii-nul` (NUL is code 0; shared with
Book 2's ASCII row if any).

## 7 `c-modules-make-tests` --- Modular Programs, Makefiles and Tests (~15 pp)

Programme: MP2I 1.1 (interface vs implementation files), 1.2 (assertions, defensive programming), 1.3 (test
sets, partitions, boundary tests, control-flow graph, coverage, exhaustive testing of a condition), Annex A
(include guards, separate compilation, `assert`).

Hook: a 600-line program in one file; one change, two minutes of rebuilding, and nobody dares touch it.

Sections:
1. *Headers and implementation files* --- the interface in the header, the implementation in the `.c`; include
   guards; `static` helpers; an opaque type (`ratio.h` declares `struct ratio`, only `ratio.c` defines it; a
   constructor and a destructor); changing the implementation without touching users (recall Book 2 g11
   modules).
2. *Separate compilation and make* --- the dependency graph of a program (object files on sources and headers);
   a Makefile: targets, prerequisites, recipes, variables, pattern rules, phony targets; make rebuilds only what
   is older than its prerequisites (session: `touch ratio.c; make`); automatic header dependencies (told,
   `-MMD`).
3. *Unit tests in C* --- a test file per module built with `-Werror`; a tiny check macro that counts failures;
   a failing test as a bug report; the test written before the fix.
4. *Designing tests* --- partition of the input domain, boundary values; the control-flow graph of a function;
   statement coverage and branch coverage; feasible paths; a compound condition tested in all its combinations;
   coverage measured with `gcc --coverage` and `gcov -b` (captured).
5. *Assertions, defensive programming and the debugger* --- `assert` for what must be true, error returns for
   what may fail; `NDEBUG`; a debugger session (breakpoint, step, print, backtrace) described in prose and in a
   schematic (no debugger is installed on the writing machine; see report); `-g` with an ASan backtrace as the
   always-available "where did it crash".

Owns: header file, include guard, interface and implementation (of a module), opaque type, separate compilation,
makefile, target (of a rule), prerequisite, recipe, unit test, test suite, input class, boundary value,
control-flow graph, statement coverage, branch coverage, path coverage, defensive programming, debugger,
breakpoint. Re-founds: assertion (Book 2 g10 `specifications-and-tests`; one definition here). Recalls:
module and interface (Book 2 g11), specification and test (Book 2 g10).
Contested: control-flow graph and coverage (Book 5; see report).

Listings: `ratio.h`, `ratio.c` (NORUN), `ratio_demo.c`; `Makefile` (printed, `akefile` language);
`make.sh` (session, no `fixtimes`: `make`, `make` again (nothing to do), `touch ratio.c`, `make`, `make clean`);
`check.h` (the test macro); `ratio_test.c` (also under `tests/`); `classify.c` (a triangle classifier with a
compound condition) + `coverage.sh` (session: `gcc --coverage`, run three tests, `gcov -b`, then all tests,
`gcov -b` again); `assert_demo.c` (staged failed assertion, `exit`); `crash.c` + `backtrace.sh` (ASan backtrace
with `-g`). Tests: `tests/ratio_test.c` (`// test-with: ../listings/ratio.c`), `tests/classify_test.c`.

Figures: (S1) a program's module graph: headers, sources, objects, executable (the Makefile's dependency
graph); (S2) make's decision on one target after `touch` (timestamps compared, rebuilt nodes shaded); (S3) the
control-flow graph of `classify` with the paths of three tests drawn (statement vs branch coverage);
(S4) a debugger session as a timeline: breakpoint, step, inspect, backtrace (generic terminal drawn, no product).

Exercises: 1★[P] which files make rebuilds after editing a header; 2★[P] does a test set reach full statement
coverage; 3★[P] output of a failed `assert`; 4★[P] what an include guard prevents; 5★★[F] a Makefile rule
missing a header prerequisite (stale build); 6★★[F] a test that always passes (wrong comparison); 7★★[W] an
opaque `stack` module (header + implementation + tests); 8★★[W] tests reaching branch coverage of a given
function; 9★★[R] number of tests needed to cover every combination of a condition with k atomic conditions
(2^k) vs MC/DC-style (k+1, told); 10★★★[R] the minimum number of rebuild steps after editing one header in a
given dependency graph (reachability, counted); 11★★★[W] a Makefile with pattern rules and automatic
dependencies for a three-module program; 12★★★[R] prove that branch coverage implies statement coverage for a
function whose every statement lies on some path, and give a counter-example to the converse.

Weekend problem --- *Taming a one-file program* (24 q.): the town library's loan checker, 300 lines in one file.
Part I splitting into modules and an opaque type; Part II the Makefile and the rebuilds it saves (counted);
Part III a test suite designed by partitions and boundaries, coverage measured; Part IV defensive checks and a
bug found by a test. Named result: *the rebuild saving* --- after an edit to each file in turn, the number of
compiler runs make performs vs a full rebuild, totalled over all edits.

Ledger: `b1:make-origin` (make, Stuart Feldman, Bell Labs, 1976; Feldman 1979 paper); `b1:gcov` (GCC 11 gcov
`-b`); `b1:gcc-mmd` (`-MMD`, GCC 11 manual); `b1:ndebug` (C17 7.2 `assert` and `NDEBUG`).

# Part II --- Tools

## 8 `the-shell` --- The Shell (~14 pp)

Programme: MP2I 5.2 (access rights and attributes, standard streams, redirections, pipes, links, hierarchical
namespace, mounting removable media); L1-UPC (bash syntax, manual, file system, rights, special characters,
expansion, quoting, processes and signals, streams, redirections, pipes, filters, scripts, `find`, `sed`);
L1-AVI (Unix commands, shell programming).

Hook: count, in one line, how many loans each library member made last year.

Sections:
1. *Commands, processes and exit status* --- a command line is a program and its arguments; the shell starts a
   process (recalled Book 2 g12); the exit status and `$?`, `&&`, `||`; environment variables and inheritance
   (a tiny C program printing `argv` and `getenv`); `man` and `--help`; Ctrl-C sends a signal (signals are the
   Year 2 volume's).
2. *Redirection and pipes* --- `>`, `>>`, `<`, `2>`, `2>&1`; pipes and pipelines; filters (`sort`, `uniq -c`,
   `wc`, `head`, `tail`, `cut`, `tr`, `paste`); a pipeline over the town's CSV files answered and checked
   against a Python computation.
3. *Patterns: globs and regular expressions in practice* --- pathname expansion; quoting rules (single,
   double, backslash) and word splitting; `grep -E`, `sed` substitution, `find`; regular expressions used as
   tool syntax, with the exact theory left to the Year 2 volume.
4. *Shell scripts* --- shebang, variables, `"$1"` and `"$@"`, `if`, `for`, `while`, functions, `set -euo
   pipefail`, exit codes as results; a script that checks every CSV of the town for a header and a row count.
5. *Permissions and links* --- users, groups, `rwx` bits, `chmod` in symbolic and octal form, `umask`;
   hard links and symbolic links (`ln`, `ln -s`, `ls -li`): two names for one file vs a file that names
   another; what removing each does; mounting a removable drive (told: it needs administrator rights).

Owns: command-line argument, exit status, environment variable, redirection, pipe, pipeline, filter (shell),
pathname expansion (glob), quoting, shell script, permission bits, hard link, symbolic link. Re-founds: shell
(Book 2 g11 `os-and-command-line`). Recalls: kernel, shell, permissions, file-system tree, paths (Book 2 g11,
Book 1 g3), process (Book 2 g12). Uses without defining: regular expression (Book 4), inode, signal, file
descriptor (Book 4).

Listings (all `.sh` sessions unless noted; the town files are copied in with the directive requested in the
report, else read through a path variable): `status.sh`; `env_child.c` + `env.sh`; `redirect.sh`; `loans.sh`
(the hook's pipeline); `loans_check.py` (the same answer in Python; a test compares both); `globs.sh` (with
`fixtimes`); `quoting.sh`; `grep_sed.sh`; `find.sh`; `check_csv.sh` (a script, run on the town files);
`perms.sh` (`fixtimes`, `ls -l` modes, `chmod`, a refused write staged); `links.sh` (`ls -li`, link counts, a
dangling symbolic link). Tests: `tests/test_pipeline.py` (shell pipeline output = Python answer).

Figures: (S1) a pipeline as processes joined by pipes, with stdin/stdout/stderr of each; (S2) the three standard
streams and what `2>&1` changes (before/after, file descriptors drawn as numbered sockets, named in prose only);
(S3) the expansion order of a command line (braces, variables, words, globs, quotes removed); (S4) hard link vs
symbolic link: two directory entries to one file, one entry naming a path; (S5) the permission bits as a
`bytefield` (type, user, group, others). Photograph: a DEC VT100 terminal (Commons) in a `history` box on
terminals and the first shells.

Exercises: 1★[P] exit status of four command lines; 2★[P] what a glob expands to in a given directory; 3★[P]
output of a pipeline on a small file; 4★[P] permissions printed by `ls -l` after `chmod 640`; 5★★[F] a script
breaking on a file name with a space (quoting); 6★★[F] `cmd > out 2>&1` vs `cmd 2>&1 > out`; 7★★[W] a script
`topk.sh FILE COL K` printing the k most frequent values of a column (tested on the town); 8★★[W] a pipeline
answering a question on the weather table (the hottest day per station); 9★★[R] count the octal modes that
let the owner read but nobody else write (counted); 10★★★[W] a script that finds duplicate files by content
(size then checksum) in a tree; 11★★★[R] after `ln a b; ln -s a c; rm a`, what each of `b` and `c` gives, and
the link counts at each step, justified; 12★★★[R] the number of words a command line splits into, for a given
set of quoting cases, justified by the expansion rules.

Weekend problem --- *A day's log in one line* (24 q.): the library's generated access log (a seeded generator in
the chapter's code). Part I filters and counts; Part II patterns: dates, member ids, error lines; Part III a
script with arguments, exit codes and tests; Part IV the pipeline checked against a Python program. Named
result: *the pipeline theorem of the log* --- the busiest hour and the number of distinct members, computed by a
single pipeline and equal to the Python reference.

Ledger: `b1:unix-shell-history` (Thompson shell 1971, Bourne shell 1979, bash 1989; primary pages: Bell Labs
Unix manuals / GNU bash page); `b1:vt100` (DEC VT100, 1978; museum page); `b1:posix-shell` (POSIX.1 Shell and
Utilities, The Open Group page; expansion order); `b1:bash-version` (`dated{2026}` only if a version is printed).

## 9 `version-control` --- Version Control with Git (~14 pp)

Programme: licence tools (outline's choice; no fetched L1 list names Git); MP2I 1.3 (tests as a development
habit, used by `bisect`).

Hook: yesterday's program worked; today's does not; forty edits happened in between.

Sections:
1. *Snapshots and commits* --- a repository; `init`, `add`, `commit`, `log`, `show`; a commit is a snapshot plus
   metadata and parent(s); object identifiers are hashes of content (told; the hash function itself is Book 5's),
   `git cat-file -p` on a commit and a tree.
2. *The staging area* --- working tree, index, repository; `status`, `diff`, `diff --staged`; staging part of
   a change; `restore` explained in prose (the tool is used inside the captured session only).
3. *Branches and merges* --- a branch is a movable name for a commit; `switch -c`; fast-forward vs three-way
   merge; the merge base; the commit graph is acyclic (`log --graph --oneline`); rebase (told).
4. *Conflicts and remotes* --- a staged conflict, its markers, its resolution; a bare repository on the same
   disk as the remote: `clone`, `push`, `fetch`, `pull`; nothing leaves the machine.
5. *Searching history* --- `log -S`, `blame`; `bisect run` with a test script finds the commit that broke a
   test; what a good commit is (one change, tests pass, a message that says why).

Owns: version control system, repository, commit, snapshot, working tree, staging area (index), branch,
fast-forward merge, three-way merge, merge base, merge conflict, remote repository, clone, bisection (of
history). Recalls: file, folder, path (Book 1 g3), test (Book 2 g10). Uses informally: graph, acyclic (defined in
ch. 24; a forward pointer).

Listings (sessions; identity Ada Lovelace and the fixed date of `capture_output.py`; `git init -b main`):
`first_commits.sh`; `objects.sh` (`cat-file`); `staging.sh`; `branches.sh` (fast-forward then three-way,
`log --graph`); `conflict.sh` (staged conflict and its resolution); `remote.sh` (bare repository, clone, push,
pull); `bisect.sh` (a generated 64-commit history via `make_history.py`, `bisect run ./test.sh`);
`make_history.py` (NORUN if only imported; else run inside the session); `history_search.sh` (`log -S`,
`blame`). Tests: `tests/test_history.py` (the generated history has exactly one bad commit at the stated
position).

Figures: (S1) working tree, staging area and repository with the commands moving changes between them;
(S2) commit graph with two branches, the merge base, a fast-forward and a merge commit (as `log --graph`
shows it, drawn); (S3) a conflict: base, ours, theirs and the marked file; (S4) bisection over 64 commits: the
interval halving at each test. AI: a team of three at a shared table with laptops (no screens readable), in
the section on remotes.

Exercises: 1★[P] `status` after a sequence of edits and adds; 2★[P] which commits a branch contains; 3★[P]
does a merge fast-forward; 4★[P] what `diff --staged` shows; 5★★[F] a commit that mixes two changes, split
(session solution); 6★★[F] a conflict resolved by keeping the markers; 7★★[W] a `test.sh` for `bisect run`
(exit 0, 1, 125 meanings); 8★★[R] the merge base of two commits in a drawn graph; 9★★[P] the graph after two
merges; 10★★★[R] bisection over n commits of linear history needs at most ⌈log₂ n⌉ tests, proved, given that
good precedes bad; 11★★★[R] in a history with merges, show that bisection still terminates and count the worst
case on a drawn example; 12★★★[W] a script that lists, for each file, the number of commits that touched it,
on a generated repository.

Weekend problem --- *Who broke the catalogue?* (24 q.): the generated history of a small catalogue program
(64 commits, two branches, one merge). Part I reading the graph (commits, merges, ancestors); Part II merge
bases and what a merge brings; Part III bisection by hand then by `bisect run`; Part IV the logarithmic bound
proved. Named result: *bisection finds the culprit among 64 commits in at most 6 tests* (and the captured run
took the printed number).

Ledger: `b1:git-origin` (Git, 2005; git-scm.com book "A Short History of Git"); `b1:git-object-ids` (SHA-1 object
names, SHA-256 transition; git docs `hash-function-transition`); `b1:git-bisect` (git-bisect docs: exit code
125 skips); `b1:git-version` (`dated{2026}`, git 2.55 if printed).

# Part III --- Reasoning about programs

## 10 `propositional-logic` --- Propositional Logic (~15 pp)

Programme: MP2I 6.1 (variables, connectives, arity, formulas by induction, trees, subformula, size, height),
6.2 (valuations, satisfiability, model, tautology, antilogy, equivalence, De Morgan, consequence, CNF, DNF,
normalisation, exponential blow-up, SAT, n-SAT, Quine's algorithm, modelling); L1-AVI (truth tables).

Hook: four friends, three rules about who sits next to whom: can everyone be happy?

Sections:
1. *Formulas as trees* --- propositional variables, connectives (¬, ∧, ∨, →, ↔) and their arities; formulas
   defined inductively; the tree of a formula; subformula, size and height (functions defined by induction,
   forward pointer to ch. 11 for the proofs); formulas as Python data; printing with the needed parentheses.
2. *Valuations and truth* --- valuation, truth value by induction on the formula; truth tables recalled from the
   mathematics book (Year 1); model, satisfiable, tautology, antilogy; consequence Γ ⊨ φ.
3. *Equivalence and normal forms* --- logical equivalence; the laws (De Morgan, distributivity, excluded middle,
   implication rewritten); literals, clauses; negation normal form, CNF, DNF; the complete DNF read off a truth
   table; a formula whose CNF has 2^n clauses (proved), and Tseitin's encoding as the way out (in the problem).
4. *Satisfiability* --- the SAT problem, k-SAT; brute force over 2^n valuations; Quine's algorithm (split on a
   variable, simplify, recurse) and unit propagation; nodes explored counted; correctness proved by induction
   on the number of variables.
5. *Modelling with formulas* --- a puzzle encoded; graph colouring as SAT (the town's friendship graph in three
   colours); reading a model back as a solution.

Owns: propositional variable, connective, propositional formula, subformula, size of a formula, height of a
formula, valuation, truth value, model, satisfiable formula, tautology, antilogy, logical equivalence, logical
consequence, literal, clause, negation normal form, conjunctive normal form, disjunctive normal form,
satisfiability problem (SAT), k-SAT, Quine's algorithm (method, indexed), unit propagation. Re-founds:
propositional logic (Book 1 g9 `logic-gates` owns gates only). Recalls: truth tables, statements (mathematics
Year 1), Boolean operations (Book 1 g9).

Listings: `formula.py` (dataclasses; prints example formulas and their trees); `evaluate.py`;
`truth_table.py`; `normal_forms.py` (NNF, CNF by distribution, DNF); `blowup.py` (clause counts for n = 1..10);
`quine.py` (with node counter); `colouring.py` (3-colouring of the town friendships: model found, checked);
`puzzle.py`. Tests: `tests/test_formula.py` (evaluation vs truth tables, hypothesis over random formulas:
NNF/CNF equivalent to the original on all valuations), `tests/test_quine.py` (agrees with brute force on random
3-CNF).

Figures: (S1) the tree of `(p → q) ∧ ¬(q ∨ r)` with size and height marked; (S2) the truth table of a formula with
its complete DNF read from the true rows; (S3) Quine's search tree on a small CNF, pruned branches shown;
(S4) the friendship graph coloured from the model.

Exercises: 1★[P] truth value under a valuation; 2★[P] size and height of a formula; 3★[P] which of four formulas
are tautologies; 4★[P] output of `normal_forms.py` on a formula; 5★★[F] an evaluator that mishandles `→`;
6★★[F] a CNF converter that forgets to distribute over a nested ∧; 7★★[W] `is_consequence(gamma, phi)` by
brute force; 8★★[W] an encoder of "exactly one of x1..xn" in CNF (pairwise), tested; 9★★[R] count the clauses
of the pairwise encoding (n(n−1)/2 + 1); 10★★★[R] prove that every formula is equivalent to one using only ¬ and
∧ (structural induction, forward to ch. 11's principle); 11★★★[W] a solver with unit propagation counting
nodes; compare with plain splitting on given CNFs; 12★★★[R] prove that a formula is a tautology iff its
negation is unsatisfiable, and that Quine's algorithm is correct.

Weekend problem --- *Seating the committee* (24 q.): seven committee members, seating constraints. Part I the
encoding (variables, clauses, counts); Part II normal forms and the blow-up of a naive CNF; Part III Tseitin's
encoding: a new variable per gate, three clauses per binary gate, equisatisfiability proved; Part IV solving with
Quine's algorithm, nodes counted, the seating read back. Named result: *Tseitin's theorem* --- every formula of
size m has an equisatisfiable CNF with at most 3m clauses, proved, and the committee's CNF counted.

Ledger: `b1:tseitin` (Tseitin 1968, "On the complexity of derivation in propositional calculus"; bibliographic
row only if the year is printed); `b1:quine` (Quine, *Methods of Logic*, 1950, if dated). Few rows: definitions
and theorems need none.

## 11 `induction-and-termination` --- Induction, Recursion and Termination (~14 pp)

Programme: MP2I 2 (ordered sets, predecessors/successors, minimal element, product and lexicographic orders,
well-founded order, inductive sets, induced order, structural induction), 3.3 (binary tree defined inductively,
vocabulary, height −1, arbitrary trees converted to binary trees), 1.1 (termination, variant).

Hook: a function that reverses a list twice; can you be sure you get the list back, for every list?

Sections:
1. *Inductively defined sets* --- the smallest set closed under rules; natural numbers, lists, binary trees,
   formulas (ch. 10); binary tree vocabulary re-founded: root, leaf, internal node, subtree, depth, size, height
   (empty tree −1); Python representations.
2. *Structural induction* --- the principle, proved from ordinary induction (recalled from the mathematics book)
   on the height; examples: `len(xs + ys)`, `reverse(reverse(xs)) = xs`, size ≤ 2^{h+1} − 1, leaves = internal
   nodes + 1 in full binary trees; the induced order.
3. *Well-founded orders* --- orders recalled from the mathematics book; strict order, minimal element,
   immediate predecessor; well-founded ⇔ no infinite descending chain ⇔ every non-empty subset has a minimal
   element (proved); product order and lexicographic order are well-founded (proved); the link with reachability
   in a directed acyclic graph (forward pointer to ch. 24).
4. *Termination by a variant* --- a variant maps states into a well-founded set and strictly decreases;
   Euclid's algorithm (recalled), a loop with a lexicographic variant, Ackermann's function terminates (lexicographic
   induction) though it grows fast (small values only, call counts).
5. *Recursive functions proved correct* --- merge of sorted lists (correctness and termination); mirror of a
   tree; converting a tree of any arity to a binary tree (left child, right sibling) and back, proved inverse;
   mutual recursion (ch. 3) proved terminating by a common variant.

Owns: inductively defined set, binary tree, root, leaf, internal node, subtree, depth (of a node), size (of a
tree), height (of a tree), full binary tree, structural induction, strict order, minimal element, immediate
predecessor, well-founded order, product order, lexicographic order, variant (termination measure),
termination, left-child right-sibling representation. Re-founds: termination, variant (Book 2 g11), binary tree
vocabulary (Book 2 g12 `trees`), recursion proved by induction (Book 2 g12). Recalls: proof by induction, order
relation (mathematics), recursion (Book 2 g12).

Listings: `inductive.py` (lists and trees as dataclasses, size/height/leaves); `tree_bounds.py` (random trees
checking size ≤ 2^{h+1} − 1 and leaves = internal + 1 on full trees); `reverse_twice.py`; `lex_loop.py` (a loop
with a lexicographic variant printing the variant at each step); `ackermann.py` (call counts for m ≤ 3, n ≤ 4);
`merge.py`; `lcrs.py` (arbitrary tree ↔ binary tree); `even_odd.py`. Tests (hypothesis): `tests/test_trees.py`,
`tests/test_merge.py`, `tests/test_lcrs.py` (round trip), `tests/test_game.py` (problem).

Figures: (S1) the rules generating binary trees and the first trees of height ≤ 2; (S2) a full binary tree with
leaves and internal nodes counted, and the induction step drawn; (S3) the lexicographic order on ℕ² as a grid
with a descending chain that must stop; (S4) a tree of arity 4 and its left-child right-sibling binary tree.

Exercises: 1★[P] size and height of four trees (with the empty tree); 2★[P] variant values along a run;
3★[P] output of `lcrs.py` on a small tree; 4★[P] is a given order well-founded; 5★★[F] a recursive function whose
"variant" does not decrease on one branch; 6★★[F] a height function returning 0 for the empty tree, with the
bound that then fails; 7★★[W] `count_paths(tree)` (root-to-leaf paths) with a structural-induction argument for
its value on full trees; 8★★[R] prove `len(flatten(t)) = size(t)` by structural induction; 9★★[R] a binary tree
of height h has at most 2^h leaves; 10★★★[R] prove the lexicographic order on finite words over a finite
alphabet (shorter first, then dictionary) is well-founded, and the dictionary order alone is not;
11★★★[W] a terminating "list-sorting game" with a proved variant; 12★★★[R] prove McCarthy's 91 function
returns 91 for every n ≤ 100 (well-founded induction on 101 − n).

Weekend problem --- *The game that always ends* (24 q.): a list of natural numbers; a move replaces some k > 0 by
two copies of k − 1. Part I the game as data and plays as sequences (inductive definitions); Part II termination
by the multiset of values (well-founded order, proved); Part III the length of a play by structural reasoning on
a single k (`M(k) = 1 + 2M(k−1)`), counted by program; Part IV the potential Σ(2^{a_i} − 1) decreases by exactly
one at each move. Named result: *every play from (a_1, ..., a_n) has the same length Σ(2^{a_i} − 1)*, proved and
checked by exhaustive search on small lists.

Ledger: `b1:ackermann` (Ackermann 1928, Math. Annalen; only if dated); `b1:mccarthy91` (McCarthy 91 function,
Manna & McCarthy 1970; only if named with a date). Mostly none.

## 12 `program-correctness` --- Program Correctness (~14 pp)

Programme: MP2I 1.1 (partial/total correctness, variant, invariant), 1.2 (specification, signatures,
pre/postconditions and invariants as annotations), 1.3 (tests from the specification); 4.3 (binary search).

Hook: a binary search printed in a famous textbook that failed for very large arrays (told without a date
unless the ledger has it).

Sections:
1. *Specifications* --- precondition, postcondition, the specification as a pair; states and assertions about
   them; signatures and contracts written in docstrings and checked by `assert` (re-found of Book 2 g10).
2. *Partial and total correctness* --- definitions; a partially correct program that does not always stop;
   total = partial + termination (ch. 11's variants).
3. *Loop invariants found systematically* --- the method: from the postcondition, replace a constant by a
   variable, or drop a conjunct; the three obligations (initialisation, preservation, conclusion) plus a variant;
   examples: sum, maximum, integer division by repeated subtraction.
4. *Proofs for array algorithms* --- partition around a pivot (Lomuto), with its invariant drawn; binary search
   on a half-open interval with every boundary case (empty array, absent key, first/last element, duplicates:
   leftmost occurrence), and the midpoint overflow in C recalled (ch. 2); the three-colour flag with four
   regions.
5. *Testing against the specification* --- the postcondition as a test oracle; property-based tests
   (hypothesis) derived from the specification; a brute-force oracle; what tests can and cannot prove.

Owns: precondition, postcondition, specification (pair), partial
correctness, total correctness, loop invariant, invariant method (method, indexed), three-colour flag problem
(named), half-open interval, test oracle, property-based test. Re-founds: invariant (Book 2 g11), precondition
and postcondition (Book 2 g10). Recalls: termination and variants (ch. 11), assertion (ch. 7), binary search
and selection sort (Book 1 g8, Book 2 g11).
Avoids: Hoare triple and its proof rules (Book 5 `program-verification`); the triple is written in words.

Listings: `contracts.py` (pre/post asserts); `sum_max.py`; `slow_division.py`; `partition.py` (with invariant
check helper); `bsearch.py` (leftmost/rightmost on `[lo, hi)`); `bsearch_bug.py` (staged infinite loop on two
elements, `timeout=3` and a step cap printing the stuck state); `flag.py`; `check_invariant.py` (runs a loop
asserting its invariant at each turn); `isqrt.py` (problem). Tests: `tests/test_bsearch.py` (hypothesis vs
`bisect`), `tests/test_partition.py`, `tests/test_flag.py`, `tests/test_isqrt.py`.

Figures: (S1) partial vs total correctness as a diagram of runs (stops-and-right, never-stops); (S2) the
invariant of Lomuto's partition: regions `< p`, `≥ p`, unknown, with indices; (S3) binary search on `[lo, hi)`:
the invariant picture and the five boundary cases; (S4) the three-colour flag's four regions and the three cases
of a step.

Exercises: 1★[P] which of four specifications a function meets; 2★[P] the invariant's values along a run;
3★[P] does a loop terminate; 4★[P] output of `bsearch.py` on duplicates; 5★★[F] `while lo <= hi` with `hi = mid`
(the staged infinite loop), fixed with its proof; 6★★[F] a partition that loses an element; 7★★[W] rightmost
occurrence with a stated invariant; 8★★[R] prove the maximum loop correct; 9★★[R] number of iterations of
binary search on n elements (⌊log₂ n⌋ + 1 at most), proved; 10★★★[W] the three-colour flag in a single pass with
the minimal number of swaps for a given input, tested; 11★★★[R] find and prove an invariant for a given
mystery loop (fast exponentiation by squaring); 12★★★[R] a "proof" with a flawed invariant: find the flaw.

Weekend problem --- *The square root that never lies* (24 q.): integer square root of a 64-bit number. Part I the
specification `r² ≤ n < (r+1)²`; Part II bisection on `[0, n+1)` with invariant and variant, iterations counted;
Part III Newton's method on integers, decreasing variant, invariant `r ≥ ⌊√n⌋`; Part IV both tested against
`math.isqrt` (hypothesis) and the iteration counts compared. Named result: *Newton's integer square root is
totally correct*, proved, with its measured iteration count against bisection's ⌈log₂(n+1)⌉ for the tested
inputs.

Ledger: `b1:bsearch-bug` (the overflow in a widely used binary search, J. Bloch, Google Research blog, 2006;
only if told with name or date); `b1:dutch-flag` (Dijkstra, *A Discipline of Programming*, 1976, if dated).

## 13 `asymptotic-analysis` --- Asymptotic Analysis and Recurrences (~15 pp)

Programme: MP2I 1.1 (complexity, worst case, average case), 2 (usual recurrences); L1 discrete-mathematics
companions. Comparison of sequences is the mathematics book's (Year 1); recall, then build.

Hook: two programs that both "work", one finishing in a second and the other in a week on the same input.

Sections:
1. *What the model counts* --- the RAM model: elementary operations of unit cost on machine words, input size;
   counting by instrumenting a program; why constants are dropped; what the model hides (memory hierarchy,
   Year 2).
2. *O, Ω and Θ* --- definitions for cost functions ℕ → ℝ₊ (eventually); properties (sum, product, transitivity,
   max); the scale log n ≪ n^a ≪ b^n ≪ n!, proved via limits recalled from the mathematics book; pitfalls (O is
   an upper bound only).
3. *Worst, best and average case* --- insertion sort: comparisons in the best and worst case; average over all n!
   orders of distinct keys equals n(n−1)/4 + O(n), counted through inversions (a counting argument, not
   probability); space cost.
4. *Sums* --- arithmetic and geometric sums; nested loops; the harmonic number H_n ∈ Θ(log n) by comparison
   with an integral (recalled); bounding by splitting (half the terms are ≥ the middle one).
5. *Recurrences* --- unrolling; the recursion tree; guess and prove by induction; the master theorem stated and
   proved for n a power of b, with floors and ceilings in a remark; the three cases on examples (binary search,
   merge sort, Karatsuba, Strassen as numbers only).

Owns: model of computation (RAM model), elementary operation, input size, cost function, big O, big Omega, big
Theta, worst-case cost, best-case cost, average-case cost, space cost, recurrence relation, recursion tree,
master theorem (indexed in its theorem). Re-founds: cost of an algorithm (Book 2 g11). Recalls: comparison of
sequences, logarithm, sums, integrals (mathematics), insertion sort (Book 1 g8).

Listings: `count_ops.py` (instrumented insertion sort, counts for best/worst/random); `inversions.py` (average
comparisons over all permutations for n ≤ 8, exact fractions); `growth.py` (table of n, n log n, n², 2^n);
`doubling.py` (comparison counts of three algorithms as n doubles; deterministic); `timing.py` (MEASURED: the
same three timed, ratios); `recurrences.py` (exact T(n) vs closed forms); `master.py` (classifies a recurrence and
checks numerically). Tests: `tests/test_counts.py`, `tests/test_recurrences.py`.

Figures: (S1) chart of growth curves on log axes from `growth.dat` (pgfplots, `figures/growth.py`); (S2) the
recursion tree of T(n) = 2T(n/2) + n with level sums; (S3) the three regimes of the master theorem as recursion
trees (cost at leaves, even, at root); (S4) measured times vs counts (chart from MEASURED data).

Exercises: 1★[P] counts printed by an instrumented loop; 2★[P] order four functions by growth; 3★[P] the value of
T(16) for a given recurrence; 4★[P] which case of the master theorem applies; 5★★[F] a "proof" that n² ∈ O(n) by
induction with a moving constant; 6★★[F] a cost count that forgets the inner loop's dependence on i; 7★★[W] an
instrumented counter for a nested loop; check the closed form; 8★★[R] Σ_{i=1}^{n} i log i ∈ Θ(n² log n);
9★★[R] solve T(n) = T(n−1) + n and T(n) = 2T(n−1) + 1 exactly; 10★★★[R] prove the master theorem's case
a = b^k; 11★★★[R] T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + n with floors: Θ(n log n), proved; 12★★★[W] a program solving
recurrences of the form T(n) = aT(n/b) + n^k numerically and identifying the case, tested.

Weekend problem --- *Three ways to find a duplicate* (24 q.): in a list of n numbers drawn from the town's
loans. Part I the quadratic double loop, counted exactly; Part II sort then scan (merge sort's count recalled
forward from ch. 19 by formula), Θ(n log n) proved; Part III a set of seen values, cost under the model's
assumptions; Part IV the doubling ratio of the counts. Named result: *the doubling ratio test* --- the counts'
ratios as n doubles tend to 4, 2·(1 + 1/log₂ n) and 2, which identifies Θ(n²), Θ(n log n) and Θ(n), proved and
read from the program's table.

Ledger: `b1:master-theorem-attrib` (Bentley, Haken, Saxe 1980, if attributed); otherwise none.

# Part IV --- Data structures

## 14 `dynamic-arrays` --- Dynamic Arrays and Amortised Analysis (~14 pp)

Programme: MP2I 3.1 (abstract data structure: type with operations; constructor, accessor, transformer;
interchangeable implementations), 3.2 (resizing an array), 1.1 (amortised cost).

Hook: Python's `list.append` is fast however long the list; how can a fixed block of memory grow for free?

Sections:
1. *Abstract type and implementation* --- an abstract data type: a set of operations with a specification;
   constructors, accessors, transformers; the interface as a C header; two implementations swapped behind it
   (fixed-capacity array, growing array); re-found of Book 2 g12.
2. *The doubling array* --- size and capacity; `push`, `pop`, `get`, `set`; growth by a factor; shrinking at a
   quarter (not a half); the code with its invariants.
3. *Amortised cost* --- definition; the aggregate method (doubling: total copies < 2n); the accounting method
   (three credits per push); the potential method (Φ = 2·size − capacity, made non-negative); the binary counter
   as the classic second example; the half-shrink policy that costs Θ(n) per operation (counter-example).
4. *The circular buffer* --- a queue in a fixed array with a head index and a count; modular indices; full vs
   empty; growing it (copying in order).
5. *Measurement* --- copy counts (deterministic) and times (MEASURED) for growth factors 1.5, 2 and +16.

Owns: abstract data type, interface (of an abstract type: in-book sense), implementation (of an abstract type),
constructor, accessor, transformer (operations of an ADT), dynamic array, size and capacity (of a dynamic
array), amortised cost, aggregate method, accounting method, potential function (potential method), circular
buffer. Re-founds: abstract data type (Book 2 g12). Recalls: growth factor (ch. 5), module and interface (Book 2
g11).

Listings: `vec.h`, `vec.c` (NORUN, tested); `vec_demo.c` (`with=vec.c`); `fixed.c` (the fixed-capacity
implementation behind the same header) + `swap_impl.sh` (session: the same demo linked with each);
`copies.c`; `counter.c` (binary counter flips); `thrash.c` (half-shrink policy staged: copies explode);
`ring.h`, `ring.c`, `ring_demo.c`; `timing.c` (MEASURED). Tests: `tests/vec_test.c`, `tests/ring_test.c`,
`tests/fixed_test.c` (one test suite run on both implementations through the header).

Figures: (S1) an ADT's interface with two implementations behind it (box diagram); (S2) doubling: size vs
capacity over 17 pushes, copy costs as spikes, the amortised line (chart from `copies.dat`); (S3) the
potential Φ across pushes (sawtooth) with actual + ΔΦ = 3; (S4) a circular buffer with head and tail
wrapping, before and after a wrap.

Exercises: 1★[P] size and capacity after a sequence of operations; 2★[P] copies made for 10 pushes; 3★[P] the
ring buffer's contents after operations; 4★[P] bits flipped by 8 increments; 5★★[F] a ring buffer that cannot
tell full from empty; 6★★[F] a `pop` that shrinks at half and thrashes; 7★★[W] a stack ADT on the dynamic array
(header + tests); 8★★[R] total cost of n increments of a binary counter < 2n (aggregate); 9★★[R] the same by
the accounting method; 10★★★[R] growth factor r: amortised copies per push ≤ r/(r−1), proved by a potential;
11★★★[R] grow ×2 and shrink at ¼: any sequence of m operations costs O(m), proved with an explicit constant;
12★★★[W] a dynamic array of generic elements (`void *` + element size), tested.

Weekend problem --- *The binary counter and the elastic array* (24 q.): Part I the counter: flips per increment,
aggregate bound; Part II the doubling array with three methods; Part III shrinking policies and the thrashing
sequence; Part IV a decrement operation on the counter breaks the bound (n operations, Θ(n log n) flips),
and a redundant representation restores it (told, then counted). Named result: *the elastic array theorem* ---
with growth ×2 and shrink at ¼, m operations make at most c·m element copies, with the smallest c the potential
gives, checked against the worst sequence found by the program.

Ledger: `b1:cpython-list-growth` (CPython's list over-allocation pattern, `listobject.c` comment; only if a
number is printed); `b1:cpp-vector-amortised` (C++ `push_back` amortised constant; cppreference); `b1:tarjan-
amortised` (Tarjan 1985, "Amortized computational complexity", if attributed).

## 15 `linked-structures` --- Linked Structures: Lists, Stacks and Queues (~15 pp)

Programme: MP2I 3.2 (list by array and by linked cells; stack and queue by array and by links; costs by
implementation), 3.1 (abstract structure, interchangeable implementations).

Hook: an editor's undo history where inserting in the middle must not move a million entries.

Sections:
1. *Singly linked lists* --- the cell (`struct node`), push at the front, traversal, insertion after a cell,
   deletion with a pointer to pointer, freeing the whole list; costs; re-found of Book 2 g12.
2. *Doubly linked lists and sentinels* --- previous and next pointers; a circular list with a sentinel removes
   every special case (proved by the invariant "the sentinel's neighbours are the ends"); constant-time removal
   of a known cell.
3. *Stacks, queues and deques* --- each on an array (ch. 14) and on links, behind one header; one test suite
   for both; bracket matching and a postfix evaluator recalled from Book 2 as users.
4. *Iterators* --- an iterator object for a list and for an array (`begin`, `has_next`, `next`); a callback
   alternative; invalidation when the structure changes.
5. *Costs compared, by proof and by measurement* --- the table of costs; traversal of a list vs an array on this
   laptop (MEASURED), the gap explained in one paragraph by locality (the Year 2 volume's caches).

Owns: linked list, cell (node of a linked list), singly linked list, doubly linked list, sentinel, stack, queue,
deque, iterator. Re-founds: linked list, stack, queue (Book 2 g12 `lists-stacks-queues`). Recalls: abstract data
type, dynamic array, circular buffer (ch. 14), pointers and heap (ch. 4--5).

Listings: `list.h`, `list.c` (NORUN, tested); `list_demo.c` (`with=list.c`); `remove_pp.c` (deletion with a
pointer to a pointer, shown next to the special-case version); `dlist.h`, `dlist.c`, `dlist_demo.c`;
`stack.h`, `stack_array.c`, `stack_list.c` + `stack_both.sh` (session: one test suite linked with each);
`queue_list.c`; `deque.c`; `brackets.c`; `iter.c`; `traverse.c` (MEASURED). Tests: `tests/list_test.c`,
`tests/dlist_test.c`, `tests/stack_test.c` (run twice, one per implementation, via two test files with
different `test-with`), `tests/queue_test.c`, `tests/josephus_test.c`.

Figures: (S1) a singly linked list with cells and arrows; insertion after a cell in two steps; (S2) deletion
with a pointer to a pointer (the `next` field being redirected); (S3) a circular doubly linked list with a
sentinel, empty and with three cells; (S4) stack and queue each on an array and on links (four small drawings);
(S5, optional) the traversal chart (MEASURED).

Exercises: 1★[P] the list after a sequence of pushes and deletions; 2★[P] stack and queue contents after
operations; 3★[P] output of the bracket checker; 4★[P] what an iterator yields after a removal; 5★★[F] a
deletion that frees the cell before reading its `next`; 6★★[F] a queue whose `rear` is not updated when it
empties; 7★★[W] reverse a singly linked list in place; 8★★[W] a deque on a circular buffer; 9★★[R] cost of
appending at the end of a singly linked list without a tail pointer, n appends: Θ(n²), and with one: Θ(n);
10★★★[W] detect a cycle in a list with two pointers (Floyd), tested on lists with and without cycles;
11★★★[R] prove that the two-pointer cycle detection terminates within λ + μ steps (tail μ, cycle λ);
12★★★[R] a queue from two stacks: amortised O(1) per operation, proved.

Weekend problem --- *The Josephus circle* (24 q.): n people in a circle, every k-th leaves. Part I simulation with a
circular list, cost Θ(nk); Part II the recurrence J(n, k) = (J(n−1, k) + k) mod n, proved; Part III the closed
form for k = 2 by splitting even and odd n; Part IV the program checks the formula for n ≤ 10⁴. Named result:
*Josephus for k = 2*: J(n) = 2(n − 2^⌊log₂ n⌋) + 1 (1-based), proved and checked.

Ledger: `b1:linked-list-origin` (Newell, Shaw and Simon's IPL, 1955--56, if a history box is written);
`b1:josephus` (Josephus problem attribution, only told without dates unless sourced).

## 16 `hash-tables` --- Hash Tables (~15 pp)

Programme: MP2I 3.2 (associative array implemented by a hash table; hash function construction and collision
methods "not required", taught here because the licence and later books need them).

Hook: a phone directory of a million names: alphabetical order needs twenty looks; can one look be enough?

Sections:
1. *Dictionaries and sets* --- the dictionary ADT (insert, search, delete; keys and values), the set as a
   dictionary without values; implementations so far (sorted array, list) and their costs; re-found of the
   Python dictionary (Book 1 g8, use only).
2. *Hash functions* --- from keys to bucket indices; the division method; a string hash by polynomial evaluation
   (Horner) mod 2^64; FNV-1a (constants from the ledger); what a good hash does.
3. *Chaining* --- buckets as lists; load factor α = n/m; worst case Θ(n); expected cost 1 + α under simple uniform
   hashing (stated; proved in the Year 2 volume); measured chain lengths on the town's names.
4. *Open addressing* --- linear probing; search, insertion, deletion with tombstones; clustering; expected probes
   (stated); a comparison of both designs by counted probes.
5. *Resizing, and inputs that defeat a hash function* --- rehashing when α passes a threshold, amortised O(1)
   (ch. 14); keys chosen against an additive hash (all anagrams collide; strings built to collide under a
   polynomial hash mod 2^64 with an even multiplier); the defence: a seeded hash (told: Python randomises its
   string hash).

Owns: dictionary (abstract type), key (of a dictionary), hash function, hash value, bucket, hash table,
collision, separate chaining, open addressing, linear probing, tombstone, load factor, simple uniform hashing
(assumption), rehashing. Re-founds: dictionary as an abstract type (Book 1 g8 "use only"). Recalls: dynamic
array, amortised cost (ch. 14), linked list (ch. 15), modular arithmetic (mathematics).

Listings: `hash_funcs.c` (division, additive, polynomial, FNV-1a on sample keys); `chain.h`, `chain.c`,
`chain_demo.c`; `probe.h`, `probe.c`, `probe_demo.c`; `chains_town.c` (chain length histogram for the 120 town
names, m = 31, 64, 127); `anagrams.c` (additive hash: k! anagrams in one bucket); `attack.c` (strings colliding
under a weak polynomial hash); `resize.c` (rehash counts); `timing.c` (MEASURED: search time vs load factor).
Tests: `tests/chain_test.c`, `tests/probe_test.c` (with deletions and tombstones), `tests/set_test.c`.

Figures: (S1) keys → hash function → buckets, a collision marked; (S2) chaining with lists of different lengths;
(S3) linear probing with a cluster and a tombstone; (S4) chart: probes per search vs load factor, counted
(chaining and probing) from `figures/probes.py`. AI (optional): a library card-catalogue drawer (generic, no
letters readable), for the hook.

Exercises: 1★[P] bucket of five keys under the division method; 2★[P] the table after inserts with linear
probing; 3★[P] chain lengths for a given hash; 4★[P] load factor after resizing; 5★★[F] deletion in linear
probing that empties the slot and loses later keys; 6★★[F] a hash of strings that ignores characters after the
first; 7★★[W] a set of integers by open addressing with resizing; 8★★[W] word frequencies of a text with the
chaining table, checked against Python's `Counter`; 9★★[R] number of colliding pairs when all n keys fall in one
bucket vs spread evenly over m: n(n−1)/2 vs about n²/(2m); 10★★★[R] with resizing at α > ¾ by doubling,
total rehash work for n inserts is fewer than 2n moves (proved with ch. 14's method); 11★★★[W] build k strings of length
L that collide under `h(s) = Σ s_i 31^{L−1−i} mod 2^{64}` (the "Aa"/"BB" trick), tested; 12★★★[R] prove that
under the additive hash every permutation of a word has the same hash, and count the words of length 4 over
26 letters sharing the most common hash value (counted by program, argued).

Weekend problem --- *Collisions in the town directory* (24 q.): the 120 people of Brenmoor keyed by full name.
Part I four hash functions, bucket histograms; Part II chaining: longest chain, average probes, as m varies;
Part III open addressing and clusters; Part IV an attacker's list of names and the seeded defence. Named result:
*the anagram attack* --- under the additive hash, a set of k distinct letters gives k! keys in one bucket (proved),
and the polynomial hash spreads the same keys over the printed number of buckets.

Ledger: `b1:fnv1a` (FNV-1a 64-bit offset basis and prime; IETF draft `draft-eastlake-fnv` or the authors' page);
`b1:python-siphash` (PEP 456: SipHash for str/bytes since Python 3.4); `b1:python-hash-random` (hash
randomisation, `PYTHONHASHSEED`, Python docs); `b1:cpp-max-load-factor` (`unordered_map::max_load_factor` default
1.0; cppreference); `b1:hash-origin` (Luhn 1953 at IBM, if a history box is written; source needed or dropped).

## 17 `balanced-trees` --- Binary Search Trees and Balanced Trees (~16 pp)

Programme: MP2I 3.3 (associative array by a binary search tree, red-black tree, traversals), 3.2/3.3
(serialisation of a hierarchical structure); outline: AVL with its height proof.

Hook: the library catalogue as a search tree, filled in alphabetical order, becomes a linked list.

Sections:
1. *Binary search trees* --- the search-tree property (re-found of Book 2 g12); search, minimum, successor,
   insertion, deletion (three cases); in-order traversal is sorted (proved by structural induction, ch. 11);
   ordered-dictionary operations (floor, ceiling, range).
2. *Height bounds* --- costs are Θ(h); ⌊log₂ n⌋ ≤ h ≤ n − 1 (proved); degenerate trees from sorted insertions;
   heights measured for sorted vs shuffled insertion of the town's 80 titles.
3. *Rotations* --- left and right rotations preserve the in-order sequence (proved) and change heights locally.
4. *AVL trees* --- balance factor; the minimal AVL tree of height h has N(h) = N(h−1) + N(h−2) + 1 nodes; the
   height bound h < 1.45 log₂(n + 2) (proved via Fibonacci numbers); insertion with single and double rotations
   (implemented in C).
5. *Red-black trees* --- the colour rules; black height; h ≤ 2 log₂(n + 1) (proved); insertion in the
   left-leaning variant (implemented; deletion told); how standard libraries implement ordered maps
   (`dated` if needed); serialising a tree to a file in preorder with null markers, and reading it back.

Owns: binary search tree, search-tree property, in-order traversal (re-founded: preorder/postorder recalled),
successor (in a search tree), ordered dictionary, degenerate tree, rotation, balance factor, AVL tree, minimal AVL
tree, red-black tree, black height, left-leaning red-black tree, serialisation (of a structure). Re-founds:
binary search tree (Book 2 g12). Recalls: binary tree, height, structural induction (ch. 11), dictionary (ch. 16).

Listings: `bst.h`, `bst.c`, `bst_demo.c`; `heights.c` (sorted vs shuffled insertion heights; the town's titles
read from `data/town/books.csv` by `args=`); `rotate.c`; `avl.h`, `avl.c`, `avl_demo.c` (rotation counts);
`llrb.h`, `llrb.c`, `llrb_demo.c`; `minimal_avl.py` (N(h) vs Fibonacci, h ≤ 20); `serialise.c` (write/read
preorder with markers; round trip). Tests: `tests/bst_test.c` (random operations vs a sorted array oracle),
`tests/avl_test.c` (invariants checked after each insert), `tests/llrb_test.c`, `tests/serialise_test.c`,
`tests/test_minimal_avl.py`.

Figures: (S1) a BST with a search path, and the deletion of a node with two children (successor moved);
(S2) right and left rotation with subtrees A, B, C (in-order preserved); (S3) the four AVL rebalancing cases
(LL, LR, RL, RR) on one page; (S4) a red-black tree with black heights marked, and its 2-3 tree view for the
left-leaning variant; (S5) heights for sorted vs shuffled insertion (chart from `heights.dat`).

Exercises: 1★[P] in-order output of a tree; 2★[P] tree after inserting a sequence; 3★[P] balance factors of a
tree; 4★[P] colours after an LLRB insertion; 5★★[F] deletion that loses a subtree in the two-child case; 6★★[F] a
rotation that forgets to update the parent's link; 7★★[W] `range_count(tree, lo, hi)` in O(h + output); 8★★[W]
check that a tree is a BST (the classic wrong local check, then the right one with bounds); 9★★[R] number of BST
shapes with n nodes for n ≤ 5 (Catalan, counted by program and recurrence); 10★★★[R] prove the red-black height
bound; 11★★★[R] every AVL insertion performs at most one single or double rotation, proved; 12★★★[W] build a
perfectly balanced BST from a sorted array in O(n), with a height proof.

Weekend problem --- *Indexing the library catalogue* (25 q.): the town's 80 titles. Part I BST from catalogue
order vs alphabetical order (heights); Part II AVL insertion: rotations counted; Part III red-black colours and
black height; Part IV minimal AVL trees. Named result: *minimal AVL trees are Fibonacci trees* --- N(h) =
F(h + 3) − 1, proved, and the height bound it gives for 80 titles compared with the measured AVL height.

Ledger: `b1:avl-origin` (Adelson-Velsky and Landis 1962, *Doklady Akademii Nauk SSSR*); `b1:rb-origin`
(Guibas and Sedgewick 1978, FOCS); `b1:llrb` (Sedgewick 2008, "Left-leaning red-black trees", author's page);
`b1:libstdcxx-rbtree` (libstdc++ `std::map` is a red-black tree: `stl_tree.h` source; `dated{2026}`).

## 18 `heaps` --- Heaps and Priority Queues (~14 pp)

Programme: MP2I 3.3 (heap property, priority queue implemented by a binary tree with the heap property, heap
sort; complete tree in an array).

Hook: a hospital emergency room: the next patient is not the one who came first.

Sections:
1. *The priority-queue type* --- insert, find-min, extract-min, decrease-key; implementations by sorted and
   unsorted arrays and their costs.
2. *The binary heap in an array* --- complete binary tree (ch. 11's vocabulary), its array layout with 0-based
   indices (parent ⌊(i−1)/2⌋, children 2i+1, 2i+2, proved), the heap property, height ⌊log₂ n⌋.
3. *Sifting up and down* --- each with the invariant "a heap except at i"; costs O(log n); insert and extract.
4. *Building a heap in linear time* --- bottom-up sift-down; total work ≤ Σ heights = n − ν(n) (ν = number of
   ones in binary), so < n; the top-down build costs Θ(n log n) in the worst case (compared, counted).
5. *Heapsort and other uses* --- in-place heapsort, Θ(n log n), not stable (example); the k smallest with a heap
   of size k; decrease-key with a position index (used by ch. 25), lazy deletion as the alternative.

Owns: priority queue, complete binary tree, binary heap, heap property, sift up, sift down, heapify (bottom-up
construction), heapsort, decrease-key. Re-founds nothing. Recalls: binary tree vocabulary and height (ch. 11),
dynamic array (ch. 14), queue (ch. 15).

Listings: `pq_naive.c`; `heap.h`, `heap.c`, `heap_demo.c`; `build.c` (swap counts bottom-up vs top-down);
`heapsort.c`; `stability.c` (heapsort reorders equal keys: staged on records); `topk.c` (k smallest of the
loans' durations); `indexed_heap.c` (decrease-key); `kmerge.c` (k-way merge, problem); `heights_sum.py` (checks Σ
heights = n − ν(n) for n ≤ 10⁴). Tests: `tests/heap_test.c` (vs sorted oracle), `tests/heapsort_test.c`,
`tests/indexed_heap_test.c`, `tests/test_heights_sum.py`.

Figures: (S1) a complete tree and its array, index arrows (parent/children); (S2) sift-down step by step on one
page (three states); (S3) bottom-up build: levels with their counts and maximum sift lengths (the sum drawn);
(S4) heapsort: heap part and sorted part of the array after three extractions.

Exercises: 1★[P] the array after inserting a sequence; 2★[P] the array after one extract-min; 3★[P] the parent and
children of index 13; 4★[P] is a given array a heap; 5★★[F] sift-down that compares with only one child;
6★★[F] an index formula written for 1-based arrays used with 0-based; 7★★[W] a max-heap for structures with a
comparator (`void *`); 8★★[W] the k-th smallest with a heap of size k, O(n log k); 9★★[R] the height of a heap of n
nodes is ⌊log₂ n⌋, proved; 10★★★[R] Σ of heights in a heap of n nodes = n − ν(n), proved by induction;
11★★★[W] median maintenance with two heaps over the loans stream, tested; 12★★★[R] heapsort makes at most 2n log₂ n
comparisons, proved from the sift-down count.

Weekend problem --- *Merging the branch libraries' lists* (24 q.): k sorted lists of loan dates. Part I merging
by repeated scanning (cost nk); Part II a heap of size k (cost n log k), proved; Part III building and
maintaining the heap, counted; Part IV the sum of heights. Named result: *the heap identity* --- in a heap of n
nodes the heights sum to n − ν(n), proved, so bottom-up construction costs fewer than n swaps, and checked by
program for n ≤ 10⁴.

Ledger: `b1:heapsort-origin` (Williams 1964, CACM Algorithm 232); `b1:floyd-treesort` (Floyd 1964, CACM
Algorithm 245, bottom-up build) --- only if the history box names them.

## 19 `sorting` --- Sorting (~16 pp)

Programme: MP2I 4.3 (merge sort, divide and conquer), 1.1 (average case); outline: quicksort, average by
counting, lower bound, counting and radix sort, stability, library sorts.

Hook: a punched-card sorting machine that sorted a census one column at a time --- and why that works.

Sections:
1. *Quicksort and its partition* --- partition recalled from ch. 12 (proved there); quicksort's correctness by
   strong induction; worst case Θ(n²) on sorted input with the first element as pivot; best case; average over
   all n! orders of distinct keys: C(n) = 2(n+1)H_n − 4n, derived by counting (each pivot rank occurs in exactly
   (n−1)! orders), so ~ 2n ln n; recursion on the smaller side bounds the depth by log₂ n; median of three and
   insertion sort for small parts; equal keys and three-way partition.
2. *Merge sort* --- re-found of Book 2 g12: top-down and bottom-up; stable; Θ(n log n) comparisons (exact worst
   case for n = 2^k); extra space Θ(n).
3. *The lower bound* --- comparison sorts as comparison trees; a tree sorting n keys has ≥ n! leaves, so height ≥
   log₂ n! ≥ (n/2) log₂(n/2) (elementary bound, proved); the average-case bound (told via path lengths).
4. *Sorting without comparisons* --- counting sort (stable), radix sort least significant digit first, correct
   by induction on digits (stability is the key), Θ(d(n + k)); stability defined and used.
5. *How library sorts are built* --- hybrid designs: introsort (quicksort, heapsort fallback, insertion sort) in
   C++ standard libraries; adaptive merge sorts (Timsort, then the powersort merge policy) in Python; what the
   standards promise (`dated{2026}` for implementation details); measured comparison on the author's laptop
   (MEASURED).

Owns: comparison sort, in-place sort, stable sort, quicksort, pivot, merge sort, comparison tree (the outline's
"decision tree"; named so to keep *decision tree* for the Year 2 learning chapter), inversion (of a sequence),
counting sort, radix sort, introsort, three-way partition. Re-founds: quicksort, merge sort, sorting lower bound
(Book 1 g8, Book 2 g12). Recalls: partition and its invariant (ch. 12), recurrences, harmonic numbers (ch. 13),
counting and n! (mathematics), heapsort (ch. 18), insertion sort (Book 1 g8).

Listings: `quicksort.c` (with comparison counter; `sorted` vs shuffled inputs); `qs_average.py` (exact average
comparisons over all permutations, n ≤ 9, vs the formula with fractions); `quicksort3.c` (three-way);
`mergesort.c` (top-down, bottom-up); `stable.c` (records sorted twice: stability shown); `lower_bound.py`
(⌈log₂ n!⌉ vs merge sort's worst case for n ≤ 16); `counting_sort.c`; `radix.c` (sorting the loans by date
digits); `library_sorts.sh` (session: `qsort` vs own sorts on the same data, MEASURED); `sort5.py` (problem:
exhaustive check of the merge-insertion order for 5 keys). Tests: `tests/quicksort_test.c`,
`tests/mergesort_test.c`, `tests/radix_test.c` (all vs `qsort` on random and adversarial inputs),
`tests/test_qs_average.py`, `tests/test_sort5.py`.

Figures: (S1) quicksort's recursion on an example, partitions boxed; (S2) the comparison tree of insertion sort on
3 keys (6 leaves, height 3); (S3) LSD radix sort on 3-digit keys, one column per pass (stability arrows);
(S4) chart: comparisons of quicksort (sorted vs shuffled), merge sort, heapsort and the lower bound, n = 2..64
(from `figures/comparisons.py`). Photograph: a punched-card sorter (IBM 082 or a Hollerith sorter, Commons,
licence read) in a `history` box on radix sorting.

Exercises: 1★[P] the array after one Lomuto partition; 2★[P] merge of two runs; 3★[P] counting sort's count array;
4★[P] is a sort stable on a given example; 5★★[F] quicksort recursing on the whole array when all keys are equal
(three-way fix); 6★★[F] radix sort with an unstable inner sort; 7★★[W] sort the town's loans by (member, date)
with a stable sort applied twice; 8★★[R] the number of inversions is the number of swaps of insertion sort,
proved; 9★★[R] ⌈log₂ 12!⌉ and what it says about sorting 12 keys; 10★★★[R] derive C(n) = 2(n+1)H_n − 4n from the
averaged recurrence; 11★★★[W] count inversions in O(n log n) by merge sort, tested vs the quadratic count;
12★★★[R] radix sort's correctness by induction on the number of passes.

Weekend problem --- *Five keys in seven comparisons* (25 q.): Part I the lower bound: ⌈log₂ 5!⌉ = 7; Part II
insertion sort (10 worst case) and merge sort (8) counted; Part III the merge-insertion strategy for 5 keys
traced on an example; Part IV an exhaustive check of all 120 orders by program. Named result: *five keys can be
sorted in seven comparisons, and no method does it in six*, proved (lower bound) and verified (all 120 orders).

Ledger: `b1:quicksort-origin` (Hoare 1961 CACM Algorithm 64 / 1962 Computer Journal); `b1:ford-johnson` (Ford and
Johnson 1959, Amer. Math. Monthly); `b1:introsort` (Musser 1997, Software: Practice and Experience);
`b1:libstdcxx-introsort` (libstdc++ `std::sort` is introsort: source `stl_algo.h`; `dated{2026}`);
`b1:cpython-listsort` (CPython `Objects/listsort.txt`: Timsort, powersort merge policy since 3.11 --- to verify);
`b1:cpp-sort-complexity` (`std::sort` O(n log n) comparisons since C++11; cppreference); `b1:card-sorter`
(the punched-card sorter photographed: model, maker, decade; IBM Archives page); photo credit.

# Part V --- Algorithm design

## 20 `backtracking` --- Exhaustive Search and Backtracking (~14 pp)

Programme: MP2I 4.2 (brute force, backtracking, ordering data first), (S3-4 there) branch and bound as a first
look; outline: subsets, permutations, combinations; n queens, sudoku, subset sum.

Hook: a sudoku grid that a newspaper calls "diabolical" solved in a fraction of a second by trying.

Sections:
1. *Enumerating* --- subsets (binary counting and recursion), permutations (swap-based and lexicographic
   successor), combinations; counts recalled from the mathematics book; cost proportional to the output.
2. *The tree of partial solutions* --- states, choices, a validity test; the generic backtracking method;
   counting the nodes visited; exhaustive search as the leaf-only test.
3. *Pruning* --- test constraints as early as possible; n queens with sets of used columns and diagonals; nodes
   with and without pruning counted for n = 4..10.
4. *Sudoku and subset sum* --- sudoku with the most constrained cell first; subset sum with sorted values and
   the remaining-sum bound.
5. *Branch and bound* (first look) --- an optimisation problem; a bound from a relaxation (the fractional
   knapsack, greedy and optimal for the relaxed problem); nodes explored vs plain backtracking.

Owns: exhaustive search (brute force), backtracking, partial solution, tree of partial solutions (search tree of a
backtracking: named so to avoid "search tree"), pruning, constraint (of a search problem), branch and bound,
bounding function, relaxation (first sense: dropping a constraint; note ch. 25 owns *relaxation of an edge* →
name ch. 20's *continuous relaxation*). Recalls: counting, permutations, combinations (mathematics), recursion
(ch. 3, 11).

Listings: `subsets.py`, `permutations.py`, `combinations.py` (generators with counts); `backtrack.py` (generic
skeleton); `queens.py` (counts of solutions and nodes, n = 1..10, with/without pruning); `sudoku.py` (+ a grid file);
`subset_sum.py`; `knapsack_bb.py` (nodes explored, bound vs none); `queens_symmetry.py` (problem). Tests:
`tests/test_enumerate.py` (vs `itertools`), `tests/test_queens.py` (known counts computed independently by brute
force for n ≤ 8), `tests/test_sudoku.py`, `tests/test_knapsack.py` (vs DP of ch. 23's exercise or brute force).

Figures: (S1) the subset tree for {a, b, c} (include/exclude); (S2) the tree of partial solutions for 4 queens with
pruned nodes crossed; (S3) a sudoku grid before/after propagation of one cell (drawn, digits as TikZ text);
(S4) branch and bound on a small knapsack: nodes with bounds, pruned branches; (S5) chart of nodes with and
without pruning, n = 4..10 (log axis).

Exercises: 1★[P] order of subsets printed; 2★[P] next permutation in lexicographic order; 3★[P] nodes visited for 4
queens; 4★[P] which branch is pruned first; 5★★[F] permutations that skip one because the swap is not undone;
6★★[F] subset sum pruning that is unsound with negative numbers; 7★★[W] all ways to write n as a sum of
distinct parts; 8★★[W] a word-search puzzle solver; 9★★[R] the number of nodes of the full permutation tree of
depth n: Σ n!/k!, and its bound e·n!; 10★★★[W] graph 3-colouring by backtracking on the friendship graph, compared
with the SAT route of ch. 10; 11★★★[R] prove the fractional-knapsack bound is an upper bound for every completion;
12★★★[R] count the nodes of n-queens backtracking for n = 6 by hand reasoning on symmetries, and check.

Weekend problem --- *Eight queens and their mirrors* (24 q.): Part I the encoding (one queen per row; columns as a
permutation); Part II pruning and node counts; Part III symmetries of the square (eight), orbits of solutions;
Part IV counting by program. Named result: *the eight-queens count*: 92 solutions, 12 up to the symmetries of the
square, computed and the orbit sizes (eleven of size 8, one of size 4) proved from the symmetry analysis.

Ledger: `b1:queens-origin` (Bezzel 1848, Nauck 1850; if named, a primary or museum-grade source, else told
without names); none for counts (computed).

## 21 `divide-and-conquer` --- Divide and Conquer (~15 pp)

Programme: MP2I 4.3 (divide and conquer, meet in the middle, dichotomy: merge sort, counting inversions,
closest pair, subset sum, binary search, the k-segment cover); outline: Karatsuba, selection, Strassen told.

Hook: multiplying two 1000-digit numbers by the school method takes a million digit products; can it take
fewer?

Sections:
1. *The paradigm and its recurrences* --- split, solve, combine (re-found of Book 2 g12); recurrences by the
   master theorem (ch. 13); counting inversions by merge sort (ch. 19's sort reused).
2. *Karatsuba's multiplication* --- three half-size products instead of four; Θ(n^{log₂ 3}); implemented on
   digit lists; digit products counted; measured crossover with the school method (MEASURED); Python's own
   integers use it above a threshold (ledger).
3. *The closest pair of points* --- the strip argument (at most seven points to check, proved); Θ(n log n);
   tested against brute force on random point sets.
4. *Selection in linear time* --- quickselect and its worst case; median of medians in groups of five:
   T(n) ≤ T(⌈n/5⌉) + T(7n/10 + 6) + O(n) ⇒ O(n), proved.
5. *Dichotomy on the answer and meeting in the middle* --- binary search on a monotone predicate (the smallest
   length of k equal segments covering n points); subset sum by splitting the set in two halves, Θ(2^{n/2} n);
   fast matrix multiplication (Strassen, 7 products; told, numbers only).

Owns: divide and conquer (re-founded), Karatsuba's algorithm (indexed), closest-pair problem, quickselect, median
of medians, selection problem, monotone predicate, dichotomy on the answer (binary search on the answer), meet in
the middle, and Strassen's algorithm is named in prose only (told). Re-founds: divide and
conquer (Book 2 g12). Recalls: master theorem (ch. 13), merge sort and inversions (ch. 19), binary search (ch. 12).

Listings: `inversions.py`; `karatsuba.py` (digit-product counter); `school.py`; `karatsuba_timing.py` (MEASURED);
`closest_pair.py`; `select.py` (quickselect and median of medians, comparison counts); `segments.py`
(dichotomy on the answer); `meet_middle.py` (subset sum, with operation counts vs 2^n). Tests:
`tests/test_karatsuba.py` (vs Python `*`, hypothesis), `tests/test_closest.py` (vs brute force),
`tests/test_select.py`, `tests/test_segments.py`, `tests/test_meet.py`.

Figures: (S1) Karatsuba's recursion tree with 3 children per node and the level sums (vs 4 for the school method);
(S2) the closest-pair strip with the δ×2δ rectangle and its eight cells; (S3) median of medians: columns of five,
the guaranteed 3/10 below and above; (S4) chart: digit products of school vs Karatsuba (counted), with the
measured times (MEASURED) on a second axis or a second chart.

Exercises: 1★[P] inversions of a short list; 2★[P] the three products Karatsuba computes for 1234 × 5678; 3★[P]
quickselect's pivots on an example; 4★[P] the predicate values of a dichotomy; 5★★[F] closest pair that only checks
the next point in the strip; 6★★[F] a dichotomy on reals that never stops (tolerance fix); 7★★[W] maximum subarray
sum by divide and conquer, tested vs Kadane; 8★★[W] the majority element by divide and conquer; 9★★[R] Karatsuba's
digit-product count for n = 2^k: exactly 3^k, proved; 10★★★[R] median of medians with groups of three is not linear
(the recurrence), proved; 11★★★[W] the skyline problem by divide and conquer; 12★★★[R] meet in the middle: the
4-sum problem in O(n² log n), with proof.

Weekend problem --- *Multiplying long numbers* (24 q.): Part I the school method's n² products and carries; Part II
Karatsuba's identity and recursion; Part III exact counts for n = 2^k and the cost of the additions; Part IV the
threshold where it pays on this machine (MEASURED, question phrased on the printed table). Named result:
*Karatsuba's count* --- 3^k digit products for 2^k-digit numbers, i.e. n^{log₂ 3} ≈ n^{1.585}, proved and equal to
the program's counter.

Ledger: `b1:karatsuba` (Karatsuba and Ofman 1962, *Doklady*); `b1:strassen` (Strassen 1969, *Numerische
Mathematik*); `b1:bfprt` (Blum, Floyd, Pratt, Rivest, Tarjan 1973, JCSS); `b1:cpython-karatsuba` (CPython
`Objects/longobject.c` `KARATSUBA_CUTOFF`, value in digits of 30 bits; source; `dated{2026}`).

## 22 `greedy-proofs` --- Greedy Algorithms and Their Proofs (~14 pp)

Programme: MP2I 4.3 (greedy giving an exact solution: Huffman coding, activity selection, unit tasks with
deadlines and penalties on one machine).

Hook: a conference with forty talks and one room: how many can be fitted?

Sections:
1. *The greedy method and the exchange argument* --- re-found of Book 2 g11; two proof templates: "greedy stays
   ahead" and the exchange argument (method box).
2. *Interval scheduling* --- earliest finishing time first, proved optimal; the wrong greedy rules
   (shortest, earliest start) with counter-examples; interval partitioning by depth (proved).
3. *Unit tasks with deadlines and penalties* --- one machine, tasks of unit length, each with a deadline and a
   penalty if late; greedy by decreasing penalty with a feasibility test; proof by exchange.
4. *Huffman codes* --- prefix codes as binary trees; cost Σ f_i · depth_i; Huffman's algorithm with a priority
   queue (ch. 18); optimality proved by two lemmas (the two rarest are siblings at maximal depth; merging
   preserves optimality); encoding and decoding a text.
5. *When greedy is only an approximation* --- coin change with {1, 3, 4}; the knapsack by value density; how far
   from optimal on examples (measured against the exact answers of ch. 20/23); the theory of approximation
   ratios is the Year 3 volume's.

Owns: greedy algorithm (re-founded), exchange argument (method), interval scheduling problem, interval
partitioning, depth (of a set of intervals: name "maximum overlap" to avoid *depth* of a node --- see
DEFINITIONS), unit-task scheduling problem, prefix code, code tree, cost of a code (weighted path length),
Huffman code, Huffman's algorithm (indexed). Re-founds: greedy method (Book 2 g11). Recalls: priority queue
(ch. 18), binary tree (ch. 11), compression (Book 2 g10).

Listings: `intervals.py` (four rules on random instances vs brute force); `partition_rooms.py`; `penalties.py`;
`huffman.py` (codes for the letters of the town's titles; total bits); `encode_decode.py` (round trip);
`coins.py`; `knapsack_greedy.py`. Tests: `tests/test_intervals.py` (greedy = brute force on all small instances),
`tests/test_huffman.py` (optimal vs exhaustive search over code trees for ≤ 6 symbols; prefix property;
round-trip), `tests/test_penalties.py`.

Figures: (S1) intervals on a time line with the greedy choice and an optimal solution aligned (stays ahead);
(S2) the exchange step drawn; (S3) Huffman's merges as a forest becoming one tree, frequencies on nodes;
(S4) the code tree of the final code with codewords on the leaves.

Exercises: 1★[P] the talks chosen on an instance; 2★[P] Huffman codeword lengths for given frequencies; 3★[P]
decode a bit string with a given tree; 4★[P] coins given by greedy for an amount; 5★★[F] interval greedy sorting by
start time; 6★★[F] Huffman with a priority queue that breaks ties inconsistently between encoder and decoder;
7★★[W] minimal number of platforms for a train timetable; 8★★[W] canonical Huffman codes from code lengths;
9★★[R] a prefix code's lengths satisfy Kraft's inequality Σ 2^{−ℓ_i} ≤ 1, proved; 10★★★[R] for coin systems
{1, c, c²,...}, greedy change is optimal, proved; 11★★★[W] scheduling to minimise the maximum lateness (earliest
deadline first), tested vs brute force; 12★★★[R] the greedy matching of intervals by earliest finish is optimal:
alternative proof by induction ("stays ahead").

Weekend problem --- *Compressing the library catalogue* (24 q.): the letters of the 80 titles. Part I frequencies and
a fixed-length code; Part II Huffman's tree built (with tie rule); Part III codeword lengths, total bits, decoding;
Part IV optimality. Named result: *Huffman's theorem on the catalogue* --- no prefix code encodes the catalogue in
fewer than B bits (B printed by the program), proved by the optimality lemmas, against the fixed-length code's
count.

Ledger: `b1:huffman-1952` (Huffman 1952, *Proceedings of the IRE*, 40(9)); `b1:kraft` (Kraft 1949 MSc thesis, if
attributed).

## 23 `dynamic-programming` --- Dynamic Programming (~15 pp)

Programme: MP2I 4.3 (optimal substructure, overlapping subproblems, bottom-up and memoisation, rebuilding the
solution: subset sum, weighted scheduling, LCS, edit distance).

Hook: a spelling checker proposing "catalogue" for "catlaogue": how does it measure closeness?

Sections:
1. *Optimal substructure* --- defined and proved by cut-and-paste on examples; overlapping subproblems;
   memoisation and bottom-up tables recalled from Book 2 g12 and made systematic.
2. *The recurrence first, the table second* --- the method box (subproblems, recurrence with its proof, order of
   evaluation, answer, reconstruction); edit distance (insert, delete, substitute) with proof of the recurrence;
   the alignment rebuilt from the table.
3. *Matrix-chain order* --- the number of parenthesisations (Catalan numbers, told with a count by program);
   the O(n³) interval DP; reconstruction.
4. *Knapsack and longest increasing subsequence* --- 0/1 knapsack in O(nW) (pseudo-polynomial, discussed);
   subset sum as its special case; LIS in O(n²) by DP and in O(n log n) by patience piles with binary search
   (proved); weighted interval scheduling (in an exercise).
5. *Saving space* --- two rows for edit distance; the cost: reconstruction lost; Hirschberg's divide-and-conquer
   recovery (told).

Owns: dynamic programming (re-founded), optimal substructure, overlapping subproblems, memoisation (re-founded),
bottom-up evaluation, edit distance (Levenshtein distance), alignment, matrix-chain problem, 0/1 knapsack
problem, pseudo-polynomial algorithm, longest increasing subsequence. Re-founds: dynamic programming,
memoisation (Book 2 g12). Recalls: LCS (Book 2 g12), recurrences (ch. 13), binary search (ch. 12), divide and
conquer (ch. 21).

Listings: `fib_memo.py` (calls counted: naive vs memo); `edit_distance.py` (table + alignment); `edit_two_rows.py`;
`chain.py` (matrix chain); `catalan.py`; `knapsack.py` (table + reconstruction); `subset_sum_dp.py`; `lis.py`
(O(n²) and patience); `spell.py` (problem: queries vs the 80 titles). Tests: `tests/test_edit.py` (vs brute force
on short strings; metric properties with hypothesis), `tests/test_knapsack.py` (vs brute force),
`tests/test_lis.py`, `tests/test_chain.py`.

Figures: (S1) the edit-distance table for two short words with the back-pointers of an optimal alignment;
(S2) the dependency pattern of the three DPs (which cells a cell reads), as small grids; (S3) matrix-chain's
interval table filled by diagonals; (S4) patience piles for LIS on a 10-element example.

Exercises: 1★[P] edit distance of two short words from a partly filled table; 2★[P] calls of naive vs memoised
Fibonacci; 3★[P] knapsack table row; 4★[P] LIS length of a sequence; 5★★[F] a knapsack loop that reuses an item
(iterating capacities upward in the one-row version); 6★★[F] memoisation keyed on a mutable list; 7★★[W] weighted
interval scheduling; 8★★[W] number of ways to climb n stairs with steps in a given set; 9★★[R] prove optimal
substructure for edit distance; 10★★★[R] the patience method gives the LIS length (proof); 11★★★[W] the
longest palindromic subsequence in O(n²), tested; 12★★★[R] edit distance is a metric: prove the triangle
inequality.

Weekend problem --- *A spelling checker for the catalogue* (24 q.): misspelt queries against the 80 titles. Part I
the recurrence and its table; Part II alignments and their reconstruction; Part III two rows and the time–space
trade-off counted; Part IV the metric properties and pruning by the triangle inequality. Named result: *edit
distance is a metric*, proved, and the number of distance computations it saves on the catalogue (counted).

Ledger: `b1:levenshtein` (Levenshtein 1966, *Soviet Physics Doklady*); `b1:bellman-dp` (Bellman 1957, *Dynamic
Programming*, Princeton UP); `b1:hirschberg` (Hirschberg 1975, CACM).

## 24 `graph-traversals` --- Graphs and Traversals (~16 pp)

Programme: MP2I 3.4 (all of it), 4.5 (traversals, BFS, DFS, traversal trees, cycles, bipartiteness, unit-distance
shortest paths, reachability, topological sort by DFS, connected components; (S3-4 there) strongly connected
components by Kosaraju), 3.2 (serialisation of a relational structure).

Hook: the town of Brenmoor has one one-way street; can every place still reach every other?

Sections:
1. *Definitions* --- re-found of Book 2 g10/g12: directed and undirected graphs, vertices, edges (arcs), loops;
   degree, in/out-degree, the handshake lemma; paths, simple paths, cycles; connected and strongly connected;
   directed acyclic graphs; free trees and forests (characterisations proved: n − 1 edges, unique paths);
   bipartite graphs; weighted and labelled graphs.
2. *Representations and their costs* --- adjacency matrix (recalled from the mathematics book), adjacency lists,
   edge list; space and the costs of standard operations; the town's roads and friendships loaded; a graph
   written to and read from a file (edge list), round trip.
3. *Depth-first search* --- recursive and iterative; discovery and finishing times; the parenthesis theorem;
   tree, back, forward and cross edges; a directed graph is acyclic iff DFS finds no back edge (proved).
4. *Breadth-first search* --- the queue (ch. 15); distances in number of edges, proved; the BFS tree; testing
   bipartiteness (odd cycle certificate).
5. *Applications* --- connected components; topological order by decreasing finishing time (proved) and by
   Kahn's algorithm; strongly connected components by Kosaraju's algorithm (two passes; correctness proved via
   the component graph); bridges by DFS low points (for the problem).

Owns: graph (directed, undirected), vertex, edge (arc), loop (graph), degree, in-degree, out-degree, path (in a
graph), simple path, cycle, connected graph, connected component, strongly connected graph, strongly connected
component, directed acyclic graph, free tree, forest, bipartite graph, weighted graph, adjacency list, edge list,
depth-first search, discovery time, finishing time, tree edge, back edge, forward edge, cross edge,
breadth-first search, BFS tree, topological order, Kosaraju's algorithm (indexed), bridge, component graph
(condensation). Re-founds: graph, path, distance in edges (Book 2 g10), traversals (Book 2 g12). Recalls:
adjacency matrix (mathematics), stack and queue (ch. 15), well-founded orders (ch. 11).

Listings: `graph.py` (dataclass with adjacency lists; loaders for the town's roads and friendships);
`representations.py` (sizes and costs); `edge_file.py` (write/read round trip); `dfs.py` (times, edge classes);
`bfs.py` (distances, tree); `bipartite.py` (friendships: odd cycle found); `components.py`; `topo.py`
(course prerequisites example; DFS and Kahn agree); `kosaraju.py` (the town roads with road 1 one-way);
`bridges.py` (problem); `orient.py` (problem: strong orientation by DFS). Tests: `tests/test_dfs.py`
(parenthesis property on random graphs), `tests/test_bfs.py` (vs brute-force
shortest edge counts), `tests/test_topo.py`, `tests/test_scc.py` (vs reachability closure), `tests/test_bridges.py`.

Figures: (S1) the town's road graph drawn from `places.csv` coordinates (schematic from data, generated `.dat`),
road 1 one-way marked; (S2) a DFS on a small directed graph: discovery/finish times and the four edge classes;
(S3) BFS layers from one vertex; (S4) Kosaraju on a small graph: the reversed graph, components, condensation
DAG; (S5) the friendship graph's three groups and its isolated person 40 (drawn from data).

Exercises: 1★[P] degrees and the handshake count of a drawn graph; 2★[P] DFS order and times; 3★[P] BFS distances;
4★[P] a topological order of a small DAG; 5★★[F] DFS that marks vertices on exit only (infinite loop / repeats);
6★★[F] bipartite test that only checks one component; 7★★[W] count the shortest paths (number of) from s to every
vertex by BFS; 8★★[W] detect a cycle in a directed graph and print it; 9★★[R] a free tree on n vertices has n − 1
edges, proved; 10★★★[R] prove the correctness of Kosaraju's algorithm; 11★★★[W] Euler circuit (Hierholzer) in a
connected even-degree graph, tested; 12★★★[R] a graph is bipartite iff it has no odd cycle, proved.

Weekend problem --- *Robbins' town* (25 q.): Brenmoor's roads and friendships. Part I the friendship graph: components,
the isolated person, bipartiteness; Part II the road graph with its one-way street: strongly connected components;
Part III bridges by DFS; Part IV making every road one-way while keeping every place reachable. Named result:
*Robbins' theorem* --- a connected graph has a strongly connected orientation iff it has no bridge, proved (both
directions; the construction by DFS), and the town's orientation computed and checked.

Ledger: `b1:robbins-1939` (Robbins 1939, *American Mathematical Monthly*); `b1:kosaraju` (attribution: Kosaraju,
unpublished 1978; Sharir 1981, *Computers & Mathematics with Applications*); `b1:euler-1736` (Königsberg, if a
history box; primary: Euler Archive); `b1:graph-sizes` (only if the `dated` box of typical sizes is written).

## 25 `shortest-paths` --- Shortest Paths (~15 pp)

Programme: MP2I 4.5 (shortest paths in a weighted graph, Dijkstra with a priority queue and adjacency lists,
Floyd--Warshall with the adjacency matrix); outline: Bellman--Ford, DAG shortest paths.

Hook: the fastest way from the station to the hospital is not the shortest one.

Sections:
1. *Weighted shortest paths* --- definitions; subpaths of shortest paths are shortest (proved); the distance and
   the triangle inequality; relaxation of an edge; the shortest-path tree; negative cycles make distances
   undefined.
2. *Dijkstra's algorithm with a heap* --- re-found of Book 2 g12; the invariant (settled vertices have their
   true distance), proved; O((n + m) log n) with a binary heap and lazy deletion (ch. 18), or with decrease-key;
   the town's roads weighted by travel times (length / speed).
3. *Negative weights and Bellman--Ford* --- why Dijkstra fails (counter-example); n − 1 rounds of relaxation
   suffice (proved by path length); detecting a negative cycle.
4. *Shortest paths in a DAG* --- relax in topological order (ch. 24), linear time, proved; longest paths in a
   DAG and the critical path of a project.
5. *All pairs: Floyd--Warshall* --- DP over the set of allowed intermediate vertices, proved; O(n³) on the
   matrix; path reconstruction; when to prefer n runs of Dijkstra.

Owns: weighted path length, shortest path, distance (in a weighted graph), relaxation (of an edge), shortest-path
tree, negative cycle, Dijkstra's algorithm (re-founded, indexed), Bellman--Ford algorithm (indexed), critical path,
Floyd--Warshall algorithm (indexed), eccentricity, centre (of a graph), diameter (of a graph). Re-founds: Dijkstra's
algorithm (Book 2 g12), distance (Book 2 g10). Recalls: priority queue, decrease-key (ch. 18), topological order
(ch. 24), dynamic programming (ch. 23), adjacency matrix (mathematics).

Listings: `wgraph.py` (town roads with travel times in seconds, one-way respected); `dijkstra.py` (pops counted;
shortest-path tree); `dijkstra_neg.py` (the failure on a negative edge); `bellman_ford.py` (rounds until
stable; a negative cycle found); `dag_paths.py` (critical path of a small project); `floyd.py` (all pairs on the
town; path reconstruction); `centre.py` (problem). Tests: `tests/test_dijkstra.py` (vs Bellman--Ford and Floyd on
random non-negative graphs), `tests/test_bellman.py`, `tests/test_floyd.py`, `tests/test_dag.py`.

Figures: (S1) the town map with the fastest route from station to hospital highlighted (from data); (S2) Dijkstra's
run on a small graph: settled set, frontier, tentative distances at three moments; (S3) the counter-example with a
negative edge; (S4) Floyd--Warshall's k-th step: paths through vertex k (matrix and graph side by side).

Exercises: 1★[P] Dijkstra's order of settling on a small graph; 2★[P] distances after two Bellman--Ford rounds;
3★[P] Floyd--Warshall matrix after k = 1; 4★[P] critical path length of a small project; 5★★[F] Dijkstra that
settles a vertex when pushed; 6★★[F] Floyd--Warshall with the k loop innermost; 7★★[W] shortest path with at most
k edges (Bellman--Ford limited), tested; 8★★[W] widest-path (maximum bottleneck) by a Dijkstra variant; 9★★[R]
prove the subpath property; 10★★★[R] prove Dijkstra's invariant; 11★★★[R] number of shortest paths in a DAG by DP,
with proof; 12★★★[W] detect and print a negative cycle.

Weekend problem --- *The centre of Brenmoor* (24 q.): travel times on the town's roads. Part I modelling: weights
from lengths and speeds, the one-way road; Part II Dijkstra from the station: the tree, the pops counted;
Part III all pairs by Floyd--Warshall, checked against 30 Dijkstra runs; Part IV eccentricities. Named result:
*the town's centre and diameter* --- the place minimising its greatest travel time and the diameter in minutes,
computed, with the proof that Floyd--Warshall's table is the distance table.

Ledger: `b1:dijkstra-1959` (Dijkstra 1959, *Numerische Mathematik* 1); `b1:bellman-1958` (Bellman 1958, *Quarterly
of Applied Mathematics*); `b1:ford-1956` (Ford 1956, RAND paper P-923); `b1:floyd-1962` (Floyd 1962, CACM
Algorithm 97); `b1:warshall-1962` (Warshall 1962, JACM).

## 26 `spanning-trees` --- Minimum Spanning Trees and Union--Find (~14 pp)

Programme: MP2I (S3-4 there) Kruskal, union--find with naive versions first and the tree implementation, the
complexity admitted; widest path adaptation.

Hook: laying fibre along Brenmoor's roads so that every place is connected, at the least total length.

Sections:
1. *Spanning trees and the cut property* --- spanning tree, minimum spanning tree; cuts and crossing edges; the
   cut property and the cycle property (proved); uniqueness when weights are distinct.
2. *Kruskal's algorithm* --- edges by increasing weight, skip those closing a cycle; correctness by the cut
   property; needs a fast "same component?" test.
3. *Disjoint sets* --- the union--find abstract type; a naive version favouring find (component labels), one
   favouring union (parent pointers); union by rank: height ≤ log₂ n (proved); path compression; the
   near-constant bound with the inverse Ackermann function stated (admitted, with a prose pointer); counts of
   parent-pointer steps on the town.
4. *Prim's algorithm* --- grow one tree with a priority queue (ch. 18); correctness by the cut property;
   O(m log n); Kruskal vs Prim on sparse and dense graphs (counted).
5. *Bottlenecks* --- a minimum spanning tree minimises the largest edge (minimax path property); widest paths read
   from a maximum spanning tree; clustering by removing the longest edges (told; the Year 2 volume's
   clustering).

Owns: spanning tree, minimum spanning tree, cut (of a graph), crossing edge, cut property, cycle property,
Kruskal's algorithm (indexed), Prim's algorithm (indexed), disjoint-set structure (union--find), representative
(of a set), union by rank, rank, path compression, bottleneck spanning tree. Recalls: free tree, connected
component (ch. 24), priority queue (ch. 18), Ackermann's function (ch. 11).

Listings: `mst_town.py` (loader: undirected roads by length); `kruskal.py`; `uf_naive.py` (two naive versions,
operation counts); `union_find.py` (rank + compression, steps counted); `rank_height.py` (max height vs log₂ n on
random unions); `prim.py`; `bottleneck.py`; `widest.py`. Tests: `tests/test_mst.py` (Kruskal = Prim weight =
brute force over spanning trees on small graphs), `tests/test_union_find.py` (hypothesis: same partitions as a
naive oracle), `tests/test_bottleneck.py`.

Figures: (S1) a cut and its lightest crossing edge with the exchange of the proof; (S2) Kruskal's progress on the
town graph (forest after k edges; from data); (S3) union by rank and path compression: a tree before and after a
find; (S4) the town's minimum spanning tree drawn on the map (from data).

Exercises: 1★[P] Kruskal's order of accepted edges; 2★[P] Prim's order from a given vertex; 3★[P] the parent array
after unions and finds; 4★[P] is a given tree an MST (cycle property); 5★★[F] Kruskal that tests cycles with a
visited flag only; 6★★[F] union by rank that compares sizes but updates ranks wrongly; 7★★[W] the second-best
spanning tree weight (brute force over swapped edges), tested; 8★★[W] a maze generator by random Kruskal on a grid
(seeded), every cell reachable; 9★★[R] with union by rank, a tree of rank r has ≥ 2^r nodes, proved;
10★★★[R] uniqueness of the MST with distinct weights, proved; 11★★★[R] every MST is a bottleneck spanning tree,
proved; the converse fails (example); 12★★★[W] Borůvka's algorithm, tested against Kruskal.

Weekend problem --- *Laying fibre in Brenmoor* (24 q.): the town's roads with lengths. Part I spanning trees and
their counts on a small piece of the town (by program); Part II Kruskal and Prim on the whole town, the same
weight; Part III union--find statistics (ranks, steps); Part IV bottlenecks and a two-cluster split.
Named result: *the minimum fibre length of Brenmoor* (in metres, printed by both algorithms) and the bottleneck
theorem, with the town's longest MST edge as the smallest possible maximum.

Ledger: `b1:boruvka-1926` (Borůvka 1926); `b1:kruskal-1956` (Kruskal 1956, *Proc. AMS*); `b1:prim-1957` (Prim
1957, *Bell System Technical Journal*); `b1:jarnik-1930` (Jarník 1930); `b1:tarjan-uf-1975` (Tarjan 1975, JACM,
the inverse-Ackermann bound).

# Part VI --- Machine and data

## 27 `combinational-circuits` --- Boolean Algebra and Combinational Circuits (~15 pp)

Programme: L1-AVI (*Fondement de l'informatique*: Boolean algebra, operators and properties, logic functions,
truth tables, Karnaugh simplification, combinational circuits, integer operations and their circuits;
*Structure des ordinateurs*: ALU, routing of information); L1-UB (*Électronique numérique*).

Hook: the adder inside a processor adds 64-bit numbers in a fraction of a nanosecond; it is built from gates that
each know only two bits.

Sections:
1. *Boolean functions and canonical forms* --- Boolean functions of n variables (2^{2^n} of them); the laws of
   Boolean algebra; minterms and maxterms; the canonical sum of products and product of sums from a truth table
   (ch. 10's DNF/CNF read as circuits); a circuit is a directed acyclic graph of gates (ch. 24).
2. *Simplification* --- by algebra; Karnaugh maps up to four variables (adjacency is a one-bit change, Gray order);
   implicants, prime implicants, essential prime implicants; don't-care conditions; a seven-segment decoder
   simplified.
3. *NAND alone is enough* --- functionally complete sets; {NAND} and {NOR} complete (proved); {AND, OR} is not
   (monotone functions, proved); transistors told as switches (the physics book owns them).
4. *Arithmetic and routing* --- half adder (recalled from Book 1 g9), full adder, ripple-carry adder; subtraction
   by two's complement (Book 2 g10/g11 recalled); carry look-ahead: generate and propagate, a 4-bit look-ahead
   unit; multiplexer, decoder; a 4-bit arithmetic and logic unit with an operation code and flags.
5. *Propagation delay* --- gate delays; the delay of a circuit is the longest path in its DAG (computed by ch. 25's
   DAG method); ripple-carry Θ(n) vs look-ahead (block and tree, told) O(log n); measured in gate delays by the
   simulator.

Owns: Boolean function, Boolean algebra (laws), minterm, maxterm, canonical sum of products, canonical product of
sums, combinational circuit, logic gate is NOT redefined (Book 1 g9 owns it; recalled), Karnaugh map, implicant, prime implicant, essential prime implicant, don't-care condition,
functionally complete set, full adder, ripple-carry adder, generate and propagate signals, carry-lookahead adder,
multiplexer, decoder, arithmetic and logic unit, propagation delay, critical path (of a circuit: name "longest
delay path" to avoid clashing with ch. 25's *critical path*: see DEFINITIONS). Re-founds: gates and half adder
(Book 1 g9), adder and multiplexer (Book 2 g11), combinational circuits. Recalls: DNF/CNF (ch. 10), DAG and
longest path (ch. 24--25), two's complement (Book 2 g10), the transistor as a switch (physics, Year 3).

Code (Python): `circuit.py` (a netlist as a DAG: gates, wires, evaluation in topological order, delay as longest
path; NORUN, imported); listings `truth_tables.py`, `canonical.py`, `karnaugh.py` (prints maps and prime
implicants by Quine--McCluskey for ≤ 4 variables), `nand_only.py` (NOT, AND, OR, XOR from NAND, checked
exhaustively), `adders.py` (ripple 8-bit vs look-ahead 4-bit blocks, checked against integer addition on all
inputs, delays printed), `alu.py` (4-bit ALU, flags), `seven_segment.py`, `min_nand.py` (problem: exhaustive
search of NAND circuits). Tests: `tests/test_circuit.py`, `tests/test_adders.py` (exhaustive for 8 bits),
`tests/test_alu.py`, `tests/test_min_nand.py`.

Figures: (S1) a full adder in circuitikz/`circuits.logic.US` gates with its truth table; (S2) a 4-variable Karnaugh
map with its prime implicants circled; (S3) NOT/AND/OR from NAND gates; (S4) 4-bit ripple-carry adder and the
look-ahead unit (block diagram with g/p signals); (S5) a 4-bit ALU block diagram with mux selecting the operation.
Photograph: a 7400 quad two-input NAND chip in its package (Commons, licence read), in a `history` box on
integrated circuits; optionally a portrait of George Boole (public domain, Commons).

Exercises: 1★[P] truth table of a small circuit; 2★[P] the canonical sum of products of a function; 3★[P] a
Karnaugh map's groups; 4★[P] the ALU output for an operation code; 5★★[F] a Karnaugh grouping that crosses a
non-adjacent pair (wrong Gray order); 6★★[F] a full adder netlist with the carry using XOR instead of OR (wrong on
one row); 7★★[W] a 2-to-1 and a 4-to-1 multiplexer in the simulator, exhaustive tests; 8★★[W] a comparator
`a < b` for 4-bit unsigned numbers; 9★★[R] count the Boolean functions of n variables (2^{2^n}) and the monotone
ones for n ≤ 3 (by program and argument); 10★★★[R] prove {NOR} complete and {AND, OR, NOT-free} not complete;
11★★★[R] the ripple-carry delay is 2n + 1 gate delays in the simulator's model, and the 4-bit look-ahead block's,
proved; 12★★★[W] a 4-bit multiplier as an array of AND gates and adders, exhaustive test, delay printed.

Weekend problem --- *An arithmetic unit from one kind of gate* (24 q.): Part I functions and canonical forms;
Part II NAND translations and gate counts of each block; Part III adders and their delays; Part IV the smallest
NAND half adder found by exhaustive search. Named result: *the half adder needs exactly five NAND gates* ---
a construction with five, and the exhaustive search over all circuits of at most four NAND gates finding none
(the search's size counted; the result stated as what the search prints).

Ledger: `b1:boole-1854` (Boole, *An Investigation of the Laws of Thought*, 1854); `b1:shannon-1938` (Shannon 1938,
*Trans. AIEE*, relay circuits and Boolean algebra); `b1:karnaugh-1953` (Karnaugh 1953, *Trans. AIEE*);
`b1:sheffer-1913` (Sheffer 1913, *Trans. AMS*, the stroke); `b1:7400` (the 7400 quad NAND, Texas Instruments,
1960s; TI datasheet); photo credits.

## 28 `sequential-circuits` --- Sequential Circuits and Finite-State Machines (~15 pp)

Programme: L1-AVI (*Structure des ordinateurs*: flip-flops, counters, registers, memories, control unit,
sequencing, micro-programming); outline: Moore and Mealy machines, from a state diagram to a circuit, the control
of a small processor.

Hook: a traffic light changes every thirty seconds and remembers which colour comes next; gates alone cannot
remember.

Sections:
1. *Feedback and memory* --- an SR latch from two NOR gates, simulated with unit delays (set, reset, hold, the
   forbidden input oscillating); the D latch; transparency as a problem.
2. *Flip-flops and the clock* --- the edge-triggered D flip-flop (master--slave from two latches); the clock;
   synchronous design (registers separated by combinational logic); the clock period bounded by the longest
   delay path plus the flip-flop's own times (setup and hold told, in a timing diagram).
3. *Registers, counters and memory* --- a register with enable; a shift register; a synchronous binary counter
   and a ripple counter (glitches shown in the timing simulation); a small random-access memory from a decoder,
   cells and a multiplexer.
4. *Finite-state machines* --- re-found of Book 2 g10's state machine: Moore and Mealy machines defined; state
   diagrams; a Mealy machine converted to a Moore machine and back (equivalence of outputs, proved); a sequence
   detector; from a state diagram to a circuit: state encoding, next-state and output logic simplified by
   Karnaugh maps (ch. 27), flip-flops.
5. *The control of a small processor* --- the toy machine (Book 2 g11; `code/shared/toymachine`) seen as a
   datapath (registers, ALU of ch. 27, memory) plus a control unit that is a Moore machine over
   fetch/decode/execute states; the control FSM simulated in Python drives the datapath and runs the toy
   programs, checked step for step against the shared simulator; microprogrammed control (told).

Owns: sequential circuit, latch, SR latch, D latch, flip-flop (edge-triggered D flip-flop), clock signal, clock
period, synchronous circuit, setup time, hold time, register (hardware), shift register, counter (circuit),
memory cell, Moore machine, Mealy machine, finite-state machine (re-founded), state diagram, state encoding,
datapath, control unit, microprogrammed control (told: in prose only, no definition --- see DEFINITIONS).
Re-founds: flip-flop (Book 2 g11), state machine (Book 2 g10). Recalls: combinational circuits, Karnaugh maps,
delay (ch. 27), the toy machine and the fetch--execute cycle (Book 1 g7, Book 2 g11).
Note: *register* here is the hardware register; the toy machine's registers are the same sense. *Finite automaton*
(acceptor) is Book 4's.

Code (Python): `seq.py` (a clocked simulator on top of ch. 27's `circuit.py` copy or import --- the chapter keeps
its own copy to stay independent; NORUN); listings `sr_latch.py` (unit-delay trace, oscillation on forbidden
input), `d_flipflop.py`, `timing.py` (prints a timing diagram as text and writes `.dat` for TikZ), `counter.py`
(synchronous vs ripple, glitch count), `shift.py`, `ram.py` (16 × 4 memory), `moore_mealy.py` (conversion and
equivalence check on all input words up to length 10), `detector.py` (detector to circuit: next-state equations
printed and verified), `toy_control.py` (control FSM driving a datapath; compared with `toymachine` on the
shared example programs), `lock.py` (problem). Tests: `tests/test_seq.py`, `tests/test_counter.py`,
`tests/test_moore_mealy.py`, `tests/test_toy_control.py` (same final state and outputs as `toymachine` on every
example program), `tests/test_lock.py`.

Figures: (S1) SR latch from NOR gates with its feedback and a state table; (S2) timing diagram of a D flip-flop
(clock, D, Q) with setup/hold windows (TikZ from the simulator's `.dat`, or `tikz-timing` if added); (S3) a
synchronous 3-bit counter: flip-flops and next-state logic; (S4) Moore and Mealy diagrams of the same detector
side by side; (S5) the toy machine's datapath with the control unit and its state diagram (fetch, decode,
execute states). Photograph: a magnetic-core memory plane (Commons, licence read) in a `history` box on memory.

Exercises: 1★[P] SR latch outputs for an input sequence; 2★[P] a counter's states over five clock edges; 3★[P]
a Moore machine's output word; 4★[P] a shift register after four shifts; 5★★[F] a ripple counter read while it
settles (glitch), fixed by synchronous design; 6★★[F] a state diagram missing a transition (incomplete machine);
7★★[W] a Mealy detector for `0110` with overlaps, tested on all words up to length 12; 8★★[W] a modulo-6
synchronous counter's next-state logic; 9★★[R] the number of flip-flops needed for k states (⌈log₂ k⌉), and the
one-hot alternative; 10★★★[R] Moore→Mealy and Mealy→Moore conversions preserve the output (proved, with the
one-step delay accounted for); 11★★★[R] maximum clock frequency of a given synchronous circuit from its delays;
12★★★[W] a control FSM for a vending machine, from diagram to next-state equations to simulated circuit.

Weekend problem --- *A combination lock* (24 q.): a keypad lock that opens on the sequence 1-0-1-1. Part I the
Mealy machine (overlaps handled); Part II the Moore machine and its extra state; Part III encoding, next-state
equations, Karnaugh simplification, flip-flops; Part IV the circuit simulated against the machine on every input
word up to length 12. Named result: *Mealy saves a state* --- the detector needs 4 Mealy states and 5 Moore
states, proved minimal for each kind by distinguishing words, and the circuits' flip-flop and gate counts
compared.

Ledger: `b1:eccles-jordan-1918` (Eccles and Jordan 1918 trigger circuit; patent GB 148582 or *Radio Review* 1919);
`b1:core-memory` (Whirlwind core memory, early 1950s; MIT Museum / Computer History Museum page);
`b1:mealy-1955` (Mealy 1955, *Bell System Technical Journal*); `b1:moore-1956` (Moore 1956, *Automata Studies*);
`b1:wilkes-microprogramming` (Wilkes 1951 microprogramming, if told with a date); photo credit.

## 29 `relational-model` --- The Relational Model, Relational Algebra and SQL (~16 pp)

Programme: MP2I 7 (all items: vocabulary, primary key, entities and associations, foreign key, 1--1/1--*/*--*,
SELECT with WHERE, projection, AS, DISTINCT, LIMIT, OFFSET, ORDER BY, UNION, INTERSECT, EXCEPT, Cartesian
product, JOIN, LEFT JOIN, aggregates, GROUP BY, HAVING, nested queries); L1-UJM (*Bases de données I*); the
licence adds relational algebra and DDL (kept).

Hook: the library wants the members who have never borrowed a book; three colleagues write three different
queries; are they the same question?

Sections:
1. *Relations, keys and integrity constraints* --- relations recalled from the mathematics book; schema,
   attribute, domain, tuple, relation instance; superkey, candidate key, primary key; foreign key; entity and
   referential integrity; NULL; the town's library tables created in SQLite with constraints (DDL), a violation
   refused (`PRAGMA foreign_keys = ON`, ledger).
2. *Relational algebra* --- selection, projection, renaming, union, difference, Cartesian product, natural join,
   theta join, intersection and division derived; laws (selection pushed through a join, cascades, join
   commutativity and associativity) proved on the set semantics; an algebra evaluator in Python over the town's
   CSV tables, tested against SQLite.
3. *SQL read as algebra* --- SELECT-FROM-WHERE as π σ ×; DISTINCT (sets vs multisets); ORDER BY, LIMIT, OFFSET;
   JOIN ... ON, LEFT JOIN and the NULLs it creates; three-valued logic of NULL (ch. 10's valuations extended);
   UNION, INTERSECT, EXCEPT; aggregates with GROUP BY and HAVING (the extended operator γ); nested queries (IN,
   EXISTS, correlated); views; a remark on the declarative (logic) paradigm.
4. *Entity--relationship modelling* --- entities, attributes, relationships, multiplicities 1--1, 1--*, *--*;
   translation rules into tables (a *--* split into two 1--* through an association table, as the town's `loans`);
   the library schema designed, then compared with the town's tables. Normal forms are the Year 2 volume's.

Owns: relation schema, attribute, domain (of an attribute), tuple (of a relation), relation (instance), superkey,
candidate key, primary key, foreign key, integrity constraint, referential integrity, NULL (as a marker),
relational algebra, selection (σ), projection (π), renaming (ρ), Cartesian product of relations (recalled? the
mathematics owns the product of sets; the relational operator is defined), natural join, theta join, outer join
(left), division (relational), aggregation (γ), three-valued logic, view, entity, relationship (association),
multiplicity (of a relationship), association table, entity--relationship model. Re-founds: relational model,
SQL (Book 2 g12 `relational-databases-sql`), join (Book 2 g10). Recalls: relations, Cartesian product (mathematics
Year 1), valuations (ch. 10), the town tables (TOWN.md).

Listings (SQL through `sqlrun.py` with `-- load: town` or a schema file): `schema.sql` (the library schema with
constraints; NORUN, loaded); `constraints.sql` (inserts refused: key, foreign key, NOT NULL); `select_project.sql`;
`order_limit.sql`; `joins.sql` (JOIN, LEFT JOIN, NULLs); `null_logic.sql` (three-valued results);
`set_ops.sql`; `aggregates.sql` (GROUP BY, HAVING vs WHERE); `nested.sql` (IN, EXISTS, correlated); `views.sql`;
`never_borrowed.sql` (three formulations); Python: `algebra.py` (σ, π, ρ, ∪, −, ×, ⋈ over sets of named tuples;
NORUN), `algebra_demo.py` (the town queries in algebra, same answers as SQL), `laws.py` (selection pushdown
checked on random tables). Tests: `tests/test_algebra.py` (each operator vs SQLite on random tables,
hypothesis), `tests/test_never_borrowed.py` (three queries equal), `tests/test_schema.py`.

Figures: (S1) a relation drawn as a table with schema, tuples, key underlined, a foreign key arrow to another
table; (S2) the algebra tree of a query and its rewritten form with selection pushed down; (S3) LEFT JOIN with NULL
padding drawn on two small tables; (S4) the library's entity--relationship diagram (entities, relationships,
multiplicities) and its translation into three tables.

Exercises: 1★[P] result of a selection and projection on a small table; 2★[P] rows of a LEFT JOIN; 3★[P] truth
value of a condition with NULL; 4★[P] GROUP BY ... HAVING output; 5★★[F] a query using WHERE on an aggregate;
6★★[F] `NOT IN` with a subquery containing NULL returning nothing; 7★★[W] members with more than three late
returns (SQL and algebra); 8★★[W] the division "members who borrowed every book of an author"; 9★★[R] number of
superkeys of a schema with a given candidate key (2^{n−k} counted); 10★★★[R] prove that σ distributes over ∪ and
can be pushed through ⋈ when it mentions one side only; 11★★★[R] prove that natural join is associative (set
semantics); 12★★★[W] translate an entity--relationship diagram with a 1--1, a 1--* and a *--* relationship into
a schema with constraints, tested by inserts that must fail.

Weekend problem --- *The library's missing readers* (25 q.): the town's books, members and loans. Part I keys and
constraints of the three tables; Part II algebra for loans still out and late returns; Part III the three SQL
formulations of "never borrowed" (EXCEPT, NOT EXISTS, LEFT JOIN ... IS NULL); Part IV their equivalence. Named
result: *the three anti-joins are equivalent* --- proved in relational algebra (with the NULL caveat for NOT IN),
and the count of members who never borrowed (printed by all three).

Ledger: `b1:codd-1970` (Codd 1970, CACM 13(6)); `b1:chen-1976` (Chen 1976, ACM TODS 1(1)); `b1:sqlite-fk`
(foreign-key enforcement off by default; SQLite `foreignkeys.html`); `b1:sqlite-version` (`dated{2026}` if
printed: Python's `sqlite3.sqlite_version`); `b1:sql-standard` (ISO/IEC 9075, told without part numbers, or
one row).

## 30 `project-text-search-engine` --- Project: A Search Engine for a Folder of Texts (~16 pp)

Programme: MP2I 3.2 (hash table), 3.3 (priority queue), 1.3 (tests), 5.2 (files); licence project practice
(Makefile, Git, tests); a synthesis of Parts I, II and IV.

Specification (one paragraph): a program `search` that indexes every `.txt` file of a folder and answers queries
of one or more words, printing the ten best documents with their scores; built with a Makefile, tested, kept in
Git; measured against a naive scan of every file per query.

Corpus: generated by a seeded script in the chapter (`figures/make_corpus.py` or `listings/make_corpus.py`):
N = 400 documents of 200--2000 words drawn from a vocabulary with a Zipf-like law (told; ledger if attributed),
with planted rare words for tests. No download.

Milestones (one `\section` each, with listings, outputs and tests):
1. *Specification and corpus* --- the interface (`search DIR QUERY...`), the exit statuses, the corpus generator,
   the naive scan (`naive.c`) as the first version and as the oracle.
2. *Splitting files into words* --- a tokenizer over bytes (ASCII letters lowercased; other bytes separate; a
   documented choice for non-ASCII), robust file reading (ch. 6), tests on tricky inputs.
3. *The inverted index* --- a hash table (ch. 16) from words to posting lists (dynamic arrays of
   (document, count), ch. 14); building it; memory used (counted).
4. *Answering queries* --- AND of terms by merging sorted posting lists; a score (term frequency times
   log(N / document frequency), told as a choice, cited); the top ten by a heap of size ten (ch. 18).
5. *Tests, Makefile and Git history* --- unit tests per module, an end-to-end test against the naive scan on
   random queries, ASan-clean run, the Makefile, and the project's Git history replayed in a session
   (commits per milestone).
6. *Measured against the naive scan* --- index build time, query time, crossover number of queries
   (MEASURED, *laptop*); what would come next (stemming, phrase queries, compression of postings: Book 4's text
   algorithms).

Owns: inverted index, posting list, document frequency, term frequency, tf--idf score (as defined here), tokenizer,
end-to-end test (stop words not used). Recalls: everything of ch. 6, 7, 9, 14, 16, 18.

Listings: `make_corpus.py`; `naive.c`; `tokenize.h/.c`, `index.h/.c`, `query.h/.c`, `topk.h/.c`, `main.c`
(NORUN except `main` built by the session); `Makefile`; `build.sh` (session: `make`, run on the corpus, queries);
`history.sh` (session: the milestone commits in a fresh repository); `measure.sh` (MEASURED). Tests:
`tests/tokenize_test.c`, `tests/index_test.c`, `tests/query_test.c`, `tests/topk_test.c`, `tests/test_end_to_end.py`
(builds with make in a temporary directory, compares with the naive scan on 200 seeded queries).

Figures: (S1) the architecture: modules and data flow (files → tokenizer → index → query → heap → output);
(S2) the inverted index: hash table buckets → posting lists; (S3) merging two posting lists for an AND query;
(S4) chart: naive scan vs index, time per query and cumulative time vs number of queries (MEASURED, from
`figures/measure.py`'s `.dat`). AI: a desk with stacks of paper folders and a closed laptop (no screen, no
letters), for the hook of milestone 1.

Exercises (12: 4★, 5★★, 3★★★; no weekend problem): 1★[P] tokens of a tricky line; 2★[P] posting lists after
indexing three tiny documents; 3★[P] the AND merge of two lists; 4★[P] the top-3 heap's contents after a stream of
scores; 5★★[F] a tokenizer that drops the last word of a file without a final newline; 6★★[F] a posting list that
counts a word twice in one document as two documents; 7★★[W] OR queries; 8★★[W] a `--count` option printing the
number of matching documents only; 9★★[R] cost of an AND query of k terms with posting lists of lengths
ℓ₁ ≤ ... ≤ ℓ_k (merging smallest first), proved; 10★★★[W] phrase queries with positions in the postings;
11★★★[R] memory of the index as a function of the corpus (distinct words, total postings), computed for the corpus;
12★★★[W] persistence: save the index to a binary file (ch. 6) and load it, with a round-trip test.

Ledger: `b1:tfidf` (Spärck Jones 1972, *Journal of Documentation*, inverse document frequency); `b1:zipf`
(Zipf 1949, *Human Behavior and the Principle of Least Effort*, if the law is named).
