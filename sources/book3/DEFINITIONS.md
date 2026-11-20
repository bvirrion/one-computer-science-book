# Book 3 (University Year 1, `bachelor-1`, prefix `b1`) --- definitions

Phase A, 2026-11-20. Every term Book 3 will define, i.e. carry as `\emph{term}\index{term}` inside a `definition`,
with its owner chapter and the label of that definition. One label may hold several terms (a definition that
defines a family). Labels: `def:b1:<chapter-slug>:<name>`; named theorems and methods indexed in their own
environment use `thm:` / `met:`. **This file is authoritative** where `BRIEFS.md`'s "Owns" lines differ.

Status: **own** = no university map gives it elsewhere and Book 3 is the earliest university book that needs it
(or the Years map gives it to Year 1); **re-found** = a school notion (Book 1 or 2) defined again rigorously, as
SERIES_DEFINITIONS rule 2 allows; **ask** = contested with Book 4 or 5's Phase A files (read 2026-11-20), settled
at the sync (list at the end). Index keys in parentheses are the qualified forms that keep one sense per word.

Sister-series notions are recalled, never defined (checked against the mathematics and physics harvest,
`sister_harvest.tsv` in the scratchpad): statement, set, map, injective/surjective/bijective, relation,
equivalence relation, **partition**, **order relation**, **interval**, permutation, binomial coefficient,
factorial, sequence, comparison of sequences, induction, logarithm, sum, matrix, adjacency matrix, congruence,
median (statistics), cycle (of a permutation), connected component (topology), the transistor.

## Part I --- C and the machine model

### 01 `compilation-pipeline`
| Term | Label | Status |
|---|---|---|
| source file | `def:b1:compilation-pipeline:source-file` | own |
| preprocessor, macro (C) | `def:b1:compilation-pipeline:preprocessor` | own |
| compiler, compilation | `def:b1:compilation-pipeline:compiler` | re-found (Book 2 g12 `halting-problem` proposes *compiler*) |
| object file, symbol (of an object file) | `def:b1:compilation-pipeline:object-file` | own |
| linker, linking, undefined reference | `def:b1:compilation-pipeline:linker` | own |
| executable file | `def:b1:compilation-pipeline:executable` | own |
| compiler warning | `def:b1:compilation-pipeline:warning` | own |
| interpreter, bytecode | `def:b1:compilation-pipeline:interpreter` | re-found (Book 1 owns *interpreter*) |
| memory layout (of a process): code segment, data segment | `def:b1:compilation-pipeline:layout` | own |

### 02 `c-types-and-control`
| Term | Label | Status |
|---|---|---|
| integer type, width (of an integer type) | `def:b1:c-types-and-control:integer-type` | own |
| integer overflow | `def:b1:c-types-and-control:overflow` | re-found (Book 2 g10 *overflow*) |
| integer promotion, usual arithmetic conversions | `def:b1:c-types-and-control:promotion` | own |
| cast (explicit conversion) | `def:b1:c-types-and-control:cast` | own |
| short-circuit evaluation | `def:b1:c-types-and-control:short-circuit` | re-found (Book 2 g10) |
| side effect, sequencing | `def:b1:c-types-and-control:side-effect` | re-found (Book 2 g10; sync ruling) |
| undefined behaviour, unspecified behaviour, implementation-defined behaviour | `def:b1:c-types-and-control:ub` | own |
| switch statement, fall-through | `def:b1:c-types-and-control:switch` | own |

### 03 `c-functions-and-stack`
| Term | Label | Status |
|---|---|---|
| function declaration (prototype), function definition | `def:b1:c-functions-and-stack:declaration` | own |
| passing by value | `def:b1:c-functions-and-stack:by-value` | own |
| call stack, stack frame | `def:b1:c-functions-and-stack:call-stack` | re-found (Book 2 g12 `recursion`) |
| return address | `def:b1:c-functions-and-stack:return-address` | own (sync ruling) |
| tree of activations (call tree) | `def:b1:c-functions-and-stack:call-tree` | own |
| mutual recursion | `def:b1:c-functions-and-stack:mutual` | own |
| stack overflow | `def:b1:c-functions-and-stack:stack-overflow` | own |
| scope (of a name), shadowing | `def:b1:c-functions-and-stack:scope` | own |
| lifetime (of a variable), automatic variable, static variable, global variable | `def:b1:c-functions-and-stack:lifetime` | own (Book 4's *lifetime (of a reference)* is qualified apart; Book 4 already recalls ours) |
| internal linkage | `def:b1:c-functions-and-stack:linkage` | own |

### 04 `pointers-and-arrays`
| Term | Label | Status |
|---|---|---|
| address (of an object), pointer, dereferencing | `def:b1:pointers-and-arrays:pointer` | own |
| null pointer | `def:b1:pointers-and-arrays:null` | own |
| array (C), array-to-pointer conversion | `def:b1:pointers-and-arrays:array` | own |
| pointer arithmetic | `def:b1:pointers-and-arrays:arithmetic` | own |
| out-of-bounds access | `def:b1:pointers-and-arrays:oob` | own |
| row-major order | `def:b1:pointers-and-arrays:row-major` | own |
| function pointer | `def:b1:pointers-and-arrays:function-pointer` | own |
| generic pointer (`void` pointer, named in words) | `def:b1:pointers-and-arrays:generic` | own |

### 05 `dynamic-memory`
| Term | Label | Status |
|---|---|---|
| heap (memory region), dynamic allocation | `def:b1:dynamic-memory:heap` | own; index `heap (memory)` |
| memory leak | `def:b1:dynamic-memory:leak` | own |
| dangling pointer, use after free, double free | `def:b1:dynamic-memory:dangling` | own |
| growth factor (of an array) | `def:b1:dynamic-memory:growth` | own |
| linearised array | `def:b1:dynamic-memory:linearised` | own |

Not defined: *ownership* (Book 4 `rust-ownership`); the "who frees" convention is described in prose.

### 06 `c-strings-structs-files`
| Term | Label | Status |
|---|---|---|
| null-terminated string | `def:b1:c-strings-structs-files:string` | own |
| buffer overflow | `def:b1:c-strings-structs-files:buffer-overflow` | own (Book 5 agrees: it owns the attack-side terms) |
| structure (C), field (of a structure) | `def:b1:c-strings-structs-files:struct` | own |
| union (C), tagged union | `def:b1:c-strings-structs-files:union` | own (Book 4's *sum type* is the typed form) |
| enumeration (C) | `def:b1:c-strings-structs-files:enum` | own (Book 4 qualifies *enumeration (Rust)*) |
| alignment, padding | `def:b1:c-strings-structs-files:alignment` | own |
| stream, standard streams | `def:b1:c-strings-structs-files:stream` | re-found (Book 2 g11 *standard input/output*) |
| text file, binary file | `def:b1:c-strings-structs-files:text-binary` | own |
| byte order, little-endian, big-endian | `def:b1:c-strings-structs-files:byte-order` | own (sync ruling) |
| sign extension | `def:b1:c-strings-structs-files:sign-extension` | own (sync ruling; Book 4 recalls) |
| file position (of a stream) | `def:b1:c-strings-structs-files:position` | own (Book 4's *file offset* is the kernel's) |

### 07 `c-modules-make-tests`
| Term | Label | Status |
|---|---|---|
| header file, include guard | `def:b1:c-modules-make-tests:header` | own |
| interface, implementation (of a module) | `def:b1:c-modules-make-tests:interface` | re-found (Book 2 g11); Book 4 does not define the bare word |
| opaque type | `def:b1:c-modules-make-tests:opaque` | own |
| separate compilation | `def:b1:c-modules-make-tests:separate` | own |
| makefile, target (of a rule), prerequisite, recipe | `def:b1:c-modules-make-tests:makefile` | own |
| unit test, test suite | `def:b1:c-modules-make-tests:unit-test` | re-found (Book 2 g10 *test suite*) |
| input class, boundary value | `def:b1:c-modules-make-tests:input-class` | own (mathematics owns *partition*: recalled) |
| control-flow graph, feasible path | `def:b1:c-modules-make-tests:cfg` | own (sync ruling; Book 5 recalls) |
| statement coverage, branch coverage, path coverage | `def:b1:c-modules-make-tests:coverage` | own (sync ruling) |
| assertion | `def:b1:c-modules-make-tests:assertion` | re-found (Book 2 g10) |
| defensive programming | `def:b1:c-modules-make-tests:defensive` | own |
| debugger, breakpoint | `def:b1:c-modules-make-tests:debugger` | own |

## Part II --- Tools

### 08 `the-shell`
| Term | Label | Status |
|---|---|---|
| shell | `def:b1:the-shell:shell` | re-found (Book 2 g11) |
| command-line argument | `def:b1:the-shell:argument` | own (Book 4's *argument vector* is the `exec`-level array) |
| exit status | `def:b1:the-shell:exit-status` | own (sync ruling) |
| environment variable | `def:b1:the-shell:environment` | own (sync ruling) |
| redirection | `def:b1:the-shell:redirection` | re-found (Book 2 g11) |
| pipeline (shell) | `def:b1:the-shell:pipeline` | own (sync ruling); the `|` operator is named in prose; *pipe* (kernel object) is Book 4's |
| filter (shell) | `def:b1:the-shell:filter` | own |
| pathname expansion (glob), quoting, word splitting | `def:b1:the-shell:expansion` | own |
| shell script | `def:b1:the-shell:script` | own |
| permission bits | `def:b1:the-shell:permission-bits` | own (Book 2 g11 owns *permission*: recalled) |
| hard link, symbolic link | `def:b1:the-shell:links` | own (sync ruling); Book 4 owns inode, link count |

Used, not defined: process, signal, file descriptor, inode, built-in command (Book 4; the text says "running
program" in prose); regular expression (Book 4 ch. 21).

### 09 `version-control`
| Term | Label | Status |
|---|---|---|
| version control system, repository | `def:b1:version-control:repository` | own |
| commit (Git), snapshot | `def:b1:version-control:commit` | own; index `commit (Git)` (Book 4's transaction *commit* is in Book 4) |
| working tree, staging area | `def:b1:version-control:staging` | own |
| commit graph, ancestor (of a commit) | `def:b1:version-control:commit-graph` | own |
| branch (Git) | `def:b1:version-control:branch` | own; index `branch (Git)` |
| fast-forward merge, three-way merge, merge base | `def:b1:version-control:merge` | own |
| merge conflict | `def:b1:version-control:conflict` | own |
| remote repository, clone | `def:b1:version-control:remote` | own |
| bisection (of a history) | `def:b1:version-control:bisection` | own |

## Part III --- Reasoning about programs

### 10 `propositional-logic`
| Term | Label | Status |
|---|---|---|
| propositional variable, connective, propositional formula | `def:b1:propositional-logic:formula` | own (mathematics owns *statement* and truth tables: recalled) |
| subformula, size (of a formula), height (of a formula) | `def:b1:propositional-logic:size` | own |
| valuation, truth value | `def:b1:propositional-logic:valuation` | own |
| model (of a formula), satisfiable formula, tautology, antilogy | `def:b1:propositional-logic:model` | own (Book 4 qualifies the first-order forms) |
| logical equivalence, logical consequence | `def:b1:propositional-logic:equivalence` | own (same) |
| literal, clause | `def:b1:propositional-logic:literal` | own |
| negation normal form, conjunctive normal form, disjunctive normal form | `def:b1:propositional-logic:normal-forms` | own |
| satisfiability problem (SAT), k-SAT | `def:b1:propositional-logic:sat` | own (named as a problem in words; *decision problem* is Book 5's) |
| equisatisfiable formulas | `def:b1:propositional-logic:equisat` | own |
| unit propagation | `def:b1:propositional-logic:unit` | own (Book 5 agrees: Book 3's solver propagates units) |
| colouring (of a graph), k-colourable graph | `def:b1:propositional-logic:colouring` | own (Book 5 proposes "the first university book that needs it": Book 3) |
| Quine's algorithm | `met:b1:propositional-logic:quine` | own |
| Tseitin's theorem (in the weekend problem) | `thm:b1:propositional-logic:tseitin` | own |

### 11 `induction-and-termination`
| Term | Label | Status |
|---|---|---|
| inductively defined set | `def:b1:induction-and-termination:inductive` | own |
| rooted tree, node (of a tree), root, parent (of a node), child, leaf, internal node, subtree | `def:b1:induction-and-termination:rooted-tree` | re-found (Book 2 g12 `trees`) |
| binary tree, full binary tree | `def:b1:induction-and-termination:binary-tree` | re-found (Book 2 g12) |
| depth (of a node), size (of a tree), height (of a tree) | `def:b1:induction-and-termination:height` | re-found (Book 2 g12); empty tree has height −1 |
| structural induction | `def:b1:induction-and-termination:structural` | own (mathematics owns induction: recalled) |
| strict order, minimal element, immediate predecessor | `def:b1:induction-and-termination:strict-order` | own (mathematics owns *order relation*: recalled) |
| well-founded order | `def:b1:induction-and-termination:well-founded` | own |
| product order, lexicographic order | `def:b1:induction-and-termination:lex` | own |
| termination, variant (termination measure) | `def:b1:induction-and-termination:variant` | re-found (Book 2 g11); index `variant (termination)` because Book 4 uses *variant* for enumerations |
| left-child right-sibling representation | `def:b1:induction-and-termination:lcrs` | own |

### 12 `program-correctness`
| Term | Label | Status |
|---|---|---|
| precondition, postcondition, specification | `def:b1:program-correctness:specification` | re-found (Book 2 g10) |
| partial correctness, total correctness | `def:b1:program-correctness:correctness` | own |
| loop invariant | `def:b1:program-correctness:invariant` | re-found (Book 2 g11) |
| test oracle, property-based test | `def:b1:program-correctness:oracle` | own |
| invariant method | `met:b1:program-correctness:invariant-method` | own |

Not defined: Hoare triple (Book 5 `program-verification`); half-open interval (mathematics owns *interval*).

### 13 `asymptotic-analysis`
| Term | Label | Status |
|---|---|---|
| model of computation (RAM model), elementary operation | `def:b1:asymptotic-analysis:ram` | re-found (Book 2 g11 *elementary operation*) |
| input size, cost function | `def:b1:asymptotic-analysis:cost` | re-found (Book 2 g11 *cost*) |
| big O, big Omega, big Theta | `def:b1:asymptotic-analysis:big-o` | own (mathematics owns comparison of sequences: recalled) |
| worst-case cost, best-case cost, average-case cost | `def:b1:asymptotic-analysis:cases` | re-found (Book 2 g11) |
| space cost | `def:b1:asymptotic-analysis:space` | own |
| recurrence relation, recursion tree | `def:b1:asymptotic-analysis:recurrence` | own |
| master theorem | `thm:b1:asymptotic-analysis:master` | own |

## Part IV --- Data structures

### 14 `dynamic-arrays`
| Term | Label | Status |
|---|---|---|
| abstract data type | `def:b1:dynamic-arrays:adt` | re-found (Book 2 g12) |
| constructor, accessor, transformer (operations of an abstract type) | `def:b1:dynamic-arrays:operations` | own; index `constructor (of an abstract type)` because Book 4 owns the C++ *constructor* |
| representation invariant | `def:b1:dynamic-arrays:rep-invariant` | own |
| dynamic array, size and capacity (of a dynamic array) | `def:b1:dynamic-arrays:dynamic-array` | own |
| amortised cost | `def:b1:dynamic-arrays:amortised` | own (Book 4 recalls it) |
| aggregate method, accounting method, potential function | `def:b1:dynamic-arrays:methods` | own (Book 4 recalls *potential*) |
| circular buffer | `def:b1:dynamic-arrays:ring` | own |

### 15 `linked-structures`
| Term | Label | Status |
|---|---|---|
| linked list, cell (of a linked list), singly linked list, doubly linked list | `def:b1:linked-structures:list` | re-found (Book 2 g12) |
| sentinel | `def:b1:linked-structures:sentinel` | own |
| stack (abstract type), queue, deque | `def:b1:linked-structures:stack` | re-found (Book 2 g12); index `stack (abstract type)` |
| iterator | `def:b1:linked-structures:iterator` | own (sync ruling) |

### 16 `hash-tables`
| Term | Label | Status |
|---|---|---|
| dictionary (abstract type), key (of a dictionary) | `def:b1:hash-tables:dictionary` | re-found (Book 1 g8 uses it) |
| hash function, hash value | `def:b1:hash-tables:hash-function` | re-found (Book 2 g12 owns it in its cryptographic use); Book 5 qualifies *cryptographic hash function* |
| hash table, bucket, collision | `def:b1:hash-tables:hash-table` | own |
| separate chaining, open addressing, linear probing, tombstone | `def:b1:hash-tables:collisions` | own |
| load factor, rehashing | `def:b1:hash-tables:load-factor` | own |
| simple uniform hashing (assumption) | `def:b1:hash-tables:uniform` | own (the expectation proof is Year 2's: stated here) |

### 17 `balanced-trees`
| Term | Label | Status |
|---|---|---|
| binary search tree, search-tree property | `def:b1:balanced-trees:bst` | re-found (Book 2 g12) |
| in-order traversal, preorder, postorder | `def:b1:balanced-trees:traversal` | re-found (Book 2 g12) |
| successor (in a search tree), ordered dictionary | `def:b1:balanced-trees:ordered` | own |
| degenerate tree | `def:b1:balanced-trees:degenerate` | re-found (Book 2 g12) |
| rotation | `def:b1:balanced-trees:rotation` | own |
| balance factor, AVL tree | `def:b1:balanced-trees:avl` | own |
| red-black tree, black height, left-leaning red-black tree | `def:b1:balanced-trees:rb` | own |
| serialisation (of a data structure) | `def:b1:balanced-trees:serialisation` | own |

### 18 `heaps`
| Term | Label | Status |
|---|---|---|
| priority queue | `def:b1:heaps:pq` | own |
| complete binary tree | `def:b1:heaps:complete` | own |
| binary heap, heap property | `def:b1:heaps:binary-heap` | own; bare *heap* goes to STOP (ch. 5 owns *heap (memory)*) |
| sift up, sift down, heapify | `def:b1:heaps:sift` | own |
| heapsort | `met:b1:heaps:heapsort` | own |
| decrease-key | `def:b1:heaps:decrease-key` | own |

### 19 `sorting`
| Term | Label | Status |
|---|---|---|
| comparison sort, in-place sort | `def:b1:sorting:comparison-sort` | own |
| stable sort | `def:b1:sorting:stable` | re-found (Book 2 g10) |
| quicksort, pivot, three-way partition | `def:b1:sorting:quicksort` | re-found (Book 1 g8 / Book 2) ; index `three-way partition (of an array)` |
| merge sort, merge (of sorted sequences) | `def:b1:sorting:merge-sort` | re-found (Book 2 g12) |
| inversion (of a sequence) | `def:b1:sorting:inversion` | own |
| comparison tree | `def:b1:sorting:comparison-tree` | own (the outline's "decision tree": renamed, Book 4 ch. 27 owns *decision tree*) |
| counting sort, radix sort | `def:b1:sorting:radix` | own |
| introsort | `def:b1:sorting:introsort` | own |

## Part V --- Algorithm design

### 20 `backtracking`
| Term | Label | Status |
|---|---|---|
| exhaustive search (brute force) | `def:b1:backtracking:exhaustive` | own |
| backtracking, partial solution, tree of partial solutions | `def:b1:backtracking:backtracking` | own (*search problem* and *state space* are Book 4's: not used as terms) |
| pruning | `def:b1:backtracking:pruning` | own |
| branch and bound, bounding function, continuous relaxation | `def:b1:backtracking:branch-and-bound` | own (sync ruling) |

### 21 `divide-and-conquer`
| Term | Label | Status |
|---|---|---|
| divide and conquer | `def:b1:divide-and-conquer:dc` | re-found (Book 2 g12) |
| selection problem, quickselect, median of medians | `def:b1:divide-and-conquer:selection` | own; index `selection problem` (ch. 29 owns *selection (relational algebra)*) |
| closest-pair problem | `def:b1:divide-and-conquer:closest` | own |
| monotone predicate, dichotomy on the answer | `def:b1:divide-and-conquer:dichotomy` | own |
| meet in the middle | `def:b1:divide-and-conquer:meet` | own |
| Karatsuba's algorithm | `met:b1:divide-and-conquer:karatsuba` | own |

### 22 `greedy-proofs`
| Term | Label | Status |
|---|---|---|
| greedy algorithm | `def:b1:greedy-proofs:greedy` | re-found (Book 2 g11) |
| exchange argument | `met:b1:greedy-proofs:exchange` | own |
| interval scheduling problem, interval partitioning, maximum overlap | `def:b1:greedy-proofs:intervals` | own (*depth* avoided: ch. 11 owns *depth (of a node)*) |
| unit-task scheduling problem | `def:b1:greedy-proofs:unit-tasks` | own |
| prefix code, code tree, cost (of a code) | `def:b1:greedy-proofs:prefix-code` | own (Book 5 agrees: it owns Kraft's inequality and entropy; ch. 22's exercise proves the inequality without indexing it) |
| Huffman code, Huffman's algorithm | `met:b1:greedy-proofs:huffman` | own |

Not defined: approximation algorithm, approximation ratio (Book 5).

### 23 `dynamic-programming`
| Term | Label | Status |
|---|---|---|
| dynamic programming, optimal substructure, overlapping subproblems | `def:b1:dynamic-programming:dp` | re-found (Book 2 g12) |
| memoisation, bottom-up evaluation | `def:b1:dynamic-programming:memo` | re-found (Book 2 g12) |
| edit distance, alignment | `def:b1:dynamic-programming:edit` | re-found (Book 2 g12) |
| longest common subsequence | `def:b1:dynamic-programming:lcs` | re-found (Book 2 g12); mathematics owns *subsequence* |
| matrix-chain problem | `def:b1:dynamic-programming:chain` | own |
| 0/1 knapsack problem, pseudo-polynomial algorithm | `def:b1:dynamic-programming:knapsack` | own |
| longest increasing subsequence | `def:b1:dynamic-programming:lis` | own |

### 24 `graph-traversals`
| Term | Label | Status |
|---|---|---|
| graph, vertex, edge (graph), directed graph, arc, loop (graph) | `def:b1:graph-traversals:graph` | re-found (Book 2 g10; the outline gives graph vocabulary to this series) |
| degree, in-degree, out-degree | `def:b1:graph-traversals:degree` | re-found (Book 2 g10) |
| path (in a graph), simple path, cycle (in a graph) | `def:b1:graph-traversals:path` | re-found; index `path (graph)`, `cycle (graph)` (file paths in ch. 8, permutation cycles in mathematics) |
| distance (in a graph) | `def:b1:graph-traversals:distance` | re-found (Book 2 g10): number of edges |
| connected graph, connected component (of a graph), strongly connected component | `def:b1:graph-traversals:connected` | re-found; index `connected component (graph)` |
| directed acyclic graph | `def:b1:graph-traversals:dag` | own |
| free tree, forest | `def:b1:graph-traversals:free-tree` | own |
| bipartite graph | `def:b1:graph-traversals:bipartite` | own |
| weighted graph, labelled graph | `def:b1:graph-traversals:weighted` | re-found (Book 2 g10) |
| adjacency list, edge list | `def:b1:graph-traversals:lists` | re-found (Book 2 g12 *adjacency list*); mathematics owns *adjacency matrix* |
| depth-first search, discovery time, finishing time | `def:b1:graph-traversals:dfs` | re-found (Book 2 g12) |
| tree edge, back edge, forward edge, cross edge | `def:b1:graph-traversals:edge-classes` | own |
| breadth-first search, BFS tree | `def:b1:graph-traversals:bfs` | re-found (Book 2 g12) |
| topological order | `def:b1:graph-traversals:topo` | own |
| component graph (condensation) | `def:b1:graph-traversals:condensation` | own |
| bridge | `def:b1:graph-traversals:bridge` | own |
| Kosaraju's algorithm | `met:b1:graph-traversals:kosaraju` | own |
| Robbins' theorem (weekend problem) | `thm:b1:graph-traversals:robbins` | own |

### 25 `shortest-paths`
| Term | Label | Status |
|---|---|---|
| weight (of a path), shortest path, weighted distance | `def:b1:shortest-paths:shortest` | own; index `weighted distance` (ch. 24 owns *distance (in a graph)*) |
| relaxation (of an edge) | `def:b1:shortest-paths:relaxation` | own (ch. 20's term is *continuous relaxation*) |
| shortest-path tree | `def:b1:shortest-paths:tree` | own |
| negative cycle | `def:b1:shortest-paths:negative` | own |
| critical path (of a project) | `def:b1:shortest-paths:critical` | own (ch. 27 says *longest delay path*) |
| eccentricity, centre, diameter (of a weighted graph) | `def:b1:shortest-paths:centre` | re-found (Book 2 g10) |
| Dijkstra's algorithm | `met:b1:shortest-paths:dijkstra` | re-found (Book 2 g12) |
| Bellman--Ford algorithm | `met:b1:shortest-paths:bellman-ford` | own |
| Floyd--Warshall algorithm | `met:b1:shortest-paths:floyd` | own |

### 26 `spanning-trees`
| Term | Label | Status |
|---|---|---|
| spanning tree, minimum spanning tree | `def:b1:spanning-trees:mst` | own |
| cut (of a graph), crossing edge | `def:b1:spanning-trees:cut` | own (sync ruling) |
| cut property, cycle property | `thm:b1:spanning-trees:cut-property` | own (two named lemmas) |
| disjoint-set structure (union--find), representative (of a set) | `def:b1:spanning-trees:union-find` | own |
| union by rank, rank (union--find), path compression | `def:b1:spanning-trees:rank` | own |
| bottleneck spanning tree | `def:b1:spanning-trees:bottleneck` | own |
| Kruskal's algorithm, Prim's algorithm | `met:b1:spanning-trees:kruskal`, `met:b1:spanning-trees:prim` | own |

## Part VI --- Machine and data

### 27 `combinational-circuits`
| Term | Label | Status |
|---|---|---|
| Boolean function | `def:b1:combinational-circuits:boolean-function` | own |
| minterm, maxterm, canonical sum of products, canonical product of sums | `def:b1:combinational-circuits:canonical` | own |
| combinational circuit | `def:b1:combinational-circuits:combinational` | re-found (Book 2 g11) |
| Karnaugh map | `def:b1:combinational-circuits:karnaugh` | own |
| implicant, prime implicant, essential prime implicant, don't-care condition | `def:b1:combinational-circuits:implicant` | own |
| functionally complete set | `def:b1:combinational-circuits:complete` | own |
| full adder, ripple-carry adder | `def:b1:combinational-circuits:adder` | re-found (Book 2 g11) |
| generate and propagate signals, carry-lookahead adder | `def:b1:combinational-circuits:lookahead` | own |
| multiplexer, decoder | `def:b1:combinational-circuits:mux` | re-found (Book 2 g11) |
| arithmetic and logic unit | `def:b1:combinational-circuits:alu` | re-found (Book 2 g11) |
| propagation delay, longest delay path | `def:b1:combinational-circuits:delay` | own |

Not defined: logic gate (Book 1 g9 owns it, recalled; sync ruling);
the transistor (physics).

### 28 `sequential-circuits`
| Term | Label | Status |
|---|---|---|
| sequential circuit | `def:b1:sequential-circuits:sequential` | re-found (Book 2 g11) |
| latch, SR latch, D latch | `def:b1:sequential-circuits:latch` | re-found (Book 2 g11) |
| flip-flop (edge-triggered) | `def:b1:sequential-circuits:flip-flop` | re-found (Book 2 g11) |
| clock signal, clock period, synchronous circuit | `def:b1:sequential-circuits:clock` | own |
| setup time, hold time | `def:b1:sequential-circuits:setup` | own |
| register (hardware), shift register, counter (circuit) | `def:b1:sequential-circuits:register` | re-found (Book 1 g7 owns *register*); Book 4 owns *general-purpose register, register file* |
| memory cell | `def:b1:sequential-circuits:memory-cell` | own |
| finite-state machine, state (of a machine), transition | `def:b1:sequential-circuits:fsm` | re-found (Book 2 g10 *state machine*); Book 4 owns the acceptors (*finite automaton*) |
| Moore machine, Mealy machine, state diagram, state encoding | `def:b1:sequential-circuits:moore-mealy` | own |
| datapath, control unit | `def:b1:sequential-circuits:datapath` | own (sync ruling) |

Told, not defined: microprogrammed control.

### 29 `relational-model`
| Term | Label | Status |
|---|---|---|
| relation schema, attribute (of a relation), domain (of an attribute) | `def:b1:relational-model:schema` | re-found (Book 2 g12); index qualified (mathematics owns *relation* and *domain*) |
| tuple (of a relation), relation (database) | `def:b1:relational-model:relation` | re-found (Book 2 g12) |
| superkey, candidate key, primary key, foreign key | `def:b1:relational-model:keys` | re-found (Book 2 g12 *primary key, foreign key*) |
| integrity constraint, referential integrity | `def:b1:relational-model:integrity` | re-found (Book 2 g12) |
| null marker | `def:b1:relational-model:null` | own |
| relational algebra | `def:b1:relational-model:algebra` | own |
| selection (relational algebra), projection, renaming | `def:b1:relational-model:selection` | re-found (Book 2 g10 *selection; projection*) |
| Cartesian product (of relations), natural join, theta join, left outer join | `def:b1:relational-model:join` | re-found (Book 2 g10 *join*) |
| division (relational algebra) | `def:b1:relational-model:division` | own |
| aggregation operator (grouping) | `def:b1:relational-model:aggregation` | re-found (Book 2 g10 *grouping; aggregate*) |
| three-valued logic | `def:b1:relational-model:three-valued` | own |
| view | `def:b1:relational-model:view` | own |
| entity, relationship, multiplicity (of a relationship), entity--relationship model | `def:b1:relational-model:er` | own |
| association table | `def:b1:relational-model:association-table` | own |

Not defined: normal forms, functional dependency, anomalies (Book 4 `database-design`); index (database) (Book 5).

### 30 `project-text-search-engine`
| Term | Label | Status |
|---|---|---|
| tokenizer | `def:b1:project-text-search-engine:tokenizer` | own |
| inverted index, posting list | `def:b1:project-text-search-engine:inverted-index` | own |
| term frequency, document frequency, tf--idf score | `def:b1:project-text-search-engine:tfidf` | own |
| end-to-end test | `def:b1:project-text-search-engine:end-to-end` | own |

## Contested terms (settled at the sync, 2026-11-20: every Book 3 claim granted)

| Term | Book 3 chapter | Other claimant | Book 3 proposal |
|---|---|---|---|
| byte order, little/big-endian | 6 | Book 4 ch. 10 (defers if Book 3 defines it) | Book 3 owns; Book 4 owns *network byte order* (it already lists it) |
| return address | 3 | Book 4 ch. 11 | Book 3 owns (frames need it); Book 4 owns prologue, epilogue, leaf function, calling convention |
| side effect | 2 | Book 4 ch. 9 | Book 3 owns (C sequencing is the first need); Book 4 owns *referential transparency*, *pure function* |
| exit status | 8 | Book 4 ch. 13 | Book 3 owns; Book 4 owns *waiting for a child* |
| environment variable | 8 | Book 4 ch. 13 (*environment*) | Book 3 owns *environment variable*; Book 4 owns *environment (of a process)* and *argument vector* |
| hard link, symbolic link | 8 | Book 4 ch. 14 | Book 3 owns the two link kinds at the user level; Book 4 owns *inode*, *link count*, *directory entry* |
| iterator | 15 | Book 4 ch. 5 | Book 3 owns *iterator*; Book 4 owns range, categories, invalidation |
| cut (of a graph) | 26 | Book 4 ch. 26 (flow) | Book 3 owns *cut*; Book 4 owns *s–t cut*, *capacity of a cut* |
| datapath, control unit | 28 | Book 4 ch. 12 | Book 3 owns (the toy machine's control); Book 4 owns *single-cycle processor*, *control signal*, pipeline terms |
| control-flow graph, coverage | 7 | Years map: Y3 | Book 3 owns (first-year testing item); Book 5 recalls |
| branch and bound | 20 | Years map: Y3 `hard-problems` | Book 3 owns (first look); Book 5 recalls |
| graph colouring | 10 | Book 5 ch. 8 (if no earlier owner) | Book 3 owns |
| constructor | 14 | Book 4 ch. 1 (C++) | no clash: Book 3 indexes `constructor (of an abstract type)`; Book 4 indexes `constructor (C++)` |
| variant | 11 | Book 4 ch. 7 (Rust enum variant) | Book 3 indexes `variant (termination)`; Book 4 should qualify `variant (of an enumeration)` |

## One sense per word (Phase C, `tools/term_config/book3_en.py`)

Bare words to STOP or EXTRA_PROTECT because Book 3 defines only qualified forms or two senses meet in the book:
*heap* (ch. 5 memory vs ch. 18 binary heap), *stack* (call stack vs abstract type), *size* (formula, tree,
dynamic array, input), *height* (formula vs tree), *key* (dictionary, sort key, primary key), *selection*
(problem vs relational operator; selection sort recalled), *branch* (Git, coverage, branch and bound), *merge*
(Git vs sorted sequences), *tree* (rooted, free, spanning, Git tree object, comparison tree), *path* (file path
vs graph), *cycle* (graph vs permutation), *distance* (edges, weighted, edit), *cost* (cost function, code cost,
amortised), *invariant* (loop vs representation), *symbol* (object file vs Huffman alphabet), *cell* (linked list
vs memory cell vs spreadsheet prose), *parent*/*child* (tree vs process in ch. 8), *root* (tree vs the root
account), *state* (machine vs program state in ch. 12), *order* (lexicographic, topological, in-order, row-major),
*partition* (mathematics' term vs quicksort's procedure), *relation* and *domain* (mathematics vs database),
*commit*, *register*, *counter* (circuit vs a loop counter), *word*, *frame*, *record*, *field*, *string*, *model*.
