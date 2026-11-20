# Book 4 (University Year 2, `bachelor-2`, prefix `b2`) --- chapter briefs

Phase A, 2026-11-20. Binding run file: `sources/BATCH_BOOKS_1-5.md`. Term list
with labels: `sources/book4/DEFINITIONS.md`. RISC-V package design:
`sources/book4/RV_PLAN.md`. Nothing below is printed; programme names appear
only in this file and in source comments.


## Sync changes (2026-11-20; these override the briefs below)

- Terms: `DEFINITIONS.md`, "Sync rulings". Byte order, sign extension and return address are recalled
  in ch. 10 (Book 3 owns them); ch. 11 never names Amdahl or defines *speed-up*; deadlock, query plan,
  decision problem, recursive descent, reference counting and lazy evaluation are used, never defined.
- Accepted additions: ch. 24 gets a section on resolution and unification (sequent calculus told only)
  and a section on 2-SAT through strongly connected components (Kosaraju recalled from Book 3); ch. 30
  gets MVDs and 4NF (the chase told). Page targets unchanged (±5 %).
- Tooling now exists, so the workarounds below are void: `.S` listings with `# capture: rv=asm|dis`
  (no `.sh` wrapper); C++ tests `*_test.cpp` with `// test-with: ../listings/x.cpp` (no `.hpp` split);
  Rust tests `*_test.rs` with `#[path]`; sessions with `copy=` and `# hidden` (no `$CH`); `scratch`,
  `with=`; shared year modules in `code/bachelor-2/lib/`; `mathpartir` `\inferrule` for proof trees.
- rv (frozen): `call`/`tail` are one `jal`; the text of ch. 10 says a real assembler emits `auipc` +
  `jalr`. Trace, stats and API as in `code/shared/rv/RV.md`.
- Outputs: strace allowed (the text says Linux-only), filtered to rerun byte for byte; up to 8 threads;
  nondeterministic counts in `MEASURED.txt` with "one run on the author's laptop"; no PID, inode or
  ephemeral port unless masked; figures uncounted, referred to by place, never `\cref{fig:...}`.

## Book-wide conventions

- **Target:** ~450 pp for 31 chapters, i.e. ~14.5 pp per chapter (body ~600
  source lines, solutions ~250, listings and outputs on top). Projection at
  chapters 10 and 20 in `PROGRESS.md`.
- **Calibration (bachelor band):** exactly 12 exercises, 4★ then 5★★ then 3★★★;
  one weekend problem of 22--28 questions in Parts I--IV ending on a named,
  quantified result. Ch. 31 (project): 12 exercises, no weekend problem,
  milestones as sections. Kinds in the lists below: **P** predict the output,
  **B** find and fix the bug, **W** write to a specification (tested solution
  under `exercises/`), **R** prove or count (prose solution).
- **Languages by part:** I C++20; II Rust 2021; III RISC-V subset (`.S`, run
  by `code/shared/rv/`) plus Python models of the pipeline and the caches,
  plus C for measured cache effects; IV C17 (POSIX), with C++ and Rust in
  ch. 15; V Python (`struct`, `socket`, `ipaddress`, `ssl`) for protocols and
  simulations, C where a byte-level or speed point is made; VI Rust for the
  automata and grammar code (it prepares Book 5's compiler), Python for
  ch. 24's logic; VII Python, with C for one measured comparison in ch. 25,
  SQL through `sqlrun.py` and Python's `sqlite3` in ch. 30; ch. 31 Rust.
- **Code mechanics this book relies on** (checked against `tools/`):
  - C++ tests are single files `tests/*_test.cpp` built alone (`-I listings`):
    a listing whose code a test needs keeps that code in a `listings/<stem>.hpp`
    (listed in `NORUN.txt`) included by both the runnable `<stem>_demo.cpp` and
    the test.
  - Rust tests are a Cargo crate under `tests/<crate>/` (std only, `--offline`)
    that pulls listing files in with `#[path = "../../listings/x.rs"] mod x;`
    and `#[allow(dead_code)]`; clippy runs with `-D warnings`, so listings are
    written clippy-clean. A listing that uses a helper module writes
    `mod helper;` and keeps `helper.rs` beside it in `NORUN.txt` (rustc
    resolves it in the same directory).
  - Non-deterministic outputs (data races, timings, partial `recv` sizes) go
    in `listings/MEASURED.txt`, caption says *laptop*. Process numbers, inode
    numbers and ephemeral ports are never printed: programs print relations
    ("the child's parent is me: yes"), not values.
  - Servers bind `127.0.0.1` on ports **44000 + 10·chapter + k** (ch. 16:
    44160--44169, ch. 19: 44190--44199, ch. 20: 44200--44209, ch. 31:
    44310--44319). Each capture starts and stops its server inside one run
    (a server thread or a forked child of the demo program).
  - Captures of `python -m rv asm|dis` need a capture directive the tool does
    not have (see the report); until then a plain `.sh` listing runs them.
- **Data:** the town (`code/shared/town/`, read-only) wherever tables fit
  (ch. 3, 5, 7, 18, 24, 26, 27, 28, 30); seeded generators in the chapter's own
  code elsewhere (ch. 12 images, ch. 25 texts, ch. 29 learning data). No
  download anywhere.
- **Visuals:** ~4 TikZ schematics per chapter; about 9 photographs in the
  book (hardware and historic network gear, free licence, Commons pages read
  before use) and about 6 AI illustrations (generic scenes, no screens to
  read, no brands). Every chart comes from a tested `figures/` script's
  `.dat`; measured charts use `MEASURED` outputs.
- **Ledger:** `sources/ledger/book4.md`, ids `b2:...` (or `rfcNNNN:` for an
  RFC fact others may share). Expected ~180 rows, mostly RFC fields, the
  RISC-V specification, POSIX/Linux manual pages, C++/Rust references and
  history dates. Budget ~300 fetches, counted in `PROGRESS.md`.

## Programme coverage (Phase A check, fetched 2026-11-20)

Sources read (data only): the official computer-science programme of the
two-year preparatory class MP2I/MPI (ministry annex, items marked as second
year), and three second-year licence course lists (one with per-course
contents). Copies of the extracted text are in the writer's scratch, not in the
repo. Second-year items and where Book 4 covers them:

| Programme item (second year) | Chapter(s) |
|---|---|
| Union--find with trees (complexity admitted) | Book 3 `spanning-trees` (recalled, ch. 26 note) |
| Deterministic vs probabilistic algorithms, Las Vegas, Monte Carlo; constructing a large prime | 27 |
| Decision and optimisation problems, instance, cost function, approximation algorithm; randomised approximation of MAX2SAT | 27 (MAX-SAT expectation bound, prop.), approximation ratio itself in Book 5 `hard-problems` |
| Branch and bound, relaxation | Book 3 `backtracking` (first look), Book 5 `hard-problems` |
| Greedy approximation (vertex cover, knapsack) | Book 5 `hard-problems` |
| Strongly connected components by Kosaraju; link with 2-SAT | Book 3 `graph-traversals` (Kosaraju); **2-SAT link: gap** (proposed: ch. 24 exercise or Book 3) |
| Kruskal, widest path | Book 3 `spanning-trees` |
| Maximum bipartite matching by augmenting paths (Hopcroft--Karp excluded) | 26 |
| Supervised learning: k-NN with Euclidean distance, k-d trees, ID3 on binary trees, confusion matrix, overfitting observed | 29 |
| Unsupervised: hierarchical agglomerative clustering, k-means (convergence proof not required; local minima observed) | 29 (termination is proved anyway) |
| Two-player reachability games on bipartite graphs, strategies, winning positions, attractors, memoryless winning strategies | 28 |
| Heuristic, minimax with a heuristic, alpha--beta | 28 |
| State graph, informed search A*, admissible and monotone heuristics | 28 |
| Threads, non-determinism; creation and join (pthreads) | 15 |
| Synchronisation: atomicity, Peterson (2 threads), Lamport's bakery (n threads), mutexes, semaphores; rendezvous, producer--consumer; deadlock and fairness on the dining philosophers | 15 (bakery, rendezvous and philosophers added to the outline's list) |
| Natural deduction: inference rule, sequent, proof tree, intro/elim rules for ∧ ∨ ¬ →, soundness, quantifier rules | 24 |
| Alphabet, word, prefix, suffix, factor, subword; languages, regular operations, inductive definition of regular languages | 21, 22 |
| Regular expressions, denotation, extended (POSIX) expressions | 22 |
| DFA, accessible/co-accessible, trim; ε-transitions; NFA; determinisation; ε-elimination linked to graph reachability; Thompson constructions on examples | 21, 22 |
| Glushkov automaton by Berry--Sethi; linear expressions; local languages | 22 (added to the outline's list) |
| Automaton to expression by state elimination; Kleene's theorem; closure under union, intersection, complement | 21, 22 |
| Star (pumping) lemma | 22 |
| Context-free grammar vocabulary, derivations, generated language; regular ⊂ context-free | 23 |
| Parse tree, leftmost/rightmost derivation, ambiguity, dangling else, weak equivalence | 23 |
| An ad hoc top-down recogniser (the example $S \to TS \mid c$, $T \to aSb$) | 23 (exercise; the technique is named in Book 5) |
| Text: Boyer--Moore (one shift), Rabin--Karp, Huffman, LZW | 25 (Boyer--Moore re-founded from g12; Huffman recalled from Book 3) |
| Decidability and complexity classes (P, NP, Cook--Levin admitted, halting problem) | Book 5 Part III (outline decision: owned in Year 3) |

Second-year licence courses (three universities): object-oriented programming
(Java there; C++ here, ch. 1--5), systems programming in C (processes, files,
threads, semaphores, shared memory: ch. 13--15), architecture and assembly
(ch. 10--12), IP and protocols (ch. 17--20), databases (relational algebra in
Book 3; design, transactions, indexes here, ch. 30), graph algorithms (Book 3
and ch. 26), automata and lexical analysis (ch. 21--22, Book 5), introduction
to AI (ch. 28--29), a programming project (ch. 31).

**Licence items no chapter of Book 4 covers** (proposals in the report):
client-side and server-side web programming (JavaScript, DOM, a server
language: the outline describes JavaScript and never teaches it; Book 2 has a
web application in Python); SQL's data-definition and access-control fragments
beyond `CREATE TABLE`/`CREATE INDEX` (`GRANT` does not exist in SQLite: told
in ch. 30); the three-level database architecture (told in ch. 30); System V
shared memory between processes (told in ch. 15; memory-mapped files are
Book 5 `virtual-memory`); linear algebra and arithmetic courses (mathematics
series).

---

## Part I --- C++

### 01 `cpp-classes-raii` --- From C to C++: Classes and Resource Management
- **Hook:** a Year 1 C function opens a file, reads a header, and returns early
  on a bad header: the file stays open. The same function in C++ closes it on
  every path.
- **Programme:** licence OOP (classes, encapsulation, constructors); RAII and
  exceptions are this book's C++ choice.
- **Recall box:** Y1 `dynamic-memory` (malloc/free, leaks, ownership
  conventions), `c-functions-and-stack` (lifetime), g12 `classes-and-objects`
  (class, instance, method at school).
- **Sections:** (1) C++ as a better C: references, `const`, namespaces,
  overloading, `std::string` and `std::vector` used as black boxes, streams;
  (2) classes: members, access, constructors with member initialiser lists,
  destructors, class invariants checked by the constructor; (3) resource
  acquisition is initialisation: lifetimes of automatic objects, destruction in
  reverse order, a `File` and a `Buffer` wrapper, scope guards; (4) exceptions:
  throw, catch, stack unwinding, the three exception-safety guarantees,
  `noexcept`, what exceptions cost (measured).
- **Statements:** def. (DEFINITIONS.md, 11 labels); `met:...:raii` (wrap every
  resource in an object whose destructor releases it); `prop:...:reverse-order`
  (automatic objects of a scope are destroyed in reverse order of construction,
  also during unwinding); `prop:...:every-path` (with RAII members, each
  acquired resource is released exactly once on every exit path; proof by
  induction on nested scopes).
- **Listings** (`code/bachelor-2/01-cpp-classes-raii/listings/`):
  `early_return.c` (the leak; ASan `cflags=-O0 -g -fsanitize=address`, output
  shows LeakSanitizer's report of the unclosed `FILE`'s buffer),
  `references.cpp` (alias vs pointer, swap), `const_error.cpp` (staged compile
  error: writing through a const reference), `counter.hpp`+`counter_demo.cpp`
  (a class with an invariant), `file_handle.hpp`+`file_demo.cpp` (open/close
  printed), `lifetimes.cpp` (construction/destruction order in nested scopes),
  `unwind.cpp` (exception thrown three frames deep; destructors print),
  `guarantee.cpp` (basic vs strong push on a small stack class),
  `exception_cost.cpp` (MEASURED: return-code path vs throw path).
- **Tests:** `tests/file_handle_test.cpp` (open/close counts on every path,
  including throws), `tests/counter_test.cpp`, `tests/guarantee_test.cpp`.
- **Figures:** S1 stack frames holding objects with arrows to the heap and to a
  `FILE`; S2 lifetime timeline of nested scopes (construction left, destruction
  right); S3 unwinding from `throw` to `catch` across frames; S4 the three
  guarantees as states of a container before/after a failed operation.
  History box: C with Classes (ledger).
- **Exercises:** 1★P order of constructor/destructor lines; 2★B a function
  returns a reference to a local; 3★W `IntArray` RAII wrapper with checked
  access; 4★R destructor calls for $n$ nested scopes of $m$ objects;
  5★★P which handler catches, through three nested `try`; 6★★B a constructor
  acquires two resources and throws after the first (leak) --- fix by RAII
  members; 7★★W `ScopeGuard` with dismiss; 8★★R prove the every-path
  proposition for a function with $k$ early returns; 9★★W bounded stack with
  the strong guarantee for `push`; 10★★★W transactional file writer (write a
  temporary, rename on commit, remove on unwinding); 11★★★R exception at depth
  $k$ of $n$ nested acquisitions: count and order the releases; 12★★★W a
  `Matrix` class whose invariant (rows × cols = size of storage) survives every
  operation, with const and non-const access.
- **Problem:** *A logger that never loses a line.* I the C logger with early
  returns (count exit paths: $k$ checks give $k+1$ paths; which leak); II the
  RAII logger; III exceptions and guarantees (a flush that may fail); IV cost:
  error codes vs exceptions, measured. Named result: **"$k+1$ exit paths, one
  release on each, and the measured price of a throw"** (~24 q).
- **Ledger:** C++20 is ISO/IEC 14882:2020; first C with Classes date; g++ 11.4
  (from `g++ --version`, a captured output, no row).

### 02 `cpp-copy-move` --- Copying, Moving and Smart Pointers
- **Hook:** a function returns a vector of a million strings: is it copied?
- **Recall:** ch. 1 RAII; Y1 `dynamic-arrays` (doubling array, amortised cost).
- **Sections:** (1) copying: copy constructor and copy assignment, shallow vs
  deep copy, the double free of a shallow copy (ASan), the rule of three;
  (2) value semantics: copy-and-swap, self-assignment; (3) moving: value
  categories, rvalue references, move constructor and assignment, `std::move`,
  moved-from state, guaranteed copy elision, why `noexcept` moves let a vector
  grow by moving; (4) rule of zero and rule of five; (5) smart pointers:
  `unique_ptr` (sole owner, move-only), `shared_ptr` (control block, count),
  `weak_ptr`, a cycle that leaks and its fix.
- **Statements:** `prop:...:growth-moves` (a vector grown by factor $r$ from 1
  to $n$ elements makes fewer than $n/(r-1)$ element transfers after the
  initial insertions; with copy-only elements they are copies, with `noexcept`
  moves they are moves; proof by the geometric sum); `prop:...:copy-and-swap`
  (copy-and-swap gives the strong guarantee); `met:...:rule-of-zero`.
- **Listings:** `shallow.cpp` (ASan double free), `deep_copy.cpp`,
  `counting.hpp`+`counting_demo.cpp` (a type counting copies/moves; pushes
  into a vector with and without `noexcept`), `move_demo.cpp`,
  `elision.cpp`, `rule_of_zero.cpp`, `unique.cpp`, `shared_cycle.cpp`
  (LeakSanitizer reports the cycle), `weak_fix.cpp`, `copy_vs_move.cpp`
  (MEASURED).
- **Tests:** `tests/counting_test.cpp` (exact copy/move counts for $n$ pushes,
  checks the proposition for $r=2$), `tests/buffer_test.cpp`,
  `tests/weak_test.cpp` (all nodes destroyed).
- **Figures:** S1 shallow copy: two objects, one heap buffer; S2 deep copy;
  S3 move: pointer stolen, source emptied (before/after); S4 `shared_ptr`
  control block with strong/weak counts and the cycle broken by a weak edge.
- **Exercises:** 1★P count copy/move lines; 2★B self-assignment frees its own
  buffer; 3★W copy constructor and assignment for `Buffer`; 4★R copies made by
  doubling from 1 to $n$ (fewer than $n$); 5★★P which constructor runs in eight
  statements; 6★★B use after move; 7★★W minimal `UniquePtr<T>` (move-only,
  tested); 8★★R prove copy-and-swap's strong guarantee; 9★★W a tree with
  `unique_ptr` children and raw/weak parent pointers; 10★★★W `SmallString`
  with a small-buffer optimisation, rule of five, tested; 11★★★R the
  growth-moves bound for every factor $r>1$ and its tightness; 12★★★B an
  observer list leaking through a cycle: find, fix with `weak_ptr`, prove every
  node freed.
- **Problem:** *The photo library that copied itself.* I count copies in an
  editing pipeline of images held by value; II add moves (counts from the
  instrumented type); III ownership graph with `shared_ptr`/`weak_ptr`
  (albums and photos), leak found and fixed; IV measured times of copy vs move
  for growing sizes. Named result: **"transfers of a growing array: fewer than
  $n/(r-1)$, and zero copies with `noexcept` moves"** (~24 q).
- **Ledger:** move semantics added in C++11; guaranteed elision in C++17
  (CPPREF).

### 03 `cpp-polymorphism` --- Inheritance and Polymorphism
- **Hook:** the town library lends books, maps and recordings, each with its
  own loan rules; the C version is a `switch` on a type tag that grows with
  every kind.
- **Recall:** g12 inheritance (first look); Y1 pointers to functions; ch. 1--2.
- **Sections:** (1) derived classes: base and derived, protected members,
  construction order, slicing; (2) virtual functions: `override`, `final`,
  dynamic dispatch, virtual destructors; the dispatch table and its pointer
  (shown by `sizeof` and by the same mechanism written by hand in C);
  (3) abstract classes as interfaces: pure virtual functions; (4) design:
  composition against inheritance, the substitution principle (the
  rectangle/square example with a client's postcondition); (5) the
  object-oriented design of the library system on the town's `books`, `loans`,
  `members` tables (loan policies as a strategy interface).
- **Statements:** `prop:...:layout` (one table per class, one table pointer per
  object; sizes on this machine captured); `met:...:open-closed` (add a kind
  without editing existing code); `ex:...:square` (violation shown).
- **Listings:** `shapes_switch.c`, `shapes.cpp`, `slicing.cpp`,
  `no_virtual_dtor.cpp` (ASan `new-delete-type-mismatch`), `vtable_by_hand.c`,
  `sizes.cpp`, `ctor_virtual.cpp` (virtual call in a constructor calls the base
  version), `library.hpp`+`library_demo.cpp` (reads `data/town/books.csv`,
  `loans.csv`; fines per policy), `dispatch_cost.cpp` (MEASURED: direct,
  virtual, switch).
- **Tests:** `tests/library_test.cpp` (fines on the town's loans, every policy),
  `tests/shapes_test.cpp`.
- **Figures:** S1 class diagram (generic boxes) of the library items; S2 object
  layout: table pointer → table → functions, for two classes; S3 slicing (a
  derived object copied into a base slot); S4 composition vs inheritance for
  the library design.
- **Exercises:** 1★P which function runs through pointer, reference, value;
  2★B missing virtual destructor; 3★W add `Triangle` without editing other
  files; 4★R object sizes with a table pointer and padding; 5★★P virtual call
  inside a constructor; 6★★B slicing in a `std::vector<Base>`; 7★★W refactor
  the C `switch` into a hierarchy; 8★★R prove the square violates the
  substitution principle for a stated client; 9★★W a loan-fine strategy
  interface with three policies on the town data; 10★★★W expression trees as a
  class hierarchy (evaluate, print, simplify); 11★★★R tables and pointers for
  $k$ classes of $m$ virtual functions and $N$ objects (memory count);
  12★★★W double dispatch for shape intersection tests.
- **Problem:** *The town library's lending rules.* I the rules as a `switch`;
  II a class hierarchy; III substitution checks on a client test suite;
  IV dispatch cost measured. Named result: **"one new file per new kind, and
  the measured cost of a virtual call against a switch"** (~24 q).
- **Ledger:** Simula 67 (history box: classes and virtual procedures), the
  substitution principle's 1987 keynote / 1994 paper (author named in prose as
  the source of the principle's name).

### 04 `cpp-templates` --- Templates and Generic Programming
- **Hook:** Year 1 wrote a growable array of `int` in C; a second one for
  `double` meant copying the file or giving up types with `void *`.
- **Recall:** Y1 `dynamic-arrays`, `qsort` with `void *`; ch. 2.
- **Sections:** (1) function templates and argument deduction; (2) class
  templates: a generic `Vec<T>` with the rule of five; (3) instantiation at
  compile time: one copy per type (symbols seen with `nm -C`), errors at
  instantiation, specialisation; (4) requirements on a type parameter:
  C++20 concepts and `requires`, error messages compared; (5) static against
  dynamic polymorphism: templates vs virtual functions; `qsort` vs
  `std::sort` measured (inlined comparator).
- **Statements:** `prop:...:instantiations` (each distinct argument list
  instantiates once per translation unit; duplicates merged at link time);
  `met:...:concept-first` (state the requirements before writing the body).
- **Listings:** `max_template.cpp`, `vec.hpp`+`vec_demo.cpp`,
  `instantiate.sh` (session: `g++ -c`, `nm -C | grep Vec`), `no_concept.cpp`
  and `with_concept.cpp` (staged compile errors, the two messages compared),
  `specialise.cpp`, `generic_stack.cpp`, `sort_qsort.c` and `sort_std.cpp`
  (MEASURED), `constexpr_pow.cpp`.
- **Tests:** `tests/vec_test.cpp` (several types, copy/move counts from ch. 2's
  counting type copied locally), `tests/stack_test.cpp`.
- **Figures:** S1 one template, three instantiations; S2 compile-time pipeline
  (source → instantiation → object symbols); S3 `Vec<T>` memory layout (size,
  capacity, pointer); S4 call graphs: `qsort` calling the comparator through a
  pointer vs `std::sort` with the comparator inlined.
- **Exercises:** 1★P which overload or template is chosen; 2★B template
  defined in a `.cpp` (staged link error); 3★W `clamp` with a concept;
  4★R instantiations produced by a program; 5★★P deduction failures;
  6★★B a concept weaker than the body needs; 7★★W generic `binary_search` on a
  random-access range; 8★★R count instantiations of a recursive template
  `Pow<N>`; 9★★W `Matrix<T, R, C>` with compile-time dimension checks;
  10★★★W generic binary heap with a comparator parameter; 11★★★R code size of
  $k$ types × $m$ functions (counted from `nm`); 12★★★W compile-time table of
  binomial coefficients with `constexpr`, tested.
- **Problem:** *One sort for every type.* I `qsort` and `void *`; II a template
  sort; III concepts; IV the measured speed-up. Named result: **"the
  comparator speed-up of `std::sort` over `qsort`, measured on the laptop"**
  (~24 q).
- **Ledger:** concepts in C++20, `qsort` in the C standard (CPPREF).

### 05 `cpp-standard-library` --- The Standard Library: Containers, Iterators and Algorithms
- **Hook:** counting the words in the town's 80 book titles in five lines.
- **Recall:** Y1 Part IV (dynamic array, linked list, hash table, balanced
  trees, heaps) --- which structure sits behind which container.
- **Sections:** (1) sequence containers (`vector`, `deque`, `list`, `array`)
  and their structures; (2) associative containers (`map`/`set` as balanced
  search trees; `unordered_map` as a chained hash table: buckets and load
  factor printed); (3) iterators: categories, ranges, invalidation rules;
  (4) generic algorithms and lambda expressions, C++20 ranges;
  (5) complexity guarantees, and a container chosen by measurement (`vector`
  vs `list` for middle insertion: the cache wins --- forward pointer to ch. 12).
- **Statements:** `prop:...:lower-bound` (comparisons of `lower_bound`),
  `met:...:choose` (choose by guarantee, then by measurement).
- **Listings:** `word_count.cpp` (town titles), `containers.cpp`,
  `buckets.cpp`, `invalidation.cpp` (ASan heap-use-after-free from a
  `push_back` during iteration), `lambdas.cpp`, `ranges.cpp`,
  `loans_by_member.cpp` (town loans grouped), `vector_vs_list.cpp` and
  `map_vs_unordered.cpp` (MEASURED).
- **Tests:** `tests/word_count_test.cpp`, `tests/lru_test.cpp` (exercise
  solution), `tests/loans_test.cpp`.
- **Figures:** S1 the red-black tree behind a `std::map` of eight town street
  names (drawn from the inserted keys; colours from the rules, checked by
  hand); S2 `unordered_map` buckets drawn from `buckets.cpp`'s output; S3
  iterator category hierarchy; S4 measured chart vector vs list (`.dat` from
  `figures/`).
- **Exercises:** 1★P results of algorithm calls; 2★B erase inside a loop;
  3★W top-$k$ words with `partial_sort`; 4★R cost of $n$ insertions into `map`
  vs `unordered_map`; 5★★P lambda captures by value and by reference;
  6★★B a returned lambda capturing a local by reference; 7★★W group the town's
  loans by member and month; 8★★R prove the `lower_bound` comparison bound;
  9★★W an LRU cache (`list` + `unordered_map`); 10★★★W an interval map on
  `std::map::lower_bound`; 11★★★R reallocation points of $n$ `push_back`s with
  doubling (when are iterators invalidated?); 12★★★W choose a container for a
  given workload by measurement; the test checks the order, not the times.
- **Problem:** *The town's loan desk.* I loans in a `vector`, sorted, searched;
  II maps from members to loans; III late returns found with algorithms;
  IV crossover between sorted vector and `map` measured. Named result:
  **"the crossover size at which a sorted vector stops beating a map, on the
  laptop"** (~24 q).
- **Ledger:** container complexity guarantees (CPPREF pages).

## Part II --- Rust and functional programming

### 06 `rust-ownership` --- Rust: Ownership and Borrowing
- **Hook:** Year 1's use-after-free, compiled in Rust: refused before it runs.
- **Recall:** Y1 `dynamic-memory` (use after free, double free); ch. 1--2
  (RAII, moves in C++).
- **Sections:** (1) Rust in a few pages: `rustc`, `let`, `mut`, types,
  functions, `println!`, a crate for tests; (2) ownership: one owner, drop at
  the end of scope, moves of `String`, copy types, `clone`; (3) borrowing:
  `&` and `&mut`, the rule (many shared or one exclusive), the borrow checker's
  errors; (4) lifetimes: dangling references refused, annotations in
  signatures, elision rules; (5) slices and strings: `&str` vs `String`, UTF-8
  (recalled from g10), `&[T]`, a byte index that is not a character boundary
  panics; a data race refused (forward pointer to ch. 15).
- **Statements:** `prop:...:no-race` (with only shared or one exclusive borrow,
  no two accesses to one value can be a write and another access at the same
  time; the soundness of the whole language is admitted, with a prose pointer
  to the research that proves it); `met:...:fix-borrow` (shorten a borrow,
  split a borrow, clone, or restructure).
- **Listings** (Rust, single files): `hello.rs`, `move_string.rs`,
  `use_after_move.rs` (staged error E0382), `borrow_rules.rs`, `two_mut.rs`
  (E0499), `dangling.rs` (E0106), `longest.rs`, `slices.rs`, `char_boundary.rs`
  (panic, `exit`), `use_after_free.c` (the C original under ASan).
- **Tests:** crate `tests/ownership/` (functions of `longest.rs`, `slices.rs`,
  exercise solutions).
- **Figures:** S1 a `String` on the stack (pointer, length, capacity) and its
  buffer, before and after a move; S2 shared vs exclusive borrows as arrows
  with a forbidden combination crossed; S3 lifetimes as nested brackets over
  source lines; S4 a slice pointing into an array.
- **Exercises:** 1★P does each of five snippets compile?; 2★B fix an E0502;
  3★W `first_word -> &str`; 4★R heap allocations of a program with clones;
  5★★P drop order printed by `Drop`; 6★★B returning a reference to a local;
  7★★W split a mutable slice in two (`split_at_mut`); 8★★R why
  `fn f<'a>(x: &'a str, y: &str) -> &'a str` cannot return `y`; 9★★W reverse
  the words of a `String` in place; 10★★★W a stack of `Box`ed nodes with
  `push`, `pop`, `peek`, `peek_mut`; 11★★★R the borrow rules exclude ch. 5's
  iterator invalidation: prove it for `push` during iteration; 12★★★B a port
  hides a quadratic cost behind `clone`: find and count.
- **Problem:** *Porting the dictionary that crashed.* I Year 1's C hash table
  and its three memory errors under ASan; II an ownership design in Rust;
  III borrows and lifetimes of the entry API; IV the two versions measured.
  Named result: **"three memory errors refused at compile time, same speed
  within a measured margin"** (~24 q).
- **Ledger:** Rust 2021 edition; the 2018 soundness proof of Rust's core
  (history, cited in prose without a `\cref`).

### 07 `rust-enums-and-errors` --- Enums, Pattern Matching and Error Handling
- **Hook:** a C function that returns $-1$ for an error and $-1$ as a valid
  answer.
- **Recall:** Y1 unions and enums in C, inductive sets and structural
  induction; ch. 6.
- **Sections:** (1) product and sum types; counting their values ($|A \times
  B| = |A||B|$, $|A + B| = |A| + |B|$); (2) `match`: patterns, bindings,
  guards, exhaustiveness checked by the compiler; (3) `Option` in place of
  null, `Result` in place of error codes and exceptions, the `?` operator,
  `From` for error conversion, panics for bugs; (4) recursive types with
  `Box`: a list, a binary search tree, an expression tree evaluated and
  simplified; (5) layout: tag and payload, and why `Option<&T>` is no bigger
  than `&T`.
- **Statements:** `prop:...:counting` (value counts of algebraic types);
  `prop:...:structural` (a function defined by structural recursion on a finite
  tree terminates; Y1's induction recalled); `thm:...:simplify` (the
  simplifier preserves the value; structural induction).
- **Listings:** `shapes_enum.rs`, `nonexhaustive.rs` (E0004), `option_demo.rs`,
  `weather_parse.rs` (reads `data/town/weather.csv`, returns `Result` per line,
  reports the planted defects), `expr.rs`, `bst.rs`, `sizes.rs`
  (`size_of` table), `null_crash.c` (`exit`: the C original crashes).
- **Tests:** crate `tests/enums/` (parser on every planted defect, tree
  properties, simplifier preserves values on generated expressions).
- **Figures:** S1 enum layout (tag + payload of the largest variant); S2 the
  niche: `Option<&T>` uses the null address; S3 a `Box` tree drawn from
  `bst.rs`'s insertions; S4 error propagation: `?` returning early through
  three functions.
- **Exercises:** 1★P values of `match` expressions; 2★B a new variant breaks a
  wildcard-free match: fix; 3★W `checked_div -> Option`; 4★R count values of
  five types; 5★★P where `?` returns; 6★★B `unwrap` on a missing value in a
  parser; 7★★W a JSON-like value type with a printer; 8★★R prove
  `mirror(mirror(t)) == t`; 9★★W a list enum with `len`, `rev`, `map`;
  10★★★W symbolic differentiation with simplification, tested numerically;
  11★★★R prove that `eval` terminates and that `simplify` preserves `eval`;
  12★★★W an error type for a configuration parser with line numbers.
- **Problem:** *Reading the weather station logs.* I types for readings;
  II parsing with `Result`; III a tree of monthly aggregates; IV every defect
  accounted for. Named result: **"every planted defect found --- six missing
  temperatures, two error codes, one duplicate --- and none accepted
  silently"** (counts from the run, ~24 q).
- **Ledger:** the `Option<&T>` size guarantee (RUST-REF, `std::option` docs).

### 08 `rust-traits-and-generics` --- Traits and Generics
- **Hook:** printing anything with `{}`: one trait.
- **Recall:** ch. 3 (virtual functions), ch. 4 (templates, concepts).
- **Sections:** (1) traits as interfaces: definition, implementation, default
  methods, coherence; (2) generic functions and trait bounds; monomorphisation
  (two instantiations seen with `nm`); (3) trait objects: `dyn Trait`, fat
  pointers (size 16 printed), object safety; (4) the standard traits: `Debug`,
  `Clone`, `Copy`, `PartialEq`/`Eq`, `PartialOrd`/`Ord`, `Hash`, `Default`,
  `From`, `Iterator` (preview), `Drop`, operators through `Add`; associated
  types; (5) compared: C++ templates checked at instantiation vs Rust generics
  checked at definition; virtual functions vs trait objects; zero-cost
  abstraction.
- **Statements:** `prop:...:derived-ord` (derived `Ord` is the lexicographic
  order on fields; total if every field is); `prop:...:mono` (one copy per
  type); `prop:...:fat` (a trait object reference is two machine pointers).
- **Listings:** `display.rs`, `bounds.rs`, `missing_bound.rs` (staged error),
  `mono.sh` (session: `rustc`, `nm | grep`), `shapes_dyn.rs`, `fat_pointer.rs`,
  `object_safety.rs` (E0038), `people_sort.rs` (town people, derived `Ord`),
  `vector2.rs` (`Add`), `float_sort.rs` (`partial_cmp` and NaN), `units.rs`
  (newtypes), `dispatch_cost.rs` (MEASURED).
- **Tests:** crate `tests/traits/`.
- **Figures:** S1 fat pointer (data pointer + table pointer) beside a C++ object
  with its own table pointer; S2 monomorphisation (one generic function, two
  machine-code copies) vs one `dyn` body; S3 the comparison-trait hierarchy;
  S4 the units example's types and the additions the compiler allows.
- **Exercises:** 1★P which implementation is called; 2★B a missing bound;
  3★W `Display` for a fraction in lowest terms; 4★R monomorphised copies of a
  program; 5★★P derived ordering on structs and enums; 6★★B sorting floats
  that contain NaN; 7★★W `largest<T: PartialOrd + Copy>`; 8★★R prove the
  derived-order proposition; 9★★W a collection of shapes as trait objects;
  10★★★W matrices generic over a numeric trait (`Add`, `Mul`, `Zero` written
  here; no algebraic structure named); 11★★★R table sizes for $k$ traits and
  $m$ types; 12★★★W a typestate API (a connection that cannot send before it
  opens).
- **Problem:** *A units library.* I newtypes for metres and seconds; II
  operator traits; III generics over units; IV zero cost: the emitted assembly
  of the typed and untyped versions compared (`rustc --emit asm`, the same
  number of instructions, a deterministic output). Named result: **"identical
  machine code: the units cost nothing"** (~24 q).
- **Ledger:** the 1999 orbiter lost to a unit mix-up (NASA investigation
  report) for the problem's story.

### 09 `functional-programming` --- Functional Programming
- **Hook:** the sum of the squares of the odd readings in one expression; a
  spreadsheet formula.
- **Recall:** g12 recursion; Y1 structural induction; ch. 6--8.
- **Sections:** (1) functions as values: function pointers, closures and what
  they capture (by reference, by mutable reference, by move; `Fn`, `FnMut`,
  `FnOnce`), returning closures; (2) map, filter, fold: higher-order functions
  on iterators; laziness (adaptors do nothing until consumed, shown by side
  effects); infinite iterators; (3) immutable data: persistent lists with `Rc`
  (structural sharing, counts printed), a persistent search tree by path
  copying; (4) recursion and tail calls: no guaranteed tail-call elimination
  in Rust (a deep recursion overflows its stack; the loop does not), the
  accumulator transformation; (5) reasoning by equations: pure functions,
  referential transparency, proofs of map fusion and fold laws by induction on
  lists.
- **Statements:** `thm:...:map-fusion` ($\mathrm{map}\, f \circ \mathrm{map}\,
  g = \mathrm{map}\,(f \circ g)$), `prop:...:fold-cons`, `prop:...:path-copy`
  (an insertion into a persistent search tree copies depth + 1 nodes and shares
  the rest), `met:...:accumulator`.
- **Listings:** `closures.rs`, `fn_once_error.rs` (staged), `pipeline.rs`
  (town weather: mean of valid temperatures), `lazy.rs`, `infinite.rs`,
  `persistent_list.rs` (`Rc::strong_count` printed), `persistent_bst.rs`
  (shared and copied node counts), `deep_recursion.rs` (stack overflow on a
  small thread stack, `exit`), `tail_loop.rs`.
- **Tests:** crate `tests/functional/` (fusion laws checked on generated lists,
  persistence: old versions unchanged).
- **Figures:** S1 a closure and its captured environment; S2 a lazy pipeline
  pulled by its consumer, one element at a time; S3 two persistent lists
  sharing a tail; S4 path copying: old and new roots sharing subtrees (drawn
  from `persistent_bst.rs`'s output).
- **Exercises:** 1★P order of side effects in a lazy chain; 2★B a closure that
  needs `FnMut`; 3★W `compose(f, g)`; 4★R the size of three closures
  (`size_of_val`); 5★★P fold results; 6★★B an iterator consumed twice;
  7★★W word frequencies with a fold into a `HashMap`; 8★★R prove that the right
  fold of cons is the identity; 9★★W a persistent queue from two lists;
  10★★★R prove map and filter fusion; 11★★★W a persistent search tree with path
  copying, old versions tested unchanged; 12★★★R the two-list queue's amortised
  bound fails when old versions are reused: a sequence costing $n$ each time.
- **Problem:** *A spreadsheet that never forgets.* I formulas as closures;
  II cells evaluated lazily; III every version kept by path copying (sharing
  counted); IV memory proved and measured. Named result: **"$k$ versions of an
  $n$-cell sheet in $n + k(\lceil \log_2 n \rceil + 1)$ nodes"** (balanced
  tree of cells; counted by the program; ~24 q).
- **Ledger:** none beyond Rust references (closure traits, `Rc`).

## Part III --- Architecture

### 10 `assembly-and-calling-convention` --- Assembly Language and the Calling Convention
- **Hook:** what does `x = a[i] + 1;` become inside the processor?
- **Recall:** g11 toy machine (registers, flags, jumps, `CALL`/`RET`); Y1
  `compilation-pipeline` (object files, memory of a process), Y1
  `c-functions-and-stack` (stack frame), alignment (Y1); two's complement
  (g10).
- **Sections:** (1) the RISC-V subset (RV32IM, `RV.md`): 32 registers, `x0`,
  ABI names; arithmetic, logic, shifts, comparisons; immediates and `li`;
  (2) memory: loads and stores of bytes, halves and words, sign and zero
  extension, little-endian order, alignment, `la`, arrays and structures;
  (3) control flow: branches and jumps; `if`, `while`, `for` compiled by hand;
  (4) encoding: the R, I, S, B, U, J formats, scattered immediates, sign
  extension; the assembler's listing; decoding a word by hand;
  (5) the calling convention: argument and result registers, `ra`, `sp`,
  caller- and callee-saved registers, the frame, prologue and epilogue;
  recursive factorial traced; (6) reading a compiler's output: the same C
  functions compiled by gcc for x86-64 (`gcc -O1 -S`), read with this
  chapter's ideas; a `switch` compiled to a jump table.
- **Statements:** `met:...:compile-if`, `met:...:compile-loop`,
  `met:...:frame` (writing a prologue and epilogue), `prop:...:li` (every
  32-bit constant is `lui` of $(c + 2^{11}) \gg 12$ then `addi` of the low 12
  bits read signed; proved), `prop:...:ranges` (branch reach $\pm 4$ KiB, `jal`
  reach $\pm 1$ MiB).
- **Listings** (`.S` unless said): `first.S` (sum $1..n$, prints with `ecall`),
  `array_sum.S`, `strlen.S`, `if_while.S`, `encoding.sh` (runs `python -m rv
  asm` on `first.S`; replaced by a directive if the sync adds one),
  `decode.sh` (`python -m rv dis` on a word file), `factorial.S` (run with
  `args=--trace`, printed in ranges), `struct_access.S`, `switch_table.S`
  (`.word` of labels), `clobber_bug.S` (a callee that overwrites `s0`: wrong
  total, staged), `misaligned.S` (access fault, staged, `exit`),
  `compiled.sh` (session: `gcc -O1 -S -o - sum.c` for x86-64, with `sum.c` in
  `NORUN.txt`), `count.S` (`args=--stats` for the problem).
- **Tests:** `tests/test_asm_programs.py` (every `.S` listing and every
  exercise solution run through `rv`'s Python API with several inputs, results
  compared with Python references).
- **Figures:** S1 the register file with ABI names and roles (a TikZ table
  figure); S2 a program's memory map (text, data, heap, stack at the addresses
  of `RV.md`); S3 the six instruction formats (`bytefield`, widths 7/5/3/5/5/7
  etc., checked against the specification); S4 factorial's frames at depth 3,
  drawn from the trace's `sp` values; S5 control-flow graph of a compiled
  `while` loop.
- **Exercises:** 1★P registers after six instructions; 2★B a loop's `bge`
  should be `blt`; 3★W largest element of an array; 4★R encode three
  instructions to hexadecimal; 5★★P decode five words; 6★★B a non-leaf function
  that does not save `ra`; 7★★W `strcmp` under the convention; 8★★R prove the
  `li` proposition (the rounding term); 9★★W hand-compile a C function taking a
  structure pointer; 10★★★W recursive binary search under the convention,
  tested; 11★★★R frames and stack bytes of recursive `fib(n)`: depth $n$,
  bytes $16n$, calls $2F_{n+1} - 1$; 12★★★W a jump-table `switch` with its
  bounds check.
- **Problem:** *Hand-compiling the library's check digit.* I the C function
  (a weighted digit sum over a book code); II compiled by hand; III a helper
  called under the convention; IV the executed-instruction count from
  `--stats` against a formula. Named result: **"exactly $an + b$ instructions
  for an $n$-digit code, proved and counted"** ($a$, $b$ from the final code;
  ~24 q).
- **Ledger:** RISC-V unprivileged specification version and the RV32I/M
  formats and opcodes used (RISCV-ISA); the integer register ABI names and
  calling convention (RISC-V psABI, new source key); x86-64 System V argument
  registers for reading gcc's output (psABI, new key); the 2010 origin of
  RISC-V (history box).

### 11 `processor-and-pipelining` --- The Processor: Datapath, Control and Pipelining
- **Hook:** a laundry with a washer, a dryer and a folding table: three loads
  overlap.
- **Recall:** Y1 `combinational-circuits` (multiplexer, decoder, ALU,
  propagation delay) and `sequential-circuits` (registers, clock, state
  machines); ch. 10.
- **Sections:** (1) a single-cycle datapath for the subset: PC, instruction
  memory, register file, immediate generator, ALU, data memory, multiplexers;
  `add`, `lw`, `sw`, `beq` traced through it; (2) control: the control table
  derived from the opcode, ALU control; (3) the five-stage pipeline: stages,
  pipeline registers, timing diagrams; (4) hazards: structural, data, control;
  forwarding paths; the load-use stall; flushing after a taken branch;
  (5) branch prediction: static, one-bit and two-bit saturating counters,
  measured on the branch traces of real programs; (6) the performance
  equation: time = instructions × CPI × cycle time; CPI from the simulator.
- **Statements:** `prop:...:speedup` (ideal $k$-stage speed-up $nk/(k+n-1)$),
  `prop:...:load-use` (with forwarding, a load followed by a dependent
  instruction needs exactly one stall), `prop:...:two-bit` (a loop branch of an
  inner loop of length $m$ costs one misprediction per execution of the inner
  loop with a two-bit counter, two with a one-bit one), `met:...:control-table`.
- **Listings** (Python, importing `rv`): `datapath.py` (single-cycle model:
  control signals per instruction, checked against `rv`'s results),
  `pipeline.py` (timing model on `rv`'s step records: stalls and cycles, with
  and without forwarding), `predictor.py`, `timing_diagram.py` (prints the
  diagram as text), and `.S` programs `loop_sum.S`, `load_use.S`,
  `bubble_sort.S`.
- **Tests:** `tests/test_datapath.py` (the model agrees with `rv` on every
  program), `tests/test_pipeline.py` (hand-computed cycle counts of four
  short sequences), `tests/test_predictor.py`.
- **Figures:** S1 the single-cycle datapath (large TikZ, every mux labelled);
  S2 a five-stage timing diagram generated from `timing_diagram.py`'s output;
  S3 forwarding paths EX/MEM and MEM/WB → ALU inputs; S4 the two-bit predictor
  as a state diagram (automata library); S5 CPI bars for three programs and
  three configurations (from `pipeline.py`, deterministic). Photograph: a
  processor die (free licence, read on Commons).
- **Exercises:** 1★P cycles for five independent instructions; 2★B a control
  table row: `sw` with RegWrite = 1; 3★W control signals for `lui`; 4★R ideal
  speed-up for given $n$, $k$; 5★★P a timing diagram with one load-use;
  6★★B a forwarding condition that forgets $rd \ne x0$: counterexample;
  7★★W add a predictor to `pipeline.py`; 8★★R prove the load-use proposition;
  9★★W reorder instructions to remove stalls, measured in the model;
  10★★★R CPI of a loop from a misprediction rate and a penalty; 11★★★R prove
  the two-bit proposition; 12★★★W add `jal` and `jalr` to the single-cycle
  model.
- **Problem:** *Making the sort run faster.* I count the instructions of
  `bubble_sort.S`; II cycles without forwarding; III with forwarding and a
  predictor; IV the performance equation. Named result: **"CPI from $c_1$ to
  $c_2$: the simulated gain of forwarding and prediction"** (values from the
  model; ~24 q).
- **Ledger:** photograph credits only; the five-stage organisation is a
  model, not a fact.

### 12 `caches` --- Caches and the Memory Hierarchy
- **Hook:** summing a matrix by rows or by columns: the same additions, very
  different times (measured).
- **Recall:** Y1 memory of a process; g4 memory and storage; ch. 11.
- **Sections:** (1) locality, temporal and spatial; the hierarchy (registers,
  caches, main memory, solid-state and hard disks) with latencies measured on
  the laptop (stride and working-set sweep), typical figures in a `dated`
  box; (2) direct-mapped caches: lines, the tag/index/offset split, hits and
  misses traced by hand; (3) associative caches: set-associative, fully
  associative, LRU; write-through, write-back, write-allocate; (4) misses
  classified (compulsory, capacity, conflict) by the simulator; (5) code that
  respects the cache: loop interchange, blocking a matrix product, array of
  structures vs structure of arrays, measured in C; the laptop's cache
  parameters (`getconf`); (6) average memory access time over levels.
- **Statements:** `prop:...:fields` (widths of tag, index, offset),
  `prop:...:cyclic` (LRU, $C$ lines, cyclic sweep of $C+1$ lines: every access
  misses), `prop:...:traversal` (row order: about $N^2/B$ misses; column order
  of a matrix wider than the cache: $N^2$), `prop:...:amat`.
- **Listings:** Python `cache.py` (direct-mapped and set-associative LRU
  simulator, write policies, 3C classification), `trace_demo.py` (traces from
  `rv` running `matrix_sum.S` both ways), `three_c.py`; C `rows_cols.c`,
  `stride.c`, `blocked_matmul.c`, `aos_soa.c` (all MEASURED, `cflags=-O2`);
  `cache_params.sh` (session: `getconf -a | grep CACHE`, deterministic on this
  laptop, in a `dated` box).
- **Tests:** `tests/test_cache.py` (hand-traced sequences, the cyclic
  proposition checked by simulation, 3C counts sum to the misses);
  `figures/test_sweep.py` (shape of the sweep: a rise past each capacity).
- **Figures:** S1 the hierarchy as a stack with measured latencies; S2 the
  address split (`bytefield`); S3 a direct-mapped cache's contents after a
  trace (from `cache.py`); S4 a 2-way set with LRU bits; S5 the measured
  working-set sweep chart; S6 blocked matrix product (tiles). Photographs: a
  memory module; optionally a die shot with cache arrays visible (same
  Commons file as ch. 11 is not reused).
- **Exercises:** 1★P hits and misses of a direct-mapped trace; 2★B a simulator
  that takes the index from the wrong bits; 3★W write-back dirty counting;
  4★R field widths for a given cache; 5★★P a 2-way LRU trace; 6★★B a
  column-order loop in C: interchange and measure; 7★★W 3C classification by
  a fully associative shadow cache; 8★★R prove the cyclic proposition;
  9★★W blocked transpose, measured; 10★★★R misses of row and column order with
  line size $B$; 11★★★W choose a block size by simulation; 12★★★R AMAT for
  three levels and the rate at which an L2 pays for itself.
- **Problem:** *Why the image filter is slow.* A box blur on a generated
  grey image. I trace and count misses by hand; II the simulator; III blocking;
  IV measured speed-up against the predicted miss ratio. Named result:
  **"a predicted miss ratio of $1/16$ in row order and the measured speed-up"**
  (64-byte lines, 4-byte pixels; ~24 q).
- **Ledger:** `dated{2026}` typical latencies and capacities (vendor
  datasheets or the measurements themselves; prefer printing only measured
  values); photograph credits.

## Part IV --- Systems programming

### 13 `processes-and-system-calls` --- Processes and System Calls
- **Hook:** typing `ls` in a shell: how many programs run, and who starts
  them?
- **Recall:** g12 `processes-and-scheduling` (program vs process, states);
  Y1 `the-shell`; Y1 memory of a process.
- **Sections:** (1) user mode, kernel mode and the system call; a library call
  vs a system call; the calls of "hello" seen with `strace`; the cost of a call
  measured; (2) creating a process: `fork`, two return values, the copied
  address space; (3) executing a program: the `exec` family, the argument
  vector and the environment; (4) waiting: `waitpid`, exit statuses and
  termination by a signal, zombies and orphans (the child's state read from
  `/proc`); (5) a minimal shell: read, split, fork, exec, wait; built-in `cd`
  and `exit`; the exit status of the last command.
- **Statements:** `prop:...:fork-count` ($n$ successive `fork`s give $2^n$
  processes; induction), `prop:...:cd-builtin` (a directory change made in a
  child cannot change the parent's: why `cd` is built in), `met:...:shell-loop`.
- **Listings** (C17): `hello_write.c`, `strace_hello.sh` (session: `gcc`,
  `strace -e trace=write,exit_group ./hello`; needs the sync's yes for
  `strace`), `syscall_cost.c` (MEASURED), `fork_basic.c` (prints roles and
  relations, never numbers), `fork_tree.c` (ordered by waits),
  `exec_demo.c`, `wait_status.c`, `zombie.c`, `minish.c` with `minish.stdin`
  (commands: `echo`, `printf`, `true`, `false`, `cd`, `pwd`, `exit`).
- **Tests:** `tests/minish_test.c` (`// test-with:` the shell's parser; runs
  scripted lines), `tests/test_minish.py` (end-to-end on stdin scripts).
- **Figures:** S1 user/kernel boundary with the path of a `write` call; S2 a
  `fork`: two address spaces, two return values; S3 the process tree of
  `fork_tree.c`; S4 process states with the zombie state (automata library);
  S5 the shell's loop.
- **Exercises:** 1★P lines printed by `fork(); fork(); printf(...)`; 2★B no
  `wait`: zombies; 3★W `run(argv)` returning the exit status; 4★R processes
  created by a loop of $n$ forks; 5★★P output order fixed by waits; 6★★B a
  failed `execvp` without `_exit` (two shells); 7★★W an `xargs`-lite;
  8★★R prove the fork-count proposition; 9★★W `cd` as a built-in, with the
  reason; 10★★★W `&&` and `||` in the shell; 11★★★R system calls of a
  buffered vs unbuffered program printing $n$ lines (count from `strace -c`);
  12★★★W a `pstree`-like printer of the program's own children.
- **Problem:** *Building the tiny shell.* I parsing; II fork, exec, wait;
  III statuses and built-ins; IV the system calls of one command, counted.
  Named result: **"the system-call budget of one external command"** (the
  count from `strace -c`, deterministic on this machine; ~24 q).
- **Ledger:** `fork`, `execve`, `waitpid` semantics and status macros
  (POSIX, new source key; Linux man-pages, new key); `/proc/<pid>/status`
  state letters (man-pages).

### 14 `files-pipes-signals` --- Files, Pipes and Signals
- **Hook:** `tr ... | sort | uniq -c | sort -n` --- four processes, three
  pipes, and none of the programs knows.
- **Recall:** Y1 `c-strings-structs-files` (`FILE *`), Y1 `the-shell`
  (redirection, pipes in practice, permissions), g3 files and folders.
- **Sections:** (1) file descriptors: `open`, `read`, `write`, `close`;
  descriptor table, open file descriptions, offsets; 0, 1 and 2; (2) buffering:
  the C library's buffers vs raw calls, counted and measured; line and full
  buffering; the duplicated buffer after `fork`; (3) the file-system interface:
  inodes and `stat`, hard links and the link count, symbolic links, a
  directory as a table of names; (4) redirection and pipes implemented:
  `dup2`, `pipe`, a pipeline of $k$ commands; end of file on a pipe;
  (5) signals: `kill`, `SIGINT`, `SIGTERM`, `SIGCHLD`, `SIGPIPE`; handlers
  with `sigaction`; async-signal-safety; reaping children.
- **Statements:** `prop:...:eof` (a reader sees end of file exactly when every
  write end is closed), `prop:...:calls` (copying $n$ bytes with a buffer of
  $b$ takes $\lceil n/b \rceil + 1$ reads), `met:...:pipeline` (fork $k$
  children, connect $k-1$ pipes, close every unused end).
- **Listings** (C17): `fd_basics.c`, `offsets.c`, `shared_offset.c` (after
  `fork`), `buffered_vs_raw.c` (MEASURED), `count_calls.sh` (session,
  `strace -c -e trace=read,write`, counts only), `fork_buffer.c` (a line
  printed twice), `links.sh` (session with `fixtimes`: `ln`, `ln -s`, `ls -l`;
  inode numbers never shown), `same_inode.c`, `redirect.c`, `pipeline.c`,
  `forgot_close.c` (hang bounded by `timeout=3`, `exit`), `sigint_self.c`,
  `sigchld_reap.c`, `sigpipe.c`.
- **Tests:** `tests/pipeline_test.c`, `tests/test_tools.py` (`mycp`, `tee`
  solutions on generated files).
- **Figures:** S1 descriptor table → open file table → inode; S2 a pipe
  between two processes before and after `dup2`/`close`; S3 a directory as a
  name → inode table with two names for one inode; S4 a signal's delivery on a
  timeline (sent, pending, handler runs, resumed).
- **Exercises:** 1★P bytes returned by successive reads; 2★B the forgotten
  write end; 3★W `mycp` with a buffer-size argument; 4★R calls to copy $n$
  bytes with buffer $b$; 5★★P `printf` without newline before `fork`;
  6★★B `dup2` arguments swapped; 7★★W `tee`; 8★★R prove the end-of-file
  proposition; 9★★W a $k$-stage pipeline builder; 10★★★W `<`, `>` and `|` added
  to ch. 13's shell; 11★★★R the buffer-size model $t = a \lceil n/b \rceil +
  cn$ fitted to the measurements; 12★★★W a `SIGCHLD` handler that reaps
  background jobs.
- **Problem:** *The word-frequency pipeline in C.* I descriptors; II four
  processes and three pipes; III buffering measured; IV `SIGPIPE` when the
  last stage exits early. Named result: **"the buffer-size law: $\lceil n/b
  \rceil + 1$ reads, counted from $b = 1$ to $b = 65\,536$"** (~24 q).
- **Ledger:** Linux signal numbers and default actions (signal(7)); pipe
  capacity 65 536 bytes and `PIPE_BUF` (pipe(7)); `stat` fields (POSIX).

### 15 `threads-and-synchronisation` --- Threads and Synchronisation
- **Hook:** two booking windows sell the last seat of a bus at the same
  moment.
- **Recall:** g12 race conditions, mutual exclusion, deadlock and its four
  conditions; ch. 13; ch. 6's borrow rules.
- **Sections:** (1) threads and processes: one address space, `pthread_create`
  and `pthread_join`; interleavings and how many there are; (2) data races:
  `counter++` loses updates (measured), atomicity; an exhaustive interleaving
  explorer (Python) that finds the bad schedules of a model; (3) mutual
  exclusion: critical sections; Peterson's algorithm for two threads (with
  sequentially consistent atomics; proof of mutual exclusion and of bounded
  waiting), Lamport's bakery algorithm for $n$ threads, locks; (4) condition
  variables and semaphores: producer--consumer on a bounded buffer,
  rendezvous and barriers, readers--writers; the dining philosophers: a
  deadlock (detected with a timed lock, bounded) and its fix by a global
  order; starvation; (5) the same programs in C++ (`std::thread`,
  `std::mutex`, `std::condition_variable`, `std::counting_semaphore`) and in
  Rust (`Arc<Mutex<_>>`, channels; the data race refused at compile time).
- **Statements:** `prop:...:interleavings` ($\binom{m+n}{m}$),
  `thm:...:peterson`, `thm:...:bakery` (mutual exclusion proved; the
  first-come-first-served property stated and argued), `prop:...:semaphore`
  (the buffer's invariant $0 \le \text{produced} - \text{consumed} \le N$),
  `prop:...:order` (acquiring locks in one global order makes a circular wait
  impossible).
- **Listings:** C `race.c` (MEASURED), `mutex_counter.c`, `peterson.c`
  (C11 atomics), `bakery.c`, `bounded_buffer.c` (mutex + conditions),
  `semaphores.c`, `barrier.c`, `philosophers.c` (timed locks report the
  deadlock), `philosophers_ordered.c`; C++ `counter_threads.cpp`,
  `pc_cpp.cpp`; Rust `race_refused.rs` (staged E0499/E0373), `arc_mutex.rs`,
  `channel_pc.rs`; Python `interleavings.py` (all schedules of small models:
  counter, a naive flag lock, Peterson, the bakery for three threads; prints
  counts, deterministic).
- **Tests:** `tests/test_interleavings.py`, `tests/counter_test.c`,
  `tests/pc_test.cpp`, crate `tests/rust_sync/`.
- **Figures:** S1 two threads' steps interleaved into a lost update; S2
  Peterson's protocol for two threads (flags, turn, the two waits); S3 the
  bounded buffer ring with its semaphores' counts; S4 the philosophers'
  table with forks numbered and the order that breaks the cycle; S5 measured
  lost updates against the number of threads (chart). AI illustration: a
  ticket office with several windows (generic, no signage).
- **Exercises:** 1★P final values of `x` after two threads each add 1 twice;
  2★B an early return that keeps the lock; 3★W a thread-safe counter with
  `std::lock_guard`; 4★R count interleavings; 5★★P possible outputs of a
  semaphore program; 6★★B `if` instead of `while` around a condition wait
  (the explorer finds the schedule); 7★★W a reusable barrier; 8★★R prove
  Peterson's mutual exclusion; 9★★W readers--writers with writer preference in
  Rust; 10★★★R a naive flag lock: exhibit the violating interleaving;
  11★★★W the bakery for three threads checked by the explorer; 12★★★R prove
  the lock-order proposition.
- **Problem:** *The bus-ticket office with three windows.* I the race; II
  locks; III a bounded queue with semaphores; IV every interleaving of the
  final protocol checked. Named result: **"all $\binom{16}{8} = 12\,870$
  interleavings checked: no violation"** (model sizes fixed at writing time;
  ~24 q).
- **Ledger:** Peterson 1981; Lamport 1974; Dijkstra's semaphores (1965) and
  dining philosophers (history); C11 `<stdatomic.h>`, POSIX threads, C++20
  `counting_semaphore` (CPPREF, POSIX).

### 16 `sockets` --- Sockets
- **Hook:** two programs on the same laptop exchange messages through the
  network stack without a cable.
- **Recall:** g10 HTTP clients and servers; g11 ports; ch. 14 descriptors;
  ch. 15 threads.
- **Sections:** (1) the socket interface: `socket`, `bind`, `listen`,
  `accept`, `connect`, `send`, `recv`, `close`; socket addresses, the loopback
  address, port numbers; (2) a TCP echo server and client in C; a stream has
  no message boundaries (a `recv` may return part of a send); (3) UDP:
  datagrams, `sendto`/`recvfrom`, truncation; (4) several clients: a process
  per client, a thread per client, an event loop with `poll`; compared by a
  load test; (5) framing a protocol: delimiters vs length prefixes; network
  byte order (`htonl`, the bytes printed); a small directory protocol over the
  town's people and streets.
- **Statements:** `prop:...:recv-all` (a loop of `recv` gets exactly $n$ bytes
  or end of stream), `prop:...:prefix-free` (length-prefixed framing decodes
  any concatenation uniquely; proof by induction on the number of messages),
  `met:...:server-skeleton`.
- **Listings** (C17 unless said): `echo_server.c`, `echo_client.c` (both in
  `NORUN.txt`, shown), `echo_pair.c` (forks a server child on 44160, runs the
  client, prints both sides in a fixed order), `udp_pair.c`,
  `partial_recv.c` (MEASURED: only "more than one call: yes"),
  `wrong_port.c` (forgotten `htons`, the actual port printed via
  `getsockname`, staged), `fork_server.c`, `thread_server.c`, `poll_server.c`
  (each with its client inside a demo), `byteorder.c`, `directory_server.c`
  + `directory_client.py` (Python client in the same capture via a demo
  script), `load_test.c` (MEASURED).
- **Tests:** `tests/framing_test.c` (encoder/decoder on generated messages),
  `tests/test_directory.py` (end-to-end on port 44169).
- **Figures:** S1 call sequence of a TCP client and server on two timelines;
  S2 stream vs datagram boundaries; S3 an event loop over a set of
  descriptors; S4 a length-prefixed message (`bytefield`); S5 measured
  requests per second for the three server designs (chart).
- **Exercises:** 1★P what a client may print when the server sends "ab" then
  "cd"; 2★B a forgotten `htons`; 3★W `recv_all`; 4★R bytes on the wire for a
  framed message; 5★★P a datagram larger than the buffer; 6★★B a server that
  loops when the client closes; 7★★W a line reader with its own buffer;
  8★★R prove the prefix-free proposition; 9★★W a thread-per-client server with
  a shared counter; 10★★★W a `poll` chat server; 11★★★R a cost model of
  thread-per-client vs event loop against the measurements; 12★★★W the
  `SO_REUSEADDR` experiment, explained.
- **Problem:** *The town directory service.* I protocol; II TCP server;
  III concurrency, three ways; IV load test. Named result: **"requests per
  second on loopback for three server designs (laptop)"** (~24 q).
- **Ledger:** 127.0.0.0/8 loopback (RFC 1122 / 6890); network byte order is
  big-endian (RFC 791 appendix or RFC 1700 lineage); Linux ephemeral range
  (`dated`, ip-sysctl docs); socket options (socket(7)).

## Part V --- Networks

### 17 `link-layer` --- The Link Layer
- **Hook:** a frame crosses a noisy radio link to the town's lighthouse with
  one bit flipped. Who notices?
- **Recall:** physics series, signals (prose); g11 protocols and layers;
  ch. 16.
- **Sections:** (1) links and frames: framing by flags and byte stuffing;
  (2) error detection: parity and two-dimensional parity, the Internet
  checksum, cyclic redundancy codes as division of 0/1 polynomials with XOR
  (no field theory), CRC-32 bit by bit and by table, checked against
  `zlib.crc32`; what each detects, proved; (3) sharing a medium: ALOHA and
  slotted ALOHA (throughput $Ge^{-G}$, expected values recalled), CSMA/CD,
  binary exponential backoff (simulated); (4) Ethernet and switches: MAC
  addresses, the frame layout, self-learning and flooding, loops and the
  spanning-tree protocol (told); (5) address resolution: ARP requests,
  replies, caches; (6) wireless links: attenuation, the hidden terminal,
  CSMA/CA and link-layer acknowledgements (told, signals recalled).
- **Statements:** `prop:...:parity` (detects every odd number of flips),
  `thm:...:crc-burst` (a generator of degree $r$ with constant term detects
  every burst of length $\le r$), `prop:...:crc-odd` (a factor $x+1$ detects
  every odd number of flips), `prop:...:aloha` (slotted throughput $Ge^{-G}$,
  maximum $1/e$ at $G = 1$; pure ALOHA $1/(2e)$ as an exercise).
- **Listings** (Python): `stuffing.py`, `parity.py`, `inet_checksum.py`,
  `crc.py` (bitwise and table-driven, compared with `zlib.crc32`),
  `burst_check.py` (every burst up to 16 bits through CRC-16: zero
  undetected), `aloha_sim.py` (seeded), `ethernet_frame.py` (a frame built
  byte by byte with locally administered addresses, hex dump), `switch_sim.py`,
  `arp_sim.py`; C `crc32.c` (table-driven, its value equals the Python one).
- **Tests:** `tests/test_crc.py`, `tests/test_checksum.py`,
  `tests/test_switch.py`, `figures/test_aloha.py`.
- **Figures:** S1 Ethernet frame (`bytefield`, widths from the ledger);
  S2 a CRC long division worked in full; S3 slotted ALOHA: simulated points
  and the curve $Ge^{-G}$; S4 a switch learning on a five-host LAN (table
  after each frame); S5 an ARP exchange. Photographs: an Ethernet cable's
  connector; a rack-mounted switch's ports (free licence). AI illustration:
  hands plugging a cable into a rack (no brand, no text).
- **Exercises:** 1★P parity bits of four bytes; 2★B a checksum that does not
  fold its carries; 3★W two-dimensional parity that corrects one flip;
  4★R a CRC remainder by hand with $x^3 + x + 1$; 5★★P a switch table after
  six frames; 6★★B a stuffing decoder that unescapes wrongly; 7★★W a
  table-driven CRC-8 tested against the bitwise one; 8★★R prove the $x+1$
  proposition; 9★★W CSMA/CD with backoff: mean delay by simulation;
  10★★★R prove the slotted and pure ALOHA maxima; 11★★★W exhaustive burst
  test for CRC-32 up to 32 bits on short frames; 12★★★R the fraction of random
  error patterns a CRC of degree $r$ misses ($2^{-r}$, counting argument).
- **Problem:** *The noisy link to the lighthouse.* I framing; II detecting
  errors; III sharing the radio channel; IV choosing a CRC. Named result:
  **"no burst of 16 bits or fewer passes CRC-16, and random errors pass at
  the predicted rate $2^{-16}$"** (simulated count; ~24 q).
- **Ledger:** Ethernet II field widths, minimum and maximum payload (46 and
  1500 bytes); CRC-32 polynomial (IEEE 802.3, read through a public
  standard that restates it, e.g. RFC 1952); EtherType values 0x0800,
  0x0806, 0x86DD (IEEE registry); ARP fields (RFC 826); Internet checksum
  (RFC 1071); the locally administered address bit; ALOHAnet 1971 (history).

### 18 `network-layer` --- The Network Layer: IP and Routing
- **Hook:** a packet from the laptop reaches a server through fifteen routers
  it never sees.
- **Recall:** g11 addresses, mask, routing table read by hand; g12 `routing`
  (distance vector, link state); Y1 `shortest-paths` (Dijkstra,
  Bellman--Ford).
- **Sections:** (1) IPv4 addresses, prefixes and CIDR; subnet arithmetic;
  (2) forwarding: the forwarding table, longest-prefix match on a binary
  trie; forwarding vs routing; the IPv4 header, its checksum, time to live;
  ICMP and traceroute (told); (3) network address translation: the table,
  port mapping, what it breaks; (4) fragmentation: MTU, offsets, flags;
  (5) IPv6: addresses and their text form, a simpler header;
  (6) routing algorithms analysed: distance vector (distributed
  Bellman--Ford, convergence, count to infinity, split horizon), link state
  (flooding, Dijkstra at each router), routing between operators
  (autonomous systems, path vector, told).
- **Statements:** `prop:...:lpm` (a binary trie answers in at most 32 steps),
  `thm:...:dv-converge` (synchronous distance vector converges in at most
  $n-1$ rounds; proof by induction on hop counts),
  `prop:...:count-to-infinity` (after a failure, two routers count up by the
  link cost per round), `met:...:subnet`.
- **Listings** (Python): `cidr.py` (bits by hand, checked against
  `ipaddress`), `lpm_trie.py`, `lpm_linear.py` and `lpm_bench.py` (MEASURED),
  `ipv4_header.py`, `nat_sim.py`, `fragment.py`, `ipv6_text.py`,
  `distance_vector.py` (tables per round; the failure scenario),
  `link_state.py`, `town_network.py` (routers at town places, costs from road
  lengths).
- **Tests:** `tests/test_cidr.py` (hypothesis against `ipaddress`),
  `tests/test_lpm.py`, `tests/test_routing.py` (DV equals Dijkstra after
  convergence on random graphs).
- **Figures:** S1 address and prefix split (`bytefield`); S2 the trie of a
  forwarding table (drawn from `lpm_trie.py`); S3 the IPv4 header
  (`bytefield`); S4 a NAT translation; S5 distance-vector tables over rounds on
  a four-router topology; S6 count to infinity on a timeline. Photograph: an
  early packet-switching node in a museum (free licence, if one is found).
- **Exercises:** 1★P the network of an address and prefix; 2★B a mask built
  one bit short; 3★W `contains(prefix, address)`; 4★R hosts in a /26 etc.;
  5★★P the route chosen among four; 6★★B a header checksum summed over its own
  field; 7★★W route aggregation into a minimal set; 8★★R prove the
  convergence theorem; 9★★W fragmentation for a given MTU; 10★★★W split horizon
  with poisoned reverse: it cures the two-router loop, not the three-router
  one (exhibit); 11★★★R trie vs sorted-list lookup costs; 12★★★W canonical
  IPv6 text, tested against `ipaddress`.
- **Problem:** *Routing the town's network.* I an addressing plan; II
  forwarding tables; III distance vector vs link state; IV a link fails.
  Named result: **"count to infinity: $k$ rounds to reach the limit 16, against
  one recomputation in link state"** (~24 q).
- **Ledger:** RFC 791 header fields; RFC 1918 private ranges; RFC 4632 CIDR;
  RFC 5737 and RFC 3849 documentation ranges (every printed address is in
  them); RFC 8200 IPv6 header; RFC 5952 text form; RFC 3022 NAT; RFC 2453
  infinity 16; RFC 2328 OSPF; RFC 4271 BGP; IANA's 2011 exhaustion of the
  IPv4 pool (history).

### 19 `transport-layer` --- The Transport Layer: UDP and TCP
- **Hook:** a file copied over a lossy link arrives byte for byte.
- **Recall:** g11 acknowledgements, timeouts, the alternating-bit protocol;
  ch. 16; ch. 18.
- **Sections:** (1) multiplexing by ports; the UDP header; (2) reliable
  transfer: stop-and-wait (the alternating bit re-founded), its utilisation;
  pipelining: go-back-N and selective repeat; the window limits;
  (3) TCP: segments, the three-way handshake, connection states, cumulative
  acknowledgements, the retransmission timeout estimated, closing and
  TIME-WAIT; (4) flow control: the receive window; (5) congestion control:
  slow start, AIMD, fast retransmit and recovery, the sawtooth from the
  simulator; a throughput law derived; (6) fairness: AIMD converges to an
  equal share (phase-plane argument); newer transports in a `dated` box.
- **Statements:** `prop:...:utilisation` ($U = (L/R)/(\mathrm{RTT} + L/R)$),
  `prop:...:gbn-window` ($W \le 2^k - 1$), `thm:...:sr-window` ($W \le
  2^{k-1}$, both directions), `prop:...:mathis` (periodic-loss sawtooth gives
  throughput $\frac{\mathrm{MSS}}{\mathrm{RTT}}\sqrt{3/(2p)}$),
  `thm:...:aimd-fair`.
- **Listings** (Python): `udp_header.py`, `channel.py` (seeded lossy channel,
  `NORUN`), `stop_and_wait.py`, `go_back_n.py`, `selective_repeat.py`,
  `sr_too_wide.py` (a window one too large: the receiver accepts an old
  packet, staged), `rto.py` (the estimator on a sample series),
  `tcp_states.py` (the state machine driven by events), `aimd.py` and
  `fairness.py` (`.dat` for charts), `bulk_transfer.py` (real TCP on
  127.0.0.1:44190, MEASURED).
- **Tests:** `tests/test_protocols.py` (every protocol delivers the exact
  stream under loss, reorder and duplication; hypothesis on seeds),
  `tests/test_window_limits.py`, `figures/test_aimd.py`.
- **Figures:** S1 stop-and-wait timeline; S2 sliding window over a sequence
  space; S3 TCP's connection states (automata library); S4 the handshake and
  the close; S5 the congestion window's sawtooth; S6 the two-flow phase plot
  converging to the fair line.
- **Exercises:** 1★P go-back-N retransmissions for given losses; 2★B a
  selective-repeat window off by one; 3★W stop-and-wait over the channel;
  4★R utilisation for given numbers; 5★★P the timeout values of a sample
  series; 6★★B go-back-N acknowledging the wrong number; 7★★W selective repeat
  with per-packet timers; 8★★R prove the go-back-N limit; 9★★W fast retransmit
  added to the simulator; 10★★★R derive the throughput law; 11★★★W two AIMD
  flows: the fairness index over time; 12★★★R prove that MIMD does not
  converge to fairness.
- **Problem:** *Sending the town archive across a bad link.* I stop-and-wait;
  II windows; III congestion; IV two transfers sharing a link. Named result:
  **"the $\sqrt{3/(2p)}$ law checked by simulation within a few per cent"**
  (~24 q).
- **Ledger:** RFC 768 (UDP header, 8 bytes); RFC 9293 (TCP header, states);
  RFC 6298 (estimator constants $\alpha = 1/8$, $\beta = 1/4$, $K = 4$, the
  1 s minimum); RFC 5681 (congestion control); RFC 6335 port ranges; RFC 9000
  (QUIC, `dated`); the 1997 throughput-law paper; the fairness index's 1984
  report.

### 20 `application-layer` --- The Application Layer: DNS, HTTP and TLS
- **Hook:** typing a web address: a name lookup, a connection, a handshake,
  a page.
- **Recall:** g8 name system and client--server; g10 HTTP request and
  response; g12 secure communication (keys, certificates, the steps of a
  secure connection); ch. 16, ch. 19.
- **Sections:** (1) the name system: the hierarchy, zones, resolvers
  (recursive and iterative), authoritative servers, record types, caching and
  record lifetimes; the message format; a toy name server for the zone
  `brenmoor.test` and a resolver on 127.0.0.1:44200 that speak the real
  format; (2) HTTP: versions 1.0 and 1.1 (persistent connections), head-of-line
  blocking, HTTP/2's binary frames and streams (told with its frame layout),
  HTTP/3 over QUIC (`dated`); a socket-level HTTP/1.1 server and a `urllib`
  client; (3) electronic mail, told: the SMTP dialogue and MX records;
  (4) TLS as a layer: where it sits, the 1.3 handshake's messages and round
  trips, certificates and chains (recalled from g12; their cryptography in the
  Year 3 volume), what is protected and what is not; Python's `ssl` on
  loopback with a self-signed certificate made by `openssl` during the capture
  (only the version and the verification result are printed).
- **Statements:** `prop:...:compression` (a name with compression pointers
  that point only backwards decodes in finite time), `prop:...:round-trips`
  (round trips of a first visit and of a revisit), `met:...:resolve`.
- **Listings** (Python): `dns_message.py` (encode/decode with name
  compression), `dns_demo.py` (server thread + resolver, one capture),
  `resolver_cache.py` (lifetimes simulated), `http_server.py` (`NORUN`) and
  `http_demo.py` (keep-alive vs one connection per request: counts),
  `hol_blocking.py` (simulation), `tls_demo.sh` (session: `openssl req
  -x509 ...` to a temporary directory with output discarded, then
  `python3 "$CH/tls_echo.py"`), `tls_wrong_name.py` (verification fails on a
  wrong host name, staged).
- **Tests:** `tests/test_dns.py` (round trips of every record type,
  compression, malformed pointer loops rejected), `tests/test_http.py`,
  `tests/test_tls.py` (skipped with a message if `openssl` is absent).
- **Figures:** S1 the name hierarchy down to `brenmoor.test`; S2 iterative
  resolution as a message sequence; S3 the DNS header (`bytefield`); S4
  HTTP/1.1 vs HTTP/2 on a timeline (head-of-line blocking); S5 the TLS 1.3
  handshake's messages; S6 the layer stack with what TLS hides shaded. AI
  illustration: a data-centre aisle (generic).
- **Exercises:** 1★P decode a DNS header's bytes; 2★B a compression pointer
  loop: bound it; 3★W encode an AAAA query; 4★R round trips to resolve a name
  with and without a cache; 5★★P parse a chunked response; 6★★B a wrong
  `Content-Length` makes the client hang; 7★★W keep-alive and `HEAD` in the
  server; 8★★R requests saved by caching for a given lifetime and query rate
  (expected value); 9★★W a caching resolver against the toy server;
  10★★★R a head-of-line blocking delay model; 11★★★W a TLS echo pair that
  verifies the server's certificate and host name; 12★★★R bytes of TLS
  overhead per record for given message sizes.
- **Problem:** *Brenmoor goes online.* I the zone and its server; II a
  resolver with a cache; III a web server with persistent connections;
  IV the cost of a first page load in round trips. Named result: **"the
  round-trip budget of a first visit (name lookup, connection, handshake,
  request) and of a revisit"** (~24 q).
- **Ledger:** RFC 1034/1035 (header 12 bytes, label $\le 63$, name $\le 255$,
  types A 1, NS 2, CNAME 5, MX 15), RFC 3596 (AAAA 28), RFC 2606 (`.test`),
  RFC 9110 and 9112 (HTTP), RFC 9113 (HTTP/2 frame layout), RFC 9114
  (HTTP/3), RFC 8446 (TLS 1.3: record header 5 bytes, 1-RTT handshake),
  RFC 5321 (SMTP), IANA ports 25, 53, 80, 443.

## Part VI --- Languages and logic

### 21 `finite-automata` --- Finite Automata
- **Hook:** a program that decides whether a typed string is a valid decimal
  number like `-12.5e3`, with one table and a loop.
- **Recall:** Y1 `sequential-circuits` (finite-state machines with outputs);
  Y1 structural induction; sets and maps (mathematics).
- **Sections:** (1) alphabets, words, languages: concatenation, powers, the
  star, prefixes, suffixes, factors, subwords; (2) deterministic automata: the
  transition function and its extension, recognised languages, complete
  automata, accessible and co-accessible states, trimming; (3) nondeterministic
  automata and spontaneous transitions; their elimination through
  $\varepsilon$-closures computed as graph reachability; (4) the subset
  construction, proved; the $2^k$ blow-up of "the $k$-th letter from the end
  is $a$", proved optimal by a fooling set; (5) closure under complement,
  union and intersection by the product construction; (6) an automaton as a
  program: table-driven DFA and on-the-fly NFA simulation in Rust, measured.
- **Statements:** `prop:...:extended` ($\delta^*(q, uv) = \delta^*(\delta^*(q,u),
  v)$), `met:...:subset` + `thm:...:subset-correct`, `prop:...:epsilon`
  (elimination keeps the language), `thm:...:blowup`, `prop:...:closure`
  (complement, union, intersection), `prop:...:trim`.
- **Listings** (Rust): `automaton.rs` (`NORUN`, the DFA/NFA types),
  `dfa_demo.rs` (the number recogniser on test strings), `epsilon.rs`,
  `subset.rs` (prints the constructed table), `blowup.rs` (states for
  $k = 1..12$), `product.rs`, `simulate_vs_determinise.rs` (MEASURED).
- **Tests:** crate `tests/automata/` (subset construction agrees with NFA
  simulation on all words up to length 10 over small alphabets; blow-up
  counts; closure constructions by brute force).
- **Figures:** S1 the decimal-number DFA (automata library); S2 an NFA with
  spontaneous transitions and its closure; S3 the NFA for $k = 3$ and its
  8-state determinisation (drawn from `subset.rs`'s table); S4 a product
  automaton for an intersection; S5 trimming (inaccessible and
  non-co-accessible states greyed). History box: the 1950s origins (ledger).
- **Exercises:** 1★P runs on five words; 2★B complementing an incomplete DFA;
  3★W the DFA of binary multiples of 3, with its proof; 4★R the number of
  accepted words of length $n$ (a recurrence); 5★★P a subset construction by
  hand; 6★★B a non-transitive $\varepsilon$-closure; 7★★W "contains the factor
  $aba$"; 8★★R closure under reversal; 9★★W multiples of $n$ in base $b$,
  tested; 10★★★R the fooling-set lower bound in general; 11★★★W NFA simulation
  vs determinisation, measured; 12★★★R the prefixes of a recognisable language
  are recognisable.
- **Problem:** *Decoding the lighthouse's light signals.* I signals as words;
  II a DFA for valid messages; III an NFA for "a given pattern near the end"
  and its determinisation; IV the blow-up. Named result: **"the $2^k$ law:
  exactly $2^k$ states, none removable"** (~24 q).
- **Ledger:** history only (Kleene 1956; Rabin and Scott 1959).

### 22 `regular-languages` --- Regular Expressions and the Limits of Regular Languages
- **Hook:** a search box accepts a pattern; one pattern freezes a backtracking
  engine for seconds (measured).
- **Recall:** ch. 21; Y1 structural induction.
- **Sections:** (1) regular expressions: inductive syntax, denotation,
  regular languages as the smallest class closed under the regular
  operations; extended expressions (classes, `+`, `?`, repetition counts) as
  abbreviations; (2) Kleene's theorem: expression to automaton by Thompson's
  construction and by Glushkov's automaton (linearised expressions, local
  languages, the Berry--Sethi first/last/follow sets); automaton to expression
  by state elimination; (3) minimisation: residuals, the Myhill--Nerode
  equivalence and theorem, uniqueness of the minimal automaton, Moore's
  partition refinement (Hopcroft's algorithm told); (4) the limits: the
  pumping lemma, non-regular languages ($a^n b^n$, balanced brackets,
  palindromes), Myhill--Nerode proofs; (5) decision questions and their costs:
  emptiness, finiteness, membership, inclusion, equivalence; (6) a regex engine
  in Rust (a parser to a syntax tree, Glushkov automaton, simulation) against
  Python's backtracking `re` on $(a|a)^*b$.
- **Statements:** `thm:...:kleene` (both directions), `prop:...:glushkov`
  (the Glushkov automaton has $n+1$ states and no spontaneous transition;
  recognises the language), `met:...:thompson`, `met:...:berry-sethi`,
  `met:...:elimination`, `thm:...:myhill-nerode`, `cor:...:unique-minimal`,
  `met:...:moore` (+ correctness), `thm:...:pumping`, `prop:...:decisions`.
- **Listings:** Rust `regex_ast.rs` and `parse.rs` (`NORUN`), `glushkov.rs`
  (prints first/last/follow and the automaton), `thompson.rs`,
  `eliminate.rs`, `minimise.rs`, `equivalent.rs` (product with a
  complement); Python `backtracking.py` (MEASURED, each run bounded by
  `timeout`), `engine_compare.rs` (MEASURED).
- **Tests:** crate `tests/regex/` (engine vs brute-force denotation on all
  words up to length 8; minimisation is canonical: equal languages give
  isomorphic automata; state elimination round trip).
- **Figures:** S1 Thompson's fragments; S2 the Glushkov automaton of
  $(a|b)^*abb$ with numbered positions; S3 state elimination in three steps;
  S4 Moore's refinement as a table of classes; S5 chart: backtracking time vs
  $n$ against the automaton's linear time.
- **Exercises:** 1★P which words match; 2★B an identifier pattern that allows
  a leading digit; 3★W an expression for ch. 21's decimal numbers, checked
  equivalent to the DFA; 4★R words of length $n$ in $(ab|b)^*$; 5★★P
  first/last/follow sets; 6★★B minimising an incomplete DFA merges wrong
  states; 7★★W state elimination; 8★★R $\{a^n b^m : n \le m\}$ is not regular;
  9★★W an equivalence checker for two expressions; 10★★★R the Myhill--Nerode
  index is the size of the minimal DFA; 11★★★W Moore vs Hopcroft, measured;
  12★★★R $\{w : |w|_a = |w|_b\}$ is not regular, by Myhill--Nerode and by an
  intersection with $a^*b^*$.
- **Problem:** *A search box that never freezes.* I patterns over the town's
  street names; II the Glushkov engine; III minimisation; IV backtracking's
  blow-up against the automaton. Named result: **"from exponential to linear:
  backtracking's time doubling with each $a$, measured, against at most
  $(m+1) n$ steps proved for the automaton"** (~24 q).
- **Ledger:** POSIX regular expressions (Open Group); Python's `re` engine
  documentation (backtracking); Thompson 1968; Glushkov 1961; Berry and Sethi
  1986; Myhill 1957, Nerode 1958 (history).

### 23 `context-free-languages` --- Context-Free Grammars and Pushdown Automata
- **Hook:** balanced brackets and arithmetic expressions: ch. 22 proved no
  automaton recognises them.
- **Recall:** ch. 21--22; Y1 `dynamic-programming`; Y1 trees.
- **Sections:** (1) grammars, derivations, generated languages; expressions,
  propositional formulas and a toy markup as grammars; right-linear grammars
  and regular $\subset$ context-free; (2) parse trees, leftmost and rightmost
  derivations, ambiguity, the dangling `else`, an unambiguous expression
  grammar with precedence levels, weak equivalence; (3) normal forms: removing
  $\varepsilon$- and unit productions, Chomsky normal form and its size;
  (4) the CYK algorithm, its proof and its $O(n^3 |G|)$ cost; counting parse
  trees; (5) pushdown automata: definition, examples; grammar to automaton
  proved, automaton to grammar admitted; (6) the limits: the pumping lemma
  for context-free languages (proved through parse-tree height), $a^n b^n c^n$
  and $ww$; closure (union yes, intersection no, intersection with a regular
  language yes).
- **Statements:** `prop:...:right-linear`, `met:...:cnf` + `prop:...:cnf`,
  `met:...:cyk` + `thm:...:cyk`, `thm:...:cfg-to-pda`,
  `thm:...:pda-to-cfg` (`\admitted`, pointer to the Year 3 volume's parsing
  chapters for the constructive side), `thm:...:pumping`,
  `prop:...:closure`.
- **Listings** (Rust): `grammar.rs` (`NORUN`), `derive.rs` (leftmost
  derivations printed), `cnf.rs`, `cyk.rs` (prints the table),
  `count_trees.rs` (parse-tree counts of $a+a+\dots$: Catalan numbers
  appear), `pda.rs` (nondeterministic run by search, bounded), `markup.rs`
  (the toy markup's grammar and CYK on it).
- **Tests:** crate `tests/grammars/` (CYK agrees with brute-force derivation
  enumeration up to length 8; CNF conversion preserves the language on all
  short words; tree counts equal Catalan numbers).
- **Figures:** S1 two parse trees of one ambiguous expression; S2 the dangling
  `else`'s two trees; S3 a CYK table (from `cyk.rs`'s output); S4 a pushdown
  automaton for $a^n b^n$; S5 a parse tree with a repeated nonterminal on a
  path (the pumping argument).
- **Exercises:** 1★P a leftmost derivation; 2★B a bracket grammar that
  generates `())(`; 3★W a grammar for palindromes; 4★R parse trees of
  $a+a+a+a$ in the ambiguous grammar; 5★★P CYK entries; 6★★B CNF conversion
  that forgets a unit cycle; 7★★W a recogniser for $S \to TS \mid c$,
  $T \to aSb$ written by hand (one function per nonterminal; the technique's
  name is left to Year 3); 8★★R the bracket grammar generates exactly the
  balanced words; 9★★W a PDA for $|w|_a = |w|_b$; 10★★★R $\{ww\}$ is not
  context-free; 11★★★W CYK counting parse trees with big integers, checked
  against Catalan numbers; 12★★★R context-free $\cap$ regular is context-free
  (product construction).
- **Problem:** *The town's markup language.* I a grammar; II ambiguity found
  and removed; III Chomsky normal form and CYK; IV the cost. Named result:
  **"CYK's cubic count: $(n^3 - n)/6$ split points for a word of length
  $n$"** (counted by the program; ~24 q).
- **Ledger:** history: Chomsky 1956; Backus--Naur form in the ALGOL 60 report;
  the CYK algorithm's 1960s origins (Younger 1967).

### 24 `predicate-logic` --- Predicate Logic and Formal Proofs
- **Hook:** "every member who has a book out has a library card" --- a rule
  the town's tables can be checked against, and a rule that can be proved
  from others.
- **Recall:** Y1 `propositional-logic` (formulas as trees, valuations,
  satisfiability, consequence); sets and relations (mathematics); Y1
  structural induction.
- **Sections:** (1) syntax: signatures, terms, atomic formulas, quantifiers,
  free and bound variables, scope, substitution and its capture, renaming;
  (2) semantics: structures, assignments, satisfaction, models, validity,
  consequence; finite structures evaluated by a program (the town's people,
  friendships, loans as a structure); (3) natural deduction for propositional
  logic: sequents, inference rules, proof trees; introduction and elimination
  for $\wedge$, $\vee$, $\to$, $\neg$, $\bot$; classical reasoning (reductio);
  examples (modus ponens, the syllogism, $(p \to q) \to \neg(p \wedge \neg
  q)$); (4) quantifier rules with their side conditions; (5) soundness proved
  by induction on proof trees; completeness stated; (6) what a proof assistant
  checks: a proof checker for propositional natural deduction in Python;
  proof assistants in a `dated` box.
- **Statements:** `lem:...:substitution`, `prop:...:evaluation-cost`
  ($|D|^q \cdot |\varphi|$ for $q$ nested quantifiers), `thm:...:soundness`,
  `thm:...:completeness` (`\admitted`), examples `ex:...:modus-ponens` etc.
- **Listings** (Python): `formulas.py` (`NORUN`: terms, formulas, free
  variables, capture-avoiding substitution), `substitution_demo.py`,
  `evaluate.py` (sentences evaluated on the town's tables; prints the
  counterexamples found), `checker.py` (`NORUN`), `check_demo.py` (three
  proofs accepted, one with a wrong $\forall$-introduction rejected with the
  reason), `proofs.py` (`NORUN`, the proof trees as data).
- **Tests:** `tests/test_formulas.py` (hypothesis: substitution lemma on
  random formulas over a small structure), `tests/test_checker.py`.
- **Figures:** S1 a formula's syntax tree with binding arrows from quantifiers
  to variables; S2--S4 proof trees (needs a proof-tree package, see report);
  S5 a two-element structure that refutes $\forall y \exists x\, R(x,y) \to
  \exists x \forall y\, R(x,y)$.
- **Exercises:** 1★P free variables of five formulas; 2★B a substitution that
  captures; 3★W an evaluator for formulas with $\exists\forall$ prefixes on
  finite structures; 4★R assignments checked by naive evaluation; 5★★P which
  of three structures satisfy a sentence; 6★★B a $\forall$-introduction whose
  variable is free in a hypothesis; 7★★W a proof tree of $\neg(p \vee q)
  \vdash \neg p \wedge \neg q$; 8★★R the soundness cases of $\to$-introduction
  and $\vee$-elimination; 9★★W the checker extended with $\forall$ rules;
  10★★★R $\exists x \forall y\, R \vdash \forall y \exists x\, R$, and a
  countermodel for the converse; 11★★★W excluded middle needs reductio: the
  proof tree; 12★★★R prove the substitution lemma.
- **Problem:** *Checking the library's rules.* I rules as sentences; II
  evaluated on the town's data (violations found); III consequences proved in
  natural deduction; IV checked mechanically. Named result: **"$k$ rules
  proved in $s$ checked steps, and a two-element countermodel for the one
  that does not follow"** (~24 q).
- **Ledger:** history: Frege 1879; Gentzen 1935 (natural deduction); Gödel
  1929/1930 (completeness); proof assistants (`dated`).

## Part VII --- Algorithms II and data

### 25 `text-algorithms` --- Text Algorithms and Compression
- **Hook:** searching the town archive for a phrase, then storing the archive
  in less space.
- **Recall:** g12 `text-search` (naive search, the Horspool shift table);
  ch. 21 automata; Y1 `greedy-proofs` (Huffman codes), `hash-tables`,
  `dynamic-arrays` (the potential method).
- **Sections:** (1) the string-matching problem and the naive cost; Boyer--Moore
  with one shift function (the bad-character rule), re-founded with a proof
  of its correctness; (2) Knuth--Morris--Pratt: borders, the failure
  function, the string-matching automaton, the linear-time proof (potential
  argument); (3) Rabin--Karp: rolling hashes modulo a prime, spurious hits and
  their expected number, several patterns; (4) tries: insertion, search,
  prefix queries; compressed tries and multi-pattern search (told);
  (5) Lempel--Ziv--Welch: encoding, decoding, the case where the code is not
  yet in the decoder's dictionary; ratios measured on generated text against
  Huffman (recalled).
- **Statements:** `prop:...:naive` (worst case $m(n-m+1)$), `prop:...:bad-char`
  (no occurrence is skipped), `thm:...:kmp-linear` (at most $2n - m$
  comparisons), `prop:...:failure` (the failure function in $O(m)$),
  `prop:...:spurious` (expected spurious hits at most $(n-m+1)/q$ for a random
  prime-modulus model, as stated), `prop:...:trie`, `thm:...:lzw` (the decoder
  rebuilds the encoder's dictionary; invariant proof including the special
  case).
- **Listings:** Python `naive.py`, `boyer_moore.py`, `kmp.py` (prints the
  failure table), `kmp_automaton.py`, `rabin_karp.py` (counts spurious hits
  for two moduli), `trie.py` (town street names, autocomplete), `lzw.py`
  (encode, decode, the special case shown), `text_gen.py` (`NORUN`, seeded
  text); C `kmp_bench.c` (MEASURED, adversarial text $a^n b$).
- **Tests:** `tests/test_matching.py` (every matcher equals `str.find` on
  hypothesis-generated texts), `tests/test_lzw.py` (round trip), 
  `tests/test_trie.py`.
- **Figures:** S1 a pattern sliding under a text with the bad-character
  shift; S2 a border and the KMP shift; S3 the KMP automaton of `ababc`
  (from `kmp_automaton.py`); S4 the trie of eight street names (from
  `trie.py`); S5 measured chart naive vs KMP on adversarial text.
- **Exercises:** 1★P the failure table of `aabaaab`; 2★B KMP with a wrong
  index after a mismatch; 3★W all occurrences with Boyer--Moore; 4★R naive
  comparisons on $a^n$ against $a^{m-1}b$; 5★★P LZW encoding by hand;
  6★★B a decoder without the special case; 7★★W autocomplete returning the
  $k$ first completions; 8★★R prove the $2n - m$ bound; 9★★W Rabin--Karp for
  several patterns of one length; 10★★★R the spurious-hit bound;
  11★★★W a multi-pattern matcher (a trie with failure links); 12★★★R LZW on
  $a^n$ emits $\lceil (\sqrt{8n+1}-1)/2 \rceil$ codes.
- **Problem:** *The town archive.* I search; II KMP against naive, counted;
  III a trie for autocomplete; IV compression. Named result: **"LZW on $a^n$:
  exactly $\lceil (\sqrt{8n+1} - 1)/2 \rceil$ codes, and the measured ratio on
  the archive"** (~24 q).
- **Ledger:** history: Knuth, Morris and Pratt 1977; Boyer and Moore 1977;
  Karp and Rabin 1987; Welch 1984 (from Ziv and Lempel 1978).

### 26 `flows-and-matchings` --- Flows and Matchings
- **Hook:** how many buses an hour can leave the town's depot for the
  stadium, if every road carries a limited number?
- **Recall:** Y1 `graph-traversals` (BFS, bipartite graphs), `shortest-paths`.
- **Sections:** (1) flow networks, flows, values; cuts and their capacities;
  a flow never exceeds a cut; (2) residual networks and augmenting paths; the
  Ford--Fulkerson method; termination on integer capacities; integrality;
  (3) the max-flow min-cut theorem; (4) Edmonds--Karp: shortest augmenting
  paths and the $O(VE^2)$ bound (distance-monotonicity lemma); the bad
  example for arbitrary paths; (5) bipartite matchings: the reduction to
  flows, alternating and augmenting paths, Berge's theorem, König's theorem,
  Hall's theorem; (6) problems modelled as flows: edge-disjoint paths
  (Menger), assignment with capacities, a project-selection min cut.
- **Statements:** `prop:...:flow-across-cut`, `cor:...:weak-duality`,
  `met:...:ford-fulkerson`, `thm:...:integrality`, `thm:...:maxflow-mincut`,
  `met:...:edmonds-karp` + `thm:...:edmonds-karp-bound` (with
  `lem:...:monotone`), `thm:...:berge`, `thm:...:konig`, `thm:...:hall`,
  `thm:...:menger`.
- **Listings** (Python): `flow.py` (Edmonds--Karp, prints each augmenting
  path and the final residual reachability = min cut), `bad_example.py`
  (DFS-chosen paths take $2C$ augmentations, BFS takes 2), `town_flow.py`
  (the town's roads, capacities derived from speed limits by a stated rule),
  `matching.py`, `hall.py` (a Hall violator found from the min cut),
  `disjoint_paths.py`, `selection.py`.
- **Tests:** `tests/test_flow.py` (max flow equals min cut on random networks;
  integrality; matching size equals flow value; König equality).
- **Figures:** S1 a network with flow/capacity labels (from `flow.py`); S2
  its residual network; S3 the minimum cut; S4 a bipartite matching with an
  augmenting path; S5 the bad example with capacities $C$ and the middle edge
  1.
- **Exercises:** 1★P is it a flow?; 2★B residual reverse edges missing;
  3★W max flow by hand, then by program; 4★R augmentations of the bad example;
  5★★P the min cut from the final residual; 6★★B a matching search that does
  not reset its marks; 7★★W edge-disjoint routes between two town places;
  8★★R prove the flow-across-cut proposition; 9★★W assigning 40 readers to
  reading-room slots; 10★★★R Hall's theorem from max-flow min-cut;
  11★★★R the distance-monotonicity lemma; 12★★★W a minimum vertex cover from a
  maximum matching, checked equal.
- **Problem:** *The stadium bus plan.* I modelling; II augmenting paths;
  III the bottleneck roads (the cut); IV drivers matched to buses. Named
  result: **"max flow = min cut = $F$ buses an hour, and the cut names the
  roads to widen"** (~24 q).
- **Ledger:** history: Ford and Fulkerson 1956; Edmonds and Karp 1972; König
  1931; Hall 1935; Menger 1927.

### 27 `randomised-algorithms` --- Randomised Algorithms
- **Hook:** quicksort on the already sorted list of town people is quadratic;
  shuffle first, and no input is bad any more.
- **Recall:** mathematics Year 2 (random variables, expectation, linearity,
  independence, the geometric law); Y1 `sorting` (quicksort's average by
  counting), Y1 `hash-tables` (uniform hashing stated there, proved here);
  g9 pseudo-random numbers.
- **Sections:** (1) Las Vegas and Monte Carlo algorithms; expected running
  time is not average-case cost; amplification; (2) randomised quicksort
  (expected comparisons by indicator variables) and quickselect (expected
  linear); (3) universal hashing: the family $((ax + b) \bmod p) \bmod m$
  proved universal (modular arithmetic recalled), expected chain length
  $1 + \alpha$, an adversary defeated; (4) Bloom filters: the false-positive
  rate derived, the best number of hash functions, measured; (5) primality:
  the Fermat test, Carmichael numbers, Miller--Rabin (the $1/4$ bound
  admitted, pointer to the mathematics books' group theory), random primes
  generated (Las Vegas); (6) random choices that approximate: a random
  assignment satisfies half the clauses in expectation, three quarters of
  2-literal clauses (MAX-2SAT); Karger's minimum cut.
- **Statements:** `prop:...:amplification`, `thm:...:quicksort`,
  `thm:...:quickselect`, `thm:...:carter-wegman`, `cor:...:chains`,
  `prop:...:bloom-rate`, `prop:...:fermat`, `thm:...:miller-rabin`
  (`\admitted`), `prop:...:maxsat`, `thm:...:karger`.
- **Listings** (Python): `quicksort_rand.py` (comparisons over 1,000 seeds:
  mean against $2(n+1)H_n - 4n$), `sorted_input.py` (deterministic pivot on
  sorted input: quadratic count), `quickselect.py`, `universal_hash.py`
  (adversarial keys: longest chain for a fixed vs a universal function),
  `bloom.py` (measured rate vs formula; `.dat`), `fermat_mr.py` (561 fools
  Fermat for every base coprime to it; Miller--Rabin catches it),
  `random_prime.py` (trials counted), `maxsat.py`, `karger.py`,
  `shuffle_bias.py` (a wrong shuffle's distribution by exhaustive count).
- **Tests:** `tests/test_random.py` (fixed seeds: exact counts; distribution
  tests by exhaustive enumeration for small $n$), `figures/test_bloom.py`.
- **Figures:** S1 a recursion tree of randomised quicksort with pivots; S2
  chain lengths under an adversary: fixed vs universal (chart); S3 a Bloom
  filter's bits with $k$ positions per key; S4 Bloom: measured
  false-positive rate against the formula (chart); S5 Karger's contractions on
  a small graph.
- **Exercises:** 1★P what a $k$-round Monte Carlo test reports; 2★B a biased
  shuffle (exhaustive count over $n^n$ choices); 3★W reservoir sampling;
  4★R expected trials until success; 5★★P Fermat witnesses of 341; 6★★B a
  Bloom filter whose $k$ functions are correlated; 7★★W a Las Vegas algorithm
  from a Monte Carlo one with a checker; 8★★R $\Pr[i, j \text{ compared}] =
  2/(j - i + 1)$; 9★★W Karger with repetitions; 10★★★R prove Carter--Wegman;
  11★★★R prove Fisher--Yates uniform; 12★★★W a skip list: expected search
  cost measured against $\log_2 n$.
- **Problem:** *The weakest links of the friendship network.* The town's
  friendships form three groups joined by a few bridges (person 40 has no
  friend and is set aside). I contraction by hand; II the bound $2/(n(n-1))$
  proved; III amplification; IV the measured success rate. Named result:
  **"Karger's bound: success at least $2/(n(n-1))$; measured on the town's
  39 connected people"** (~24 q).
- **Ledger:** history: Hoare 1961; Carter and Wegman 1979; Bloom 1970;
  Miller 1976 and Rabin 1980; Karger 1993.

### 28 `search-and-games` --- Search and Games
- **Hook:** a sliding-tile puzzle, and a game of noughts and crosses that
  nobody can lose if both play well.
- **Recall:** Y1 `shortest-paths` (Dijkstra), `heaps`, `backtracking`;
  g10 graphs.
- **Sections:** (1) state spaces: states, actions, goal tests, implicit
  graphs; breadth-first, depth-first and iterative deepening, with costs in
  $b^d$; (2) uniform-cost search, proved; (3) heuristics: admissible and
  consistent; A* and its optimality (admissible for tree search, consistent
  for graph search); heuristics compared on the 8-puzzle (misplaced tiles,
  Manhattan distance); A* on the town's road map with the straight-line
  heuristic (the town's roads are longer than straight lines: admissible);
  (4) two-player reachability games on a graph: positions owned by each
  player, strategies, memoryless winning strategies, attractors computed
  backwards, draws; a matches game solved; (5) minimax with an evaluation
  function, depth-limited; alpha--beta pruning, correctness, best-case leaf
  count; (6) noughts and crosses solved by exhaustive search (the value and
  the number of positions computed).
- **Statements:** `thm:...:ucs`, `prop:...:consistent-admissible`,
  `thm:...:astar-optimal`, `thm:...:attractor` (the attractor is exactly the
  winning set; a memoryless strategy comes with it; linear time with
  counters), `thm:...:alpha-beta` (returns the minimax value),
  `prop:...:best-case` ($b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$
  leaves with perfect ordering).
- **Listings** (Python): `state_space.py` (`NORUN`), `eight_puzzle.py`
  (nodes expanded by BFS and by A* with two heuristics), `town_astar.py`
  (A* vs Dijkstra on the town: nodes expanded, same distance),
  `attractor.py` (a matches game; winning positions printed),
  `tictactoe.py` (value 0; positions counted), `alphabeta.py` (leaves visited
  with and without pruning and ordering, on random trees and on the game).
- **Tests:** `tests/test_search.py` (A* distance equals Dijkstra's on random
  graphs with admissible heuristics), `tests/test_games.py` (attractor equals
  brute-force game values; alpha--beta equals minimax).
- **Figures:** S1 part of the 8-puzzle's state graph; S2 A*'s expanded nodes
  on the town map (coordinates from `places.csv`); S3 a game graph with
  attractor layers; S4 a minimax tree with values; S5 an alpha--beta tree
  with its cut branches. AI illustration: two people at a café table playing
  a board game (generic).
- **Exercises:** 1★P BFS order; 2★B A* with an inadmissible heuristic returns
  a longer route; 3★W iterative deepening; 4★R nodes of a full tree to depth
  $d$; 5★★P a minimax value; 6★★B alpha--beta with bounds not passed down;
  7★★W the attractor of the subtraction game $\{1, 3, 4\}$; 8★★R consistent
  implies admissible; 9★★W Manhattan distance and its admissibility proof;
  10★★★R alpha--beta's correctness; 11★★★W noughts and crosses with
  memoisation and symmetry: distinct positions counted; 12★★★R the
  attractor's linear running time.
- **Problem:** *The delivery robot and its rival.* I the state space; II A*
  on the town; III a two-player game solved backwards; IV alpha--beta
  measured. Named result: **"alpha--beta with good ordering visits $L$ of $N$
  leaves, near the $b^{d/2}$ bound"** (~24 q).
- **Ledger:** history: Hart, Nilsson and Raphael 1968 (A*); von Neumann 1928
  (minimax); Knuth and Moore 1975 (alpha--beta analysis).

### 29 `trees-and-clustering` --- Learning from Examples: Decision Trees and Clustering
- **Hook:** the library wants to predict which loans will come back late.
- **Recall:** g11 `k-nearest-neighbours` (re-founded); mathematics Year 2
  probability; Y1 trees, `spanning-trees` (Kruskal); ch. 27.
- **Sections:** (1) learning as an algorithmic problem: examples, features,
  class labels; supervised and unsupervised; training and test sets;
  confusion matrices and accuracy; overfitting; (2) the $k$-nearest-neighbour
  classifier re-founded with its costs; $k$-d trees: construction by medians,
  nearest-neighbour search with pruning; (3) decision trees: entropy of a
  label distribution, information gain, ID3 on binary splits (thresholds on
  numeric features); depth against test accuracy (overfitting measured);
  (4) $k$-means: Lloyd's algorithm, why it stops, local minima seen over
  seeds, $k$-means++ seeding (told and measured); (5) hierarchical
  agglomerative clustering: linkages, dendrograms, single linkage as a cut of
  the minimum spanning tree.
- **Statements:** `prop:...:knn-cost`, `prop:...:kd-correct`,
  `prop:...:gain-nonneg` (information gain is never negative; binary case
  proved by concavity), `met:...:id3`, `met:...:lloyd`,
  `thm:...:lloyd-stops`, `thm:...:single-linkage`.
- **Data:** generated by the chapter's seeded `dataset.py` (loans with
  features and a planted lateness rule plus noise; points in the plane with
  planted clusters). The town's tables are used for names only. Nothing is
  downloaded.
- **Listings** (Python, standard library only): `dataset.py` (`NORUN`),
  `knn.py`, `kdtree.py` (nodes visited vs brute force), `id3.py` (prints the
  tree), `overfit.py` (`.dat`: depth vs train and test accuracy),
  `confusion.py`, `kmeans.py` (cost per iteration; local minima over seeds),
  `kmeanspp.py` (MEASURED only if timing; otherwise deterministic costs),
  `hac.py` (merge heights; single linkage equals the spanning-tree cut).
- **Tests:** `tests/test_learning.py` (k-d tree NN equals brute force; Lloyd's
  cost never increases; single linkage equals Kruskal's cut; ID3 recovers the
  planted rule on noiseless data).
- **Figures:** S1 a $k$-d tree's partition of the plane (from `kdtree.py`); S2
  the learned decision tree (from `id3.py`); S3 train and test accuracy vs
  depth (chart); S4 $k$-means iterations (three panels); S5 a dendrogram (from
  `hac.py`). AI illustration: a library returns desk with a trolley of books
  (generic).
- **Exercises:** 1★P accuracy from a confusion matrix; 2★B $k$-NN without
  feature scaling; 3★W a $k$-d tree range query; 4★R the information gain of a
  split by hand; 5★★P one Lloyd iteration by hand; 6★★B ID3 splitting on an
  identifier column; 7★★W $k$-fold cross-validation; 8★★R prove Lloyd's cost
  never increases and the algorithm stops; 9★★W complete-linkage clustering;
  10★★★R single linkage equals the spanning-tree cut; 11★★★W $k$-means++
  against random seeding over 100 seeds; 12★★★R a $k$-d tree search that
  visits every node: build the input.
- **Problem:** *Which loans come back late?* I the data and the split; II a
  tree that finds the planted rule; III overfitting with noise; IV members
  clustered. Named result: **"the tree recovers the planted rule at depth 2:
  test accuracy $a$ against a majority baseline of $b$"** (~24 q).
- **Ledger:** history: Quinlan 1986 (ID3); Lloyd (1957 report, 1982 paper);
  Bentley 1975 ($k$-d trees).

### 30 `database-design` --- Database Design: Dependencies, Normal Forms and Transactions
- **Hook:** the library's spreadsheet keeps a member's street on every loan
  line; one move, forty edits, and one forgotten.
- **Recall:** Y1 `relational-model` (relations, keys, relational algebra,
  SQL, entity--relationship modelling); g12 anomalies.
- **Sections:** (1) functional dependencies, implication, Armstrong's axioms
  (sound and complete, proved), attribute closures and their algorithm, keys
  computed from dependencies, minimal covers; (2) normal forms: anomalies,
  third normal form, Boyce--Codd normal form; (3) decomposition: lossless
  joins (Heath's theorem), dependency preservation; BCNF decomposition
  (lossless, may lose a dependency) and 3NF synthesis (lossless and
  preserving); the example with no preserving BCNF decomposition;
  (4) transactions: atomicity, consistency, isolation, durability; commit and
  rollback in SQLite; a failure in the middle rolls back; (5) isolation:
  schedules, the anomalies (dirty read, non-repeatable read, phantom, lost
  update, write skew), the standard isolation levels; seen in a live session
  with two Python connections (lost update by read-modify-write, prevented by
  `BEGIN IMMEDIATE` or by an update expression; a dirty read in shared-cache
  `read_uncommitted` mode); the other anomalies on a schedule simulator,
  because SQLite serialises writers; (6) using an index: `CREATE INDEX`, the
  plan SQLite prints before and after, a measured speed-up (B+ trees and plan
  search in the Year 3 volume).
- **Statements:** `thm:...:armstrong`, `prop:...:closure-algo`,
  `cor:...:key-test`, `thm:...:heath`, `thm:...:bcnf-lossless`,
  `thm:...:3nf-synthesis`, `ex:...:no-preserving-bcnf`.
- **Listings:** Python `fd.py` (`NORUN`: closures, keys, minimal cover, BCNF,
  3NF), `fd_demo.py`; SQL `wide_table.sql` (`-- load: town`, the wide table
  built by a join, then the update anomaly), `decomposed.sql` (the BCNF
  tables; the join gives back the same rows), `transaction.sql`,
  `explain.sql` (`EXPLAIN QUERY PLAN` before and after `CREATE INDEX`);
  Python `rollback.py`, `lost_update.py`, `dirty_read.py`, `schedules.py`
  (anomaly simulator), `index_timing.py` (MEASURED).
- **Tests:** `tests/test_fd.py` (closure by the algorithm equals closure by
  Armstrong saturation on random sets; decompositions lossless by the chase on
  random instances), `tests/test_sql.py` (the decomposition round trip on the
  town).
- **Figures:** S1 dependencies drawn as arrows over a schema's attributes;
  S2 a decomposition tree; S3 two connections' timeline for the lost update;
  S4 measured query times with and without the index (chart). Table (not a
  figure): the isolation levels and the anomalies each allows.
- **Exercises:** 1★P an attribute closure; 2★B a BCNF step that keeps a
  violating dependency; 3★W all candidate keys of a schema; 4★R superkeys of a
  schema with one key of size $k$ among $n$ attributes ($2^{n-k}$);
  5★★P lossless or not, by Heath; 6★★B a Python lost update: fix it two ways;
  7★★W 3NF synthesis; 8★★R the union and decomposition rules from Armstrong's
  axioms; 9★★W the library's schema from the wide table, checked BCNF by
  `fd.py`; 10★★★R prove Heath's theorem; 11★★★R prove the closure algorithm
  correct; 12★★★W the selectivity at which the index stops helping, measured.
- **Problem:** *Redesigning the library's spreadsheet.* I dependencies of the
  wide table; II keys and normal forms; III a lossless decomposition, checked
  on the town's data; IV transactions and an index. Named result: **"from one
  wide table with $k$ anomalies to four BCNF tables with none, and the
  measured gain of one index"** (~24 q).
- **Ledger:** SQLite documentation: isolation in SQLite, `BEGIN IMMEDIATE`,
  shared-cache `read_uncommitted`, `EXPLAIN QUERY PLAN`; the standard isolation
  levels as SQLite or PostgreSQL documents state them; history: Codd 1970,
  3NF 1971, BCNF 1974, Härder and Reuter 1983 (the four letters).

### 31 `project-key-value-server` --- Project: A Key-Value Server
- **Specification (the chapter's first paragraph):** a server on
  `127.0.0.1:44310` keeps a map from string keys to string values; it speaks a
  line-based text protocol (`SET k v`, `GET k`, `DEL k`, `COUNT`, `QUIT`, each
  answered on one line: `OK`, `VALUE v`, `NOTFOUND`, `ERR <reason>`, `COUNT n`);
  it serves many clients at once, survives a restart by replaying an
  append-only log, and is measured under a load test. Written in **Rust**
  (standard library only), because the Year 3 project makes this server
  fault-tolerant in Rust.
- **Recall:** ch. 6--9 (Rust), ch. 15 (locks), ch. 16 (sockets, framing),
  ch. 17 (CRC), ch. 19 (TCP), Y1 `hash-tables`.
- **Milestones (one `\section` each, with listings, outputs, tests):**
  M1 the protocol: a `Command` enum, a parser returning `Result`, unit tests
  for every malformed line; M2 a single-threaded server with `TcpListener`;
  a client; M3 concurrency: a thread per connection, then a fixed thread pool;
  the map behind one `Mutex`, then sharded behind $N$ `RwLock`s; M4
  persistence: log records `len|crc32|command`, append and flush policy,
  replay at start, a truncated last record detected by its CRC and dropped,
  compaction by rewriting; a crash test (the server killed mid-write by the
  test harness); M5 the load test: a seeded client workload, throughput and
  latency percentiles, one lock against sharded (MEASURED); M6 the full test
  suite and what the server does not do (replication, left to Year 3).
- **Statements:** `prop:...:replay` (replaying a log of operations rebuilds
  the map that existed after the last complete record; induction on the
  log), `prop:...:compaction` (the compacted log replays to the same map),
  `prop:...:lock-order` (multi-key operations take shard locks in increasing
  order: no deadlock; recalls ch. 15).
- **Listings** (Rust, one directory of modules): `protocol.rs`, `store.rs`,
  `log.rs`, `server.rs` (`NORUN`), `demo.rs` (starts a server thread and runs
  a scripted client; deterministic transcript), `crash_demo.rs` (writes a torn
  record, restarts, prints what was recovered), `load.rs` (MEASURED).
- **Tests:** crate `tests/kv/` (protocol, store under concurrent clients,
  replay and compaction properties, crash recovery, end-to-end on port
  44311).
- **Figures:** S1 the architecture (listener, pool, shards, log); S2 a log
  record (`bytefield`); S3 crash and replay on a timeline; S4 throughput vs
  client threads for one lock and for 16 shards (chart). AI illustration: a
  server rack in a small machine room (generic).
- **Exercises:** 1★P server replies to a scripted session; 2★B a reader that
  assumes one `read` gives one line; 3★W an atomic `INCR k`; 4★R log size
  after $n$ `SET`s over $k$ keys, before and after compaction; 5★★P outcomes
  of two unlocked clients interleaving `GET`/`SET`; 6★★B `MSET` taking two
  shard locks in either order: deadlock; fix; 7★★W key expiry (`SETEX`);
  8★★R prove the replay proposition with a torn tail; 9★★W snapshot plus log
  tail; 10★★★W an atomic `MSET` across shards with ordered locking, tested
  under load; 11★★★R a throughput model (service time and lock hold time)
  against the measurements; 12★★★W request pipelining in the client, measured.
- **No weekend problem** (project chapter).
- **Ledger:** none new (CRC-32 from ch. 17's row; ports in the book's
  range need no row).

---

## Totals planned (to be re-counted in `PROGRESS.md`)

| Item | Planned |
|---|---|
| Chapters | 31 (30 with a weekend problem, 1 project) |
| Exercises | 372 (12 × 31) |
| Schematics and charts | ~140 (4--6 per chapter) |
| Photographs | ~9 (ch. 11, 12, 17 ×2, 18, and history boxes where a free photograph of a historic machine exists) |
| AI illustrations | ~6 (ch. 15, 17, 20, 28, 29, 31) |
| Listings | ~330 |
| Ledger rows | ~180 |
| Pages | ~450 |

## For the shared docs (Phase A traps)

- A C++ or Rust listing with `main` cannot be included by a test: keep the
  code in a `.hpp` / a module file listed in `NORUN.txt` (C++ tests have no
  `test-with:` line; Rust tests are Cargo crates only).
- `tools/capture_output.py` appends a listing's `args=` after the file name
  (`python -m rv run f.S --trace`), so `rv`'s command line accepts options
  after the file.
- Outputs that depend on scheduling (threads, `recv` sizes, PIDs, inode
  numbers, ephemeral ports) are either MEASURED or not printed.
- `perf` cannot read hardware counters on this kernel (WSL) and `tcpdump`
  needs root: cache effects are measured by timing and simulated; packets are
  built and printed by the book's own code.
