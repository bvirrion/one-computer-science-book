# Series definition map --- One Computer Science Book

Which book and chapter **owns** each defined term, i.e. carries its
`\emph{term}\index{term}` pair inside a `definition`. Owned by the main
session; book writers read it and never edit it (they report at their sync).

Term links are generated **per book**, so a book can only link a term it
defines itself. The rules:

1. **Books 1 and 2 (grades 1--12) never repeat themselves.** Together they
   follow `OUTLINE.md`, "Notion-ownership map, Books 1--2": one owner chapter
   per notion across the twelve school years. A later chapter, in the same
   book or in Book 2, opens with a `recall` box (Book 1's notions are named in
   prose in Book 2: "as Book 1 showed, in grade 8") and uses the word without
   a new `\emph{}\index{}` pair. Book 2 therefore does not link the Book 1
   words it recalls; that is the price of never re-teaching.
2. **Books 3--5 (Years 1--3)**: each notion has exactly **one owner across the
   three university books** (`OUTLINE.md`, "Years 1--3"). A university book
   may **re-found** a school notion --- define it again, rigorously, in the
   chapter the outline names ("Re-founds" column) --- because the school
   books' definitions do not link inside a university book. It never defines a
   notion owned by another university book: it uses the owner's word with a
   prose pointer ("defined in the Year 1 volume"), never a `\cref`.
3. **Notions owned by another series** (`OUTLINE.md`, "Owned by another series
   (recall, then build)") are never defined here at all: a `recall` box names
   the series in prose ("the mathematics books show that\dots"), states what
   is used, and the chapter takes the computing angle. Before defining a term
   that sounds like mathematics or physics (a set, a relation, a matrix, a
   prime, a logarithm, an expectation, a group, a field, a signal, a
   transistor), grep the sister series' harvest (commands below).
4. A term not in any map goes to the **earliest chapter** that needs it: in
   Books 1--2 by grade; across Books 3--5 in the lowest-numbered university
   book. Contested terms are settled at a sync by the main session, and the
   ruling is written below.
5. **Harvester rule**: `\index{}` appears only beside the `\emph{}` of a term
   the chapter owns, inside a `definition`, and nowhere else. Named theorems
   and algorithms this series owns (the master theorem, Dijkstra's algorithm,
   Kleene's theorem, the Cook--Levin theorem) may be indexed in their theorem
   or method, owner chapter only. A term in `\code{}` is never harvested
   (the linker masks code), so a definition of a keyword names it in words:
   ``a \emph{for loop}\index{for loop}'' with \code{for} beside it.
6. **One sense per word in a book.** Computer science reuses everyday words:
   a *key* (keyboard, dictionary, primary, cryptographic), a *table* (data,
   hash, truth, routing, page), a *heap* (a structure, a memory region), a
   *stack* (a structure, the call stack), a *node*, a *root*, a *path* (a
   file path, a path in a graph), a *word* (a machine word, a word of a
   language), a *frame* (a stack frame, a network frame), a *page*, a *block*,
   a *cell*, a *port*, a *register*, a *record*, a *field*, a *string*. When a
   book needs two senses, the definition names the qualified form (*hash
   table*, *call stack*, *file path*, *machine word*, *stack frame*) and the
   writer adds the bare word to its term config's `STOP` or `EXTRA_PROTECT` in
   Phase C, so a link never lands on the wrong sense.

## Harvest commands

```sh
# this series, one book's years at a time
perl -0777 -ne 'while(/\\emph\{([^}]*)\}\s*\\index\{([^}]*)\}/g){($t=$2)=~s/\s+/ /g; print "$ARGV\t$t\n"}' parts/grade-*/[0-9]*.tex
perl -0777 -ne 'while(/\\emph\{([^}]*)\}\s*\\index\{([^}]*)\}/g){($t=$2)=~s/\s+/ /g; print "$ARGV\t$t\n"}' parts/bachelor-*/[0-9]*.tex
# the sister series (read-only): what they own
for s in math physics; do
  perl -0777 -ne 'while(/\\emph\{([^}]*)\}\s*\\index\{([^}]*)\}/g){($t=$2)=~s/\s+/ /g; print "$ARGV\t$t\n"}' \
    ../one-$s-book/parts/*/[0-9]*.tex
done | grep -i '<term>'
# the AI series (an extra shelf for readers who already program: named in prose only)
perl -0777 -ne 'while(/\\emph\{([^}]*)\}\s*\\index\{([^}]*)\}/g){($t=$2)=~s/\s+/ /g; print "$ARGV\t$t\n"}' \
  ../one-artificial-intelligence-book/parts/*/[0-9]*.tex | grep -i '<term>'
```

## Seed (2026-11-19)

The binding seed is `OUTLINE.md`'s three ownership tables, approved by the user
on 2026-11-19. They are not copied here, so that they cannot drift; the sync
below adds only what the tables do not say.

Points the outline already settles and every writer must know:

- **Mathematics owns** (recall, never define): powers of two (g8), divisors,
  primes and Euclid's algorithm (g9), probability and frequencies (g9), mean,
  median and spread (g10), proof by induction (g12), the logarithm (g12),
  counting (g12, Y1), modular arithmetic, fast powers and the miniature RSA
  (g12, Y1), matrices and the adjacency matrix (g12), truth tables, sets,
  maps and relations (Y1), comparison of sequences (Y1), Gaussian elimination,
  discrete probability and expectation (Y2), groups, rings and finite fields
  (Y3). Note: Book 1 grade 9 `logic-gates` teaches truth tables of gates for
  the machine before the mathematics book's Year 1 logic; it owns *truth
  table of a gate* and *logic gate*, not propositional logic.
- **Physics owns**: the electric circuit and the switch (g3--g8), signals
  (g10), refraction and the optical fibre (g10), the sampling theorem and
  analog-to-digital conversion (Y2), semiconductors and the transistor (Y3).
  The transistor is *told* here as an electrically controlled switch.
- **Earth and space sciences owns** satellite positioning (g9).
- **The AI series owns** machine learning beyond the three algorithm chapters
  (g11 `k-nearest-neighbours`, Y2 `search-and-games`, Y2
  `trees-and-clustering`), which this series owns for itself.

## Sync decisions (2026-11-20)

The five `sources/book<N>/DEFINITIONS.md` files of Phase A are the detailed lists. These rulings settle every
term two books claimed or one book asked about; where a book's file disagrees, the ruling wins. A term not
named here stays where that book's `DEFINITIONS.md` puts it.

### School books (Books 1 and 2)

| Term | Owner | Notes |
|---|---|---|
| byte (unit of size) | Book 1 g4/01 | bit, and "a byte is 8 bits", in g5/01 |
| trace table | Book 1 g6/02 | debugging and tracing with `print` in g7/05 |
| interpreter | Book 1 g6/01 | Book 1 never defines *compiler* |
| compiler | Book 2 g12-13 | Book 3 re-founds compilation |
| character code, code table | Book 1 g5/02 | ASCII named in a history box only |
| ASCII, one-byte extensions | Book 2 g10-05 | |
| resolution | Book 1 g5 | Book 2 recalls |
| authentication | Book 1 g5/03 | Book 2 recalls; Book 5 may re-found it rigorously |
| string method | Book 1 g7/03 | *method* (objects) is Book 2 g12 |
| folder tree (g3), document tree (g9) | Book 1 | bare *tree* is Book 2 g12-04 |
| class of an HTML element | Book 1 g9/01 | *class* (programming) is Book 2 g12 |
| machine language, instruction | Book 1 g7 | |
| assembly language, assembler, label | Book 2 g11-02 | Book 1 avoids the words |
| specification | Book 2 g10 | Book 1 uses the word in prose only |
| full adder, routing table, network mask, event, permissions, sensor, actuator | Book 2 | Book 1 tells, never defines |
| protocol | Book 2 g10-08 | g11-04 owns *layer*, *encapsulation*, *peer-to-peer* |
| port number | Book 2 g10-08 | Book 1 says "port" for a connector in prose, no definition |
| sampling rate, bit depth | Book 2 g10-06 | *sampling* itself is physics's: told in prose |
| side effect | Book 2 g10-01 | Book 3 ch. 2 re-founds it |
| paradigm, pure function | Book 2 g12-02 | *higher-order function* is Book 4's |
| interrupt | Book 2 g12-10 | Book 5 re-founds it with *trap* |
| network switch, network interface, bit rate | Book 1 g8/05 | |
| random walk | mathematics | prose only |

**"Key" in Book 1** has three senses (keyboard g2/01, dictionary g8/02, encryption g9/06). The nearest-preceding
policy handles g2–g9; the typing appendix, which comes last, needs a protect rule in `book1_en.py`.

### University books (Books 3, 4 and 5)

| Term | Owner | Notes |
|---|---|---|
| byte order, sign extension | Book 3 ch. 6 | Book 4 recalls (Book 2 owns two's complement at school) |
| return address | Book 3 ch. 3 | |
| exit status, environment variable, hard link, symbolic link | Book 3 ch. 8 | Book 4 owns inode, link count, built-in command |
| signal, file descriptor | Book 4 | *process*, *system call*, *race condition*, *critical section*, *mutual exclusion* and *lock* are Book 2 g12-10's: Book 4 ch. 13 and 15 recall them in remarks (2026-11-21, R4-040/045); Book 3 says "running program" in prose |
| pipeline (shell) | Book 3 ch. 8 | *pipe* (kernel object) is Book 4's |
| iterator | Book 3 ch. 15 | Book 4: iterator ranges, categories, invalidation, *lazy iterator* |
| cut of a graph | Book 3 ch. 26 | Book 4: cut of a flow network, its capacity |
| datapath, control unit | Book 3 ch. 28 | |
| control-flow graph, statement/branch/path coverage | Book 3 ch. 7 | Book 5 recalls |
| branch and bound | Book 3 ch. 20 | Book 5 recalls |
| graph colouring, unit propagation, prefix code, buffer overflow, unit test | Book 3 | Book 5 recalls |
| model (of a formula), logical equivalence, logical consequence | Book 3 propositional logic | Book 4 defines the first-order forms by their qualified names |
| constructor (of an abstract type) | Book 3 | Book 4's *constructor* is the C++ member function: name the sense in the definition |
| variant (of a loop, for termination) | Book 3 | Book 4's Rust *enum variant*: name the sense |
| comparison tree, maximum overlap, longest delay path, input class | Book 3 | renamed to avoid clashes |
| logic gate | Book 1 | no university book redefines it; Book 3 ch. 27 recalls it |
| atomic operation (informal) | Book 4 | Book 5: compare-and-swap, memory orderings, memory model |
| LRU | Book 4 | Book 5 recalls |
| TLS (as a layer) | Book 4 | Book 5: certificate, the handshake's cryptography |
| vertex cover | Book 4 | Book 5 recalls |
| entropy, information gain | Book 4 (decision trees) | the outline gave entropy to Y3: changed; Book 5 recalls and builds codes on it |
| schedule (of transactions), isolation level, index | Book 4 | Book 5 recalls |
| free variable, bound variable, starvation, data race | Book 4 | Book 5 recalls |
| resolution, unification | Book 4 predicate logic | Book 5 recalls (logic programming, Horn-SAT) |
| subtype polymorphism, static polymorphism, abstract class | Book 4 | bare *interface* is not defined |
| parametric polymorphism | Book 5 | |
| decision problem, recursive descent, query plan, reference counting, trap, certificate, lazy evaluation | Book 5 | Book 4 uses the words without defining them, or avoids them |
| deadlock, interrupt | Book 2 g12-10 | Book 5 re-founds them at university rigour (deadlock with livelock and the Coffman conditions, ch. 13; interrupt with trap, ch. 10); Book 4 uses the words without defining them |
| Amdahl's law, speed-up | Book 5 | Book 4's pipelining chapter does not name Amdahl |

A university book never `\cref`s another: "defined in the Year 1 volume" in prose.
