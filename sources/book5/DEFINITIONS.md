# Book 5 (`bachelor-3`, `b3`) — terms the book defines

Phase A, 2026-11-20; brought in line with the sync rulings (`sources/SERIES_DEFINITIONS.md`, "Sync decisions") the same day. Each row is one `definition` environment: its label, and the terms it carries as
`\emph{}\index{}` pairs (owner chapter only). Notes: **R** = re-founds a school notion (allowed by
`OUTLINE.md`'s "Re-founds" column); **Q** = qualified form chosen because the bare word has another sense
in this book or is owned elsewhere (bare word goes to `STOP`/`EXTRA_PROTECT` in Phase C); **C** = contested
with another book or series, see the list at the end. Everything not listed here is recalled in prose
("defined in the Year 1 volume", "as the mathematics books show") and never re-defined.

Before each chapter the harvest of `sources/SERIES_DEFINITIONS.md` is re-run over the other books' files and
the sister series; a clash found then is reported, not silently resolved.

## Part I — Compilers and programming languages

| Ch. | Label | Terms | Notes |
|---|---|---|---|
| 1 | `def:b3:lexical-analysis:phases` | compiler phase, front end, back end | |
| 1 | `def:b3:lexical-analysis:token` | token, lexeme, token class | Q: *token* means lexer token in this book; ch. 29 says *session token* |
| 1 | `def:b3:lexical-analysis:scanner` | scanner, span | |
| 1 | `def:b3:lexical-analysis:munch` | maximal munch, priority rule | "longest match" as a synonym in prose |
| 1 | `def:b3:lexical-analysis:generator` | scanner generator | |
| 2 | `def:b3:top-down-parsing:ast` | abstract syntax tree | earliest use is ch. 2 (the parser builds it); ch. 4 recalls |
| 2 | `def:b3:top-down-parsing:first-follow` | nullable, FIRST set, FOLLOW set | |
| 2 | `def:b3:top-down-parsing:ll1` | LL(1) grammar, predictive parsing table | |
| 2 | `def:b3:top-down-parsing:left-recursion` | left recursion, left factoring | |
| 2 | `def:b3:top-down-parsing:descent` | recursive descent | sync: Book 5 owns |
| 2 | `def:b3:top-down-parsing:precedence` | precedence climbing, binding power | |
| 2 | `def:b3:top-down-parsing:recovery` | panic-mode recovery, synchronising token | |
| 3 | `def:b3:bottom-up-parsing:shift-reduce` | shift–reduce parsing, handle | |
| 3 | `def:b3:bottom-up-parsing:items` | LR(0) item, item closure, goto function | Q: *closure* is Y2's (functions); the term here is *item closure* |
| 3 | `def:b3:bottom-up-parsing:automaton` | viable prefix, LR(0) automaton | |
| 3 | `def:b3:bottom-up-parsing:slr` | SLR table, shift–reduce conflict, reduce–reduce conflict | |
| 3 | `def:b3:bottom-up-parsing:lr1` | LR(1) item, LALR table | |
| 3 | `def:b3:bottom-up-parsing:generator` | parser generator | |
| 4 | `def:b3:semantic-analysis:scope` | lexical scope, shadowing, dynamic scope | Q: bare *scope* is ordinary (Y1 uses it for C) |
| 4 | `def:b3:semantic-analysis:symbol-table` | symbol table | |
| 4 | `def:b3:semantic-analysis:resolution` | name resolution, binding occurrence | Q: *binding* alone collides with Rust/λ senses |
| 4 | `def:b3:semantic-analysis:static-semantics` | static semantics, type checking | |
| 4 | `def:b3:semantic-analysis:error-type` | error type | |
| 4 | `def:b3:semantic-analysis:interpreter` | tree-walking interpreter | Q: bare *interpreter* is school/Y1 |
| 5 | `def:b3:lambda-calculus:terms` | λ-term, abstraction, application (of λ-terms) | free and bound variables are Book 4's (`def:b2:predicate-logic:free`): recalled, applied to λ-terms in prose |
| 5 | `def:b3:lambda-calculus:alpha` | α-equivalence, capture-avoiding substitution | |
| 5 | `def:b3:lambda-calculus:debruijn` | de Bruijn index | |
| 5 | `def:b3:lambda-calculus:beta` | β-reduction, redex, normal form (of a λ-term) | Q: *normal form* is also Y1 (formulas) and Y2 (databases) |
| 5 | `def:b3:lambda-calculus:strategy` | evaluation strategy, call by value, call by name, normal-order reduction, lazy evaluation (call by need) | Book 4 asks Y3 to own *lazy evaluation* (it owns *lazy iterator*) |
| 5 | `def:b3:lambda-calculus:rewriting` | term rewriting system, confluence | |
| 5 | `thm:b3:lambda-calculus:church-rosser` / `lem:b3:lambda-calculus:newman` | Church–Rosser theorem, Newman's lemma (indexed in the statements) | named results |
| 5 | `def:b3:lambda-calculus:church` | Church numeral, Church boolean | |
| 5 | `def:b3:lambda-calculus:fixpoint` | fixed-point combinator | Q: math g10 owns *fixed point* |
| 5 | `def:b3:lambda-calculus:semantics` | operational semantics, small-step semantics, big-step semantics | |
| 6 | `def:b3:type-systems:judgement` | typing context, typing judgement, typing derivation, typing rule | |
| 6 | `def:b3:type-systems:stlc` | simply typed λ-calculus | |
| 6 | `def:b3:type-systems:safety` | type safety, progress, preservation, canonical form | |
| 6 | `def:b3:type-systems:polymorphism` | type variable, type scheme, parametric polymorphism, let-polymorphism | Q: Y2 owns *polymorphism* (OO) |
| 6 | `def:b3:type-systems:unification` | type substitution, type equation | sync: *unification*, *unifier*, *most general unifier* (and the occurs check with them) are Book 4's (predicate logic): recalled and applied to types |
| 6 | `def:b3:type-systems:inference` | type inference, principal type | |
| 6 | `def:b3:type-systems:curry-howard` | Curry–Howard correspondence | |
| 6 | `def:b3:type-systems:linear` | linear type, affine type | told, for ownership |
| 6 | (umbrella) | type system | OUTLINE: Y3 `type-systems` owns it |
| 7 | `def:b3:code-generation:ir` | intermediate representation, three-address code, temporary | Q: *temporary* defined as *virtual register* synonym |
| 7 | `def:b3:code-generation:cfg` | basic block, leader | sync: *control-flow graph* is Book 3's (ch. 7): recalled; Q: *block* bare = disk block (ch. 12) |
| 7 | `def:b3:code-generation:selection` | instruction selection, tiling | |
| 7 | `def:b3:code-generation:frame` | frame layout, spill slot | stack frame itself is Y1's (recalled) |
| 7 | `def:b3:code-generation:codegen` | code generator, compiler correctness | |
| 8 | `def:b3:program-optimisation:lattice` | dataflow lattice, monotone framework, transfer function, least fixed point | Q/C: *lattice* and *partial order* are mathematics' (grep at the chapter); the qualified *dataflow lattice* is ours |
| 8 | `def:b3:program-optimisation:worklist` | worklist algorithm | |
| 8 | `def:b3:program-optimisation:liveness` | live variable, liveness analysis, reaching definition | |
| 8 | `def:b3:program-optimisation:ssa` | static single assignment form, φ-function | |
| 8 | `def:b3:program-optimisation:dominance` | dominator, immediate dominator, dominance frontier | |
| 8 | `def:b3:program-optimisation:opts` | constant propagation, copy propagation, value numbering, dead code | |
| 8 | `def:b3:program-optimisation:regalloc` | interference graph, register allocation, spill, register coalescing | |
| 8 | `def:b3:program-optimisation:colouring` | (none) | sync: *graph colouring* is Book 3's: recalled; *chromatic number* told in prose |
| 9 | `def:b3:garbage-collection:allocator` | allocator, free list, first fit, best fit, boundary tag | |
| 9 | `def:b3:garbage-collection:fragmentation` | external fragmentation, internal fragmentation, coalescing of free blocks | |
| 9 | `def:b3:garbage-collection:refcount` | reference counting, reference count | Book 4 describes the count in `cpp-copy-move` without defining it (its proposal) |
| 9 | `def:b3:garbage-collection:reachability` | root set, reachable object, garbage | |
| 9 | `def:b3:garbage-collection:marksweep` | garbage collection, mark and sweep, tri-colour invariant | |
| 9 | `def:b3:garbage-collection:copying` | copying collector, forwarding pointer | |
| 9 | `def:b3:garbage-collection:generational` | generational collection, write barrier, remembered set | |

## Part II — Operating systems

| Ch. | Label | Terms | Notes |
|---|---|---|---|
| 10 | `def:b3:kernel-and-scheduling:kernel` | kernel, monolithic kernel, microkernel | R: g11 `os-and-command-line` |
| 10 | `def:b3:kernel-and-scheduling:interrupt` | interrupt, trap, hardware exception, interrupt vector, timer interrupt | sync: Book 5 re-founds *interrupt* (Book 2 g12 owns it at school) and owns *trap*; Q: *exception* bare is Book 4's C++ sense |
| 10 | `def:b3:kernel-and-scheduling:switch` | preemption, context switch, process control block | R: g12 `processes-and-scheduling` (context switch) |
| 10 | `def:b3:kernel-and-scheduling:metrics` | turnaround time, waiting time, response time | |
| 10 | `def:b3:kernel-and-scheduling:policies` | scheduling policy, first come first served, shortest job first, shortest remaining time first, time slice | R: g12 (scheduler, round robin) |
| 10 | `def:b3:kernel-and-scheduling:mlfq` | multilevel feedback queue | |
| 10 | `def:b3:kernel-and-scheduling:share` | fair-share scheduling, lottery scheduling, stride scheduling | |
| 10 | `def:b3:kernel-and-scheduling:realtime` | real-time scheduling, deadline, rate-monotonic scheduling, earliest deadline first | |
| 11 | `def:b3:virtual-memory:space` | virtual memory, address space, virtual address, physical address | |
| 11 | `def:b3:virtual-memory:paging` | page, page frame, page table, page-table entry, multi-level page table | Q: *page* = memory page; ch. 21 says *database page*; *frame* bare is Y1/Y2 |
| 11 | `def:b3:virtual-memory:tlb` | translation lookaside buffer, TLB reach, address-space identifier | not in Book 4's map |
| 11 | `def:b3:virtual-memory:fault` | page fault, demand paging | |
| 11 | `def:b3:virtual-memory:replacement` | optimal replacement (OPT), clock algorithm, second-chance bit | *replacement policy* and *LRU* are Book 4's (`def:b2:caches:lru`): recalled for pages |
| 11 | `def:b3:virtual-memory:belady` | Belady's anomaly, stack algorithm | |
| 11 | `def:b3:virtual-memory:working-set` | working set, thrashing | |
| 11 | `def:b3:virtual-memory:cow` | copy on write, memory-mapped file | |
| 12 | `def:b3:file-systems:disk` | disk block, sector, seek time, rotational latency | Q: *block* = disk block in Part II |
| 12 | `def:b3:file-systems:disk-scheduling` | disk scheduling, SCAN algorithm | |
| 12 | `def:b3:file-systems:flash` | erase block, flash translation layer, wear levelling, write amplification | |
| 12 | `def:b3:file-systems:layout` | superblock, block bitmap, inode table, direct block, indirect block, directory entry | inode itself is Y2's (recalled) |
| 12 | `def:b3:file-systems:consistency` | crash consistency, journaling, idempotent replay | Q: *journal* in ch. 12 vs *write-ahead log* in ch. 23 (two qualified terms) |
| 12 | `def:b3:file-systems:lfs` | log-structured file system, segment cleaning | |
| 12 | `def:b3:file-systems:raid` | RAID, striping, mirroring, parity block | |
| 13 | `def:b3:concurrency:properties` | safety property, liveness property | |
| 13 | `def:b3:concurrency:deadlock` | deadlock, livelock, Coffman conditions | R: g12; Book 4 uses *deadlock* undefined (agreed) and owns *starvation* (recalled) |
| 13 | `def:b3:concurrency:rag` | resource-allocation graph, lock ordering | |
| 13 | `def:b3:concurrency:banker` | safe state, banker's algorithm, deadlock detection | |
| 13 | `def:b3:concurrency:monitor` | monitor, Mesa semantics, Hoare semantics | |
| 13 | `def:b3:concurrency:memory-model` | memory model, sequential consistency, happens-before order (memory) | *data race* is Book 4's (`def:b2:threads-and-synchronisation:race`): recalled; Q: ch. 25 owns *happened-before relation* (messages): the memory one is named *happens-before order* in a remark only, not indexed, to keep one sense |
| 13 | `def:b3:concurrency:atomics` | compare-and-swap, read-modify-write operation, acquire ordering, release ordering | C: *atomic operation* — Book 4 defines it informally (indivisible step) for Peterson; proposal: Book 4 owns it, Book 5 recalls and owns the rest |
| 13 | `def:b3:concurrency:lock-free` | lock-free, wait-free, ABA problem | |
| 13 | `def:b3:concurrency:linearisability` | linearisability, linearisation point | |
| 14 | `def:b3:virtualisation:vm` | system virtual machine, hypervisor, type-1 hypervisor, type-2 hypervisor, guest, host | Q: *virtual machine* only in this sense in Book 5 |
| 14 | `def:b3:virtualisation:sensitive` | sensitive instruction, privileged instruction, trap and emulate | |
| 14 | `thm:b3:virtualisation:popek-goldberg` | Popek–Goldberg theorem (indexed in the theorem) | |
| 14 | `def:b3:virtualisation:techniques` | binary translation, paravirtualisation, nested paging | |
| 14 | `def:b3:virtualisation:container` | container, kernel namespace, control group, resource limit | Q: Y2 C++ owns *namespace* |
| 14 | `def:b3:virtualisation:isolation` | isolation boundary | |

## Part III — Theory of computation

| Ch. | Label | Terms | Notes |
|---|---|---|---|
| 15 | `def:b3:computability:tm` | Turing machine, configuration, transition function (of a Turing machine) | Q: Y2 automata use *transition function*; qualified here |
| 15 | `def:b3:computability:languages` | decider, decidable language, recognisable language | R: g12 `halting-problem` (decidable problem); Book 4 uses "decision problem" in prose only (agreed) |
| 15 | `def:b3:computability:multitape` | multi-tape Turing machine | |
| 15 | `def:b3:computability:thesis` | Church–Turing thesis | |
| 15 | `def:b3:computability:recursive` | primitive recursive function, μ-recursive function, Ackermann function | |
| 15 | `def:b3:computability:universal` | encoding of a machine, universal Turing machine | |
| 15 | `def:b3:computability:halting` | halting problem | R: g12 |
| 15 | `def:b3:computability:reduction` | many-one reduction | |
| 15 | `def:b3:computability:rice` | semantic property, non-trivial property; Rice's theorem (in the theorem) | |
| 15 | `def:b3:computability:pcp` | Post correspondence problem | told |
| 15 | `def:b3:computability:busy-beaver` | busy beaver function | |
| 16 | `def:b3:complexity-classes:decision` | decision problem, instance size | Book 4 agrees |
| 16 | `def:b3:complexity-classes:classes` | time complexity class, space complexity class, class P | |
| 16 | `def:b3:complexity-classes:np` | certificate, verifier, class NP, nondeterministic Turing machine | |
| 16 | `def:b3:complexity-classes:self-reducibility` | self-reducibility | |
| 16 | `thm:b3:complexity-classes:hierarchy` / `thm:b3:complexity-classes:savitch` | time hierarchy theorem, space hierarchy theorem, Savitch's theorem | named results |
| 16 | `def:b3:complexity-classes:pspace` | EXP, PSPACE, TQBF | |
| 16 | `def:b3:complexity-classes:logspace` | class L, class NL, log-space reduction | |
| 17 | `def:b3:np-completeness:reduction` | polynomial-time reduction, NP-hard, NP-complete | |
| 17 | `thm:b3:np-completeness:cook-levin` | Cook–Levin theorem | named result |
| 17 | `def:b3:np-completeness:problems` | 3-SAT, independent set, clique, Hamiltonian cycle, subset sum problem | *vertex cover* is Book 4's (`def:b2:flows-and-matchings:vertex-cover`, first needed for König): recalled; *3-SAT* builds on Book 3's *k-SAT*: if Book 3 owns k-SAT, ch. 17 recalls it and owns nothing for 3-SAT; mathematics owns no *clique* or *Hamiltonian cycle* (grep 2026-11-20; physics' *Hamiltonian* is another sense) |
| 17 | `def:b3:np-completeness:gadget` | gadget | |
| 17 | `def:b3:np-completeness:conp` | co-NP | |
| 17 | `def:b3:np-completeness:2sat` | 2-SAT, implication graph (of a 2-CNF formula) | Q: ch. 18 says *solver implication graph* |
| 17 | `def:b3:np-completeness:pseudo` | pseudo-polynomial algorithm, strongly NP-complete | |
| 18 | `def:b3:hard-problems:approximation` | approximation algorithm, approximation ratio, maximal matching | Book 4 has a MAX-SAT proposition but defines no *approximation algorithm*: Book 5 owns; *matching* is Book 4's, *maximal* matching qualified here |
| 18 | `def:b3:hard-problems:set-cover` | set cover problem | |
| 18 | `def:b3:hard-problems:tsp` | metric travelling salesman problem, tree doubling | |
| 18 | `def:b3:hard-problems:inapproximability` | inapproximability | |
| 18 | `def:b3:hard-problems:relaxation` | relaxed problem, relaxation bound | Q: Book 3 owns *relaxation (of an edge)* (shortest paths); branch and bound is Book 3's |
| 18 | `def:b3:hard-problems:cdcl` | watched literals, solver implication graph, conflict clause, clause learning, unique implication point, backjumping, CDCL solver | *unit propagation* is Book 3's (`propositional-logic`, with Quine's algorithm): recalled |
| 18 | `def:b3:hard-problems:horn` | Horn clause, Horn-SAT, forward chaining | |
| 18 | `def:b3:hard-problems:local-search` | local search, 2-opt move, WalkSAT | |
| 19 | `def:b3:information-and-codes:entropy` | self-information, entropy of a source (block entropy) | C: Book 4 `trees-and-clustering` proposes to own *entropy of a finite distribution* (ID3 needs it first); accepted: ch. 19 recalls it and owns the source and coding terms; physics owns thermodynamic entropy |
| 19 | `def:b3:information-and-codes:prefix` | Kraft inequality, uniquely decodable code | *prefix code* and *cost of a code* are Book 3's (`greedy-proofs`): recalled |
| 19 | `thm:b3:information-and-codes:source-coding` | source-coding theorem | |
| 19 | `def:b3:information-and-codes:channel` | binary symmetric channel, channel capacity, repetition code | |
| 19 | `thm:b3:information-and-codes:noisy-channel` | noisy-channel coding theorem | |
| 19 | `def:b3:information-and-codes:distance` | Hamming distance, minimum distance, error-correcting code | not in Book 4's map; error-detecting code is Book 4's |
| 19 | `def:b3:information-and-codes:linear` | linear code, generator matrix, parity-check matrix, syndrome | |
| 19 | `def:b3:information-and-codes:hamming` | Hamming code, perfect code, sphere-packing bound | |
| 19 | `def:b3:information-and-codes:cyclic` | cyclic code, Reed–Solomon code | CRC is Book 4's (recalled) |
| 20 | `def:b3:program-verification:hoare` | Hoare triple, Hoare logic, assignment axiom, rule of consequence | |
| 20 | `def:b3:program-verification:wp` | weakest precondition, strongest postcondition | |
| 20 | `def:b3:program-verification:vc` | annotated program, verification condition, bit-blasting | |
| 20 | `def:b3:program-verification:kripke` | Kripke structure, temporal logic, computation tree logic, linear temporal logic | |
| 20 | `def:b3:program-verification:mc` | model checking, counterexample trace, state explosion | |

## Part IV — Data and distributed systems

| Ch. | Label | Terms | Notes |
|---|---|---|---|
| 21 | `def:b3:database-storage:page` | database page, slotted page, record identifier | Q |
| 21 | `def:b3:database-storage:buffer` | buffer pool, pin count, dirty page | |
| 21 | `def:b3:database-storage:bptree` | B+ tree, order (of a B+ tree), fill factor, node split, bulk loading | |
| 21 | `def:b3:database-storage:index` | clustered index, secondary index, covering index | *index (database)* is Book 4's (`def:b2:database-design:index`): recalled; Book 4 leaves *query plan* and the B+ tree to Book 5 |
| 21 | `def:b3:database-storage:hashing` | static hashing, extendible hashing, linear hashing | |
| 21 | `def:b3:database-storage:lsm` | log-structured merge tree, memtable, sorted run, read amplification | write amplification is ch. 12's; *compaction* is Book 4's (`def:b2:project-key-value-server:log`): recalled (changed 2026-11-20) |
| 22 | `def:b3:query-optimisation:plan` | query plan, physical operator, access path | |
| 22 | `def:b3:query-optimisation:sort` | external merge sort | |
| 22 | `def:b3:query-optimisation:joins` | nested-loop join, block nested-loop join, index nested-loop join, sort–merge join, hash join | |
| 22 | `def:b3:query-optimisation:estimates` | selectivity, cardinality estimate, equi-depth histogram | Q: math owns *histogram* |
| 22 | `def:b3:query-optimisation:search` | left-deep plan, interesting order, cost-based optimiser | |
| 23 | `def:b3:transactions-and-recovery:schedule` | conflicting operations, conflict serialisability, precedence graph, view serialisability, serial schedule | *schedule (of transactions)* is Book 4's (its proposal, needed for anomalies): recalled |
| 23 | `def:b3:transactions-and-recovery:2pl` | two-phase locking, strict two-phase locking, cascading abort, recoverable schedule | |
| 23 | `def:b3:transactions-and-recovery:deadlock` | wait-for graph, wound–wait, wait–die | |
| 23 | `def:b3:transactions-and-recovery:mvcc` | multiversion concurrency control, snapshot isolation, serialisable snapshot isolation | *write skew* is Book 4's (`def:b2:database-design:anomalies`): recalled (changed 2026-11-20) |
| 23 | `def:b3:transactions-and-recovery:isolation` | predicate lock | *isolation level* and *phantom read* are Book 4's (`def:b2:database-design:isolation-level`, `:anomalies`): recalled; ch. 23 maps the levels to mechanisms (changed 2026-11-20) |
| 23 | `def:b3:transactions-and-recovery:wal` | write-ahead log, undo record, redo record, log sequence number, checkpoint | Q: *log* bare collides with *replicated log* (ch. 26) |
| 23 | `def:b3:transactions-and-recovery:trigger` | trigger | only if no other book defines it |
| 24 | `def:b3:parallel-programming:speedup` | speed-up, efficiency (parallel) | sync: Book 5 owns *speed-up* |
| 24 | `thm:b3:parallel-programming:amdahl` / `gustafson` | Amdahl's law, Gustafson's law | C: Book 4 `processor-and-pipelining` might state Amdahl's law |
| 24 | `def:b3:parallel-programming:kinds` | task parallelism, data parallelism, fork–join | |
| 24 | `def:b3:parallel-programming:workspan` | work, span, parallelism (ratio) | Q: bare *work* is everyday; definition names *work of a computation*; STOP |
| 24 | `thm:b3:parallel-programming:brent` | Brent's theorem | |
| 24 | `def:b3:parallel-programming:scheduler` | greedy scheduler, work stealing | |
| 24 | `def:b3:parallel-programming:scan` | parallel reduction, prefix sum | |
| 24 | `def:b3:parallel-programming:false-sharing` | false sharing | C: Book 4 `caches` may define it |
| 24 | `def:b3:parallel-programming:simd` | SIMD, vectorisation | |
| 25 | `def:b3:distributed-systems:model` | distributed system, synchronous system, asynchronous system | |
| 25 | `def:b3:distributed-systems:failures` | crash failure, omission failure, Byzantine failure, failure detector | |
| 25 | `def:b3:distributed-systems:generals` | two generals problem | |
| 25 | `def:b3:distributed-systems:rpc` | remote procedure call, stub, marshalling, idempotent operation, at-most-once semantics, at-least-once semantics | C: Book 4 `sockets` / `application-layer` may name RPC |
| 25 | `def:b3:distributed-systems:clocks` | happened-before relation, concurrent events, Lamport clock, vector clock | |
| 25 | `def:b3:distributed-systems:causal` | causal delivery | |
| 25 | `def:b3:distributed-systems:cuts` | cut, consistent cut, global snapshot, channel state | |
| 25 | `def:b3:distributed-systems:chandy-lamport` | Chandy--Lamport algorithm | added 2026-11-20 (owned by the brief, needed its own definition) |
| 26 | `def:b3:replication-and-consensus:replication` | replication, primary–backup replication, state-machine replication | |
| 26 | `def:b3:replication-and-consensus:consistency` | consistency model, causal consistency, eventual consistency | sequential consistency is ch. 13's |
| 26 | `def:b3:replication-and-consensus:quorum` | quorum, read quorum, write quorum | |
| 26 | `def:b3:replication-and-consensus:consensus` | consensus problem, partial synchrony | |
| 26 | `thm:b3:replication-and-consensus:flp` | FLP impossibility | |
| 26 | `def:b3:replication-and-consensus:raft` | Raft, election term, leader election, replicated log, log matching property, commit index | Q: *term* bare is ch. 5's λ-term sense |
| 26 | `def:b3:replication-and-consensus:2pc` | two-phase commit, coordinator, blocking protocol | |
| 26 | `def:b3:replication-and-consensus:cap` | network partition; CAP theorem (in the theorem) | |
| 26 | `def:b3:replication-and-consensus:crdt` | conflict-free replicated data type | in an exercise's setup; may move to a remark |

## Part V — Security

| Ch. | Label | Terms | Notes |
|---|---|---|---|
| 27 | `def:b3:symmetric-cryptography:security` | Kerckhoffs's principle, attack model, perfect secrecy, computational security, indistinguishability | |
| 27 | `def:b3:symmetric-cryptography:otp` | one-time pad | |
| 27 | `def:b3:symmetric-cryptography:block` | block cipher, round key, AES | R: g9/g12 |
| 27 | `def:b3:symmetric-cryptography:modes` | mode of operation, ECB mode, CBC mode, initialisation vector, padding, CTR mode, padding oracle | |
| 27 | `def:b3:symmetric-cryptography:stream` | stream cipher, keystream, nonce | |
| 27 | `def:b3:symmetric-cryptography:hash` | cryptographic hash function, preimage resistance, second-preimage resistance, collision resistance | Q/C: Y1 owns *hash function*; R: g12 hash functions |
| 27 | `def:b3:symmetric-cryptography:md` | Merkle–Damgård construction, length-extension attack | |
| 27 | `def:b3:symmetric-cryptography:mac` | message authentication code, HMAC, authenticated encryption, AEAD | |
| 28 | `def:b3:public-key-cryptography:pk` | public-key cryptography, key pair | R: g12 |
| 28 | `def:b3:public-key-cryptography:dh` | Diffie–Hellman key exchange, discrete-logarithm problem, man-in-the-middle attack | R: g12 (key agreement) |
| 28 | `def:b3:public-key-cryptography:bsgs` | baby-step giant-step (method label `met:`) | indexed in its method |
| 28 | `def:b3:public-key-cryptography:rsa` | RSA, textbook RSA, OAEP | R: g12; mathematics owns the miniature RSA arithmetic |
| 28 | `def:b3:public-key-cryptography:ec` | elliptic curve (cryptographic) | told; C: mathematics may own *elliptic curve*: grep |
| 28 | `def:b3:public-key-cryptography:signature` | digital signature, hash-then-sign, Schnorr signature | R: g12 |
| 28 | `def:b3:public-key-cryptography:certificate` | certificate, certificate chain, trust anchor, revocation | R: g12; C: Book 4 `application-layer` |
| 28 | `def:b3:public-key-cryptography:forward-secrecy` | forward secrecy | |
| 28 | `def:b3:public-key-cryptography:passwords` | password hashing, salt, key-derivation function | C: school safety boxes say *password* only |
| 29 | `def:b3:software-security:threat` | threat model, asset, adversary, trust boundary, attack surface | |
| 29 | `def:b3:software-security:memory` | stack smashing, integer overflow vulnerability | *buffer overflow* is Book 3's (`c-strings-structs-files`): recalled |
| 29 | `def:b3:software-security:defences` | stack canary, address-space layout randomisation, non-executable memory, control-flow integrity | |
| 29 | `def:b3:software-security:injection` | SQL injection, parameterised query, command injection, path traversal | |
| 29 | `def:b3:software-security:validation` | input validation, output encoding | |
| 29 | `def:b3:software-security:web` | cross-site scripting, cross-site request forgery, session token | C: school g10 or Book 4 may mention cookies/sessions (school owns *cookie*, *session*) |
| 29 | `def:b3:software-security:access` | access-control matrix, access-control list, capability, role-based access control | Q: *capability* only in this sense |
| 29 | `def:b3:software-security:privilege` | least privilege, privilege separation, confused deputy | |

## Part VI — Building software

| Ch. | Label | Terms | Notes |
|---|---|---|---|
| 30 | `def:b3:software-engineering:requirements` | requirement, use case | |
| 30 | `def:b3:software-engineering:uml` | UML class diagram, sequence diagram | |
| 30 | `def:b3:software-engineering:modularity` | modularity, coupling, cohesion, information hiding, dependency inversion | R/C: g11 `modules-and-interfaces` (module, interface) |
| 30 | `def:b3:software-engineering:patterns` | design pattern, strategy pattern, observer pattern, adapter pattern, model–view–controller | |
| 30 | `def:b3:software-engineering:tests` | integration test, end-to-end test, test double, test oracle, metamorphic testing | unit test is Y1's |
| 30 | `def:b3:software-engineering:property` | property-based test, shrinking | |
| 30 | `def:b3:software-engineering:coverage` | (none) | sync: statement/branch/path coverage are Book 3's (ch. 7): recalled; ch. 30 builds the tool |
| 30 | `def:b3:software-engineering:mutation` | mutation testing, mutant, mutation score, equivalent mutant | |
| 30 | `def:b3:software-engineering:process` | continuous integration, code review, refactoring, characterisation test, technical debt | C: Y1 `version-control` may define *code review*? (it has "what a good commit is") |
| 31 | `def:b3:computer-graphics:homogeneous` | homogeneous coordinates | C: mathematics (projective geometry) may own it: grep; else ours |
| 31 | `def:b3:computer-graphics:transforms` | model transform, view transform, projection matrix | |
| 31 | `def:b3:computer-graphics:projection` | perspective division, view frustum, perspective projection | Q: math owns *projection* |
| 31 | `def:b3:computer-graphics:raster` | rasterisation, edge function, top-left rule | |
| 31 | `def:b3:computer-graphics:barycentric` | barycentric coordinates | C: mathematics (affine geometry b2) likely owns: recall if so |
| 31 | `def:b3:computer-graphics:visibility` | depth buffer, back-face culling | |
| 31 | `def:b3:computer-graphics:shading` | Lambertian shading, Phong shading, Gouraud shading | |
| 31 | `def:b3:computer-graphics:rays` | ray tracing, primary ray, shadow ray | |
| 32 | — | (none) | project chapter: recalls only |

About 330 terms in 190 definition environments, ~6 per chapter.

## Contested terms (for the sync)

Checked 2026-11-20 against Book 4's Phase A `DEFINITIONS.md` and Book 3's Phase A `BRIEFS.md` ("Owns"
lines). Rows marked *settled* follow the other book's own proposal; the rest need a ruling.

| Term | Book 5 | Other book | Proposal | State |
|---|---|---|---|---|
| free / bound variable | 5 | Book 4 `predicate-logic` owns | Book 5 recalls | settled |
| lazy evaluation | 5 | Book 4 owns *lazy iterator* only, asks Y3 | Book 5 ch. 5 owns | settled |
| reference counting | 9 | Book 4 describes, does not define | Book 5 owns | settled |
| interrupt, trap | 10 | Book 4 uses, does not define | Book 5 owns | settled |
| replacement policy, LRU | 11 | Book 4 `caches` owns | Book 5 recalls, owns OPT, clock, Belady | settled |
| deadlock | 13 | Book 4 uses, does not define | Book 5 owns | settled |
| starvation, data race | 13 | Book 4 owns | Book 5 recalls | settled |
| atomic operation | 13 | Book 4 (informal) | Book 4 owns; Book 5 owns CAS, orderings, memory model | settled at the sync |
| decision problem, decidable | 15–16 | Book 4 prose only | Book 5 owns | settled |
| vertex cover | 17–18 | Book 4 `flows-and-matchings` owns (König) | Book 5 recalls | settled |
| k-SAT / 3-SAT | 17 | Book 3 owns *k-SAT* | Book 5 recalls; 3-SAT is an instance | settled |
| unit propagation | 18 | Book 3 owns | Book 5 recalls | settled |
| relaxation | 18 | Book 3 owns *relaxation (of an edge)* | Book 5 says *relaxed problem* | settled (qualified) |
| entropy, information gain | 19 | Book 4 owns | Book 5 recalls, builds codes on it | settled at the sync |
| prefix code, cost of a code | 19 | Book 3 `greedy-proofs` owns | Book 5 recalls | settled |
| index (database), isolation level, schedule | 21, 23 | Book 4 `database-design` owns | Book 5 recalls; owns B+ tree, query plan, serialisability | settled (Book 4 marks *schedule* "ask": accept Book 4) |
| certificate | 28 | Book 4 leaves to Y3 | Book 5 owns | settled |
| buffer overflow | 29 | Book 3 owns | Book 5 recalls; owns *stack smashing*, canary, ASLR | settled |
| unit test | 30 | Book 3 owns | Book 5 recalls | settled |
| graph colouring, control-flow graph, coverage, branch and bound | 7, 8, 18, 30 | Book 3 owns | Book 5 recalls | settled at the sync |
| unification, resolution | 6, 18 | Book 4 owns | Book 5 recalls | settled at the sync |
| Amdahl's law, speed-up | 24 | — | Book 5 owns (Book 4 does not name Amdahl) | settled at the sync |
| happened-before | 13, 25 | — | one sense in Book 5: ch. 25's (messages); ch. 13 says "ordering" | internal |
| page / database page, block / disk block / basic block, log / journal / write-ahead log / replicated log, term / λ-term / election term, token / session token | many | — | qualified terms, bare words to STOP in Phase C | internal |
| homogeneous coordinates, barycentric coordinates, clique, Hamiltonian cycle, lattice, histogram, elliptic curve | 8, 17, 22, 28, 31 | mathematics owns none of them (grep of `\index` 2026-11-20); physics owns *Hamiltonian* (mechanics) and *entropy* (thermodynamics) | Book 5 owns with qualified forms where a physics sense exists | settled; re-grep at each chapter |
