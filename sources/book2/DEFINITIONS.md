# Book 2 (grades 10–12) — definition map (Phase A, 2026-11-20)

Owned by the Book 2 writer. Every term below gets its `\emph{term}\index{key}` pair inside a `definition` of the owner
chapter, and nowhere else in Book 2 (`sources/SERIES_DEFINITIONS.md`, rules 1, 5, 6). Label = the `definition`'s label
(`def:<prefix>:<chapter-slug>:<name>`); several terms may share one definition. A term printed in `\code{}` is never
harvested, so a keyword is defined in words (``a \emph{comprehension}'' with \code{[x for x in t]} beside it).
Items marked are proposed and need the sync's ruling (see section D).

## A. Terms Book 2 owns

### Grade 10
| Term (index key) | Ch. | Label |
|---|---|---|
| specification | 01 | `def:g10:specifications-and-tests:specification` |
| precondition; postcondition | 01 | `def:g10:specifications-and-tests:pre-post` |
| docstring (documentation string) | 01 | `def:g10:specifications-and-tests:docstring` |
| assertion | 01 | `def:g10:specifications-and-tests:assertion` |
| short-circuit evaluation | 01 | `def:g10:specifications-and-tests:short-circuit` |
| test case; boundary case | 01 | `def:g10:specifications-and-tests:test-case` |
| test suite | 01 | `def:g10:specifications-and-tests:test-suite` |
| side effect | 01 | `def:g10:specifications-and-tests:side-effect` (used again in g12-02's paradigms; recalled there) |
| tuple; unpacking | 02 | `def:g10:tuples-sets-comprehensions:tuple` |
| named tuple | 02 | `def:g10:tuples-sets-comprehensions:named-tuple` |
| mutable; immutable | 02 | `def:g10:tuples-sets-comprehensions:mutable` |
| alias | 02 | `def:g10:tuples-sets-comprehensions:alias` |
| shallow copy; deep copy | 02 | `def:g10:tuples-sets-comprehensions:copy` |
| set (Python type) — index `set (type)` | 02 | `def:g10:tuples-sets-comprehensions:set` |
| comprehension | 02 | `def:g10:tuples-sets-comprehensions:comprehension` |
| unsigned integer; n-bit integer | 03 | `def:g10:machine-integers:unsigned` |
| overflow | 03 | `def:g10:machine-integers:overflow` |
| two's complement | 03 | `def:g10:machine-integers:twos-complement` |
| bitwise operation | 03 | `def:g10:machine-integers:bitwise` |
| shift (bit shift) | 03 | `def:g10:machine-integers:shift` |
| mask (bit mask) | 03 | `def:g10:machine-integers:mask` |
| binary fraction | 04 | `def:g10:floating-point:binary-fraction` |
| floating-point number; sign, exponent, significand | 04 | `def:g10:floating-point:float` |
| rounding error | 04 | `def:g10:floating-point:rounding-error` |
| machine epsilon | 04 | `def:g10:floating-point:epsilon` |
| special values (infinity, NaN) | 04 | `def:g10:floating-point:special` |
| character; code point | 05 | `def:g10:text-encodings:code-point` |
| character encoding | 05 | `def:g10:text-encodings:encoding` |
| ASCII | 05 | `def:g10:text-encodings:ascii` |
| Unicode | 05 | `def:g10:text-encodings:unicode` |
| UTF-8 | 05 | `def:g10:text-encodings:utf8` |
| mojibake (garbled text) | 05 | `def:g10:text-encodings:mojibake` |
| photosite | 06 | `def:g10:images-sound-compression:photosite` |
| colour depth | 06 | `def:g10:images-sound-compression:colour-depth` |
| sampling rate; bit depth | 06 | `def:g10:images-sound-compression:sampling-rate` |
| compression; lossless; lossy | 06 | `def:g10:images-sound-compression:compression` |
| run-length coding | 06 | `def:g10:images-sound-compression:rle` |
| compression ratio | 06 | `def:g10:images-sound-compression:ratio` |
| metadata | 06 | `def:g10:images-sound-compression:metadata` |
| header (of a table); descriptor; domain of a column | 07 | `def:g10:data-tables:header` |
| selection; projection | 07 | `def:g10:data-tables:selection` |
| sort key; stable sort | 07 | `def:g10:data-tables:sort-key` |
| grouping; aggregate | 07 | `def:g10:data-tables:aggregate` |
| join | 07 | `def:g10:data-tables:join` |
| missing value; consistency test | 07 | `def:g10:data-tables:missing` |
| JSON (nested text format) | 07 | `def:g10:data-tables:json` |
| URL; scheme; host; query string; fragment | 08 | `def:g10:http-clients-servers:url` |
| port number | 08 | `def:g10:http-clients-servers:port-number` |
| protocol | 08 | `def:g10:http-clients-servers:protocol` |
| HTTP; request; response | 08 | `def:g10:http-clients-servers:http` |
| method (HTTP), GET, POST — index `method (HTTP)` | 08 | `def:g10:http-clients-servers:methods` |
| status code | 08 | `def:g10:http-clients-servers:status` |
| header (HTTP) | 08 | `def:g10:http-clients-servers:http-header` |
| form; parameter | 08 | `def:g10:http-clients-servers:form` |
| cookie; session | 08 | `def:g10:http-clients-servers:cookie` |
| HTTPS | 08 | `def:g10:http-clients-servers:https` |
| graph; vertex; edge | 09 | `def:g10:graphs-first-look:graph` |
| directed graph; weighted graph | 09 | `def:g10:graphs-first-look:directed` |
| degree; neighbour | 09 | `def:g10:graphs-first-look:degree` |
| path (in a graph) — index `path (graph)`; length of a path | 09 | `def:g10:graphs-first-look:path` |
| distance (in a graph) — index `distance (graph)` | 09 | `def:g10:graphs-first-look:distance` |
| connected graph; connected component | 09 | `def:g10:graphs-first-look:connected` |
| eccentricity; radius, diameter and centre of a graph | 09 | `def:g10:graphs-first-look:eccentricity` |
| embedded system | 10 | `def:g10:sensors-actuators-control:embedded` |
| sensor; actuator | 10 | `def:g10:sensors-actuators-control:sensor` |
| control loop | 10 | `def:g10:sensors-actuators-control:control-loop` |
| hysteresis | 10 | `def:g10:sensors-actuators-control:hysteresis` |
| state machine; state; event; transition | 10 | `def:g10:sensors-actuators-control:state-machine` |
| route (web application); dispatcher | 11 | `def:g10:project-web-application:route` |
| escaping (HTML) | 11 | `def:g10:project-web-application:escaping` |

### Grade 11
| Term (index key) | Ch. | Label |
|---|---|---|
| full adder | 01 | `def:g11:gates-to-arithmetic-unit:full-adder` |
| ripple-carry adder | 01 | `def:g11:gates-to-arithmetic-unit:ripple` |
| multiplexer; decoder | 01 | `def:g11:gates-to-arithmetic-unit:mux` |
| arithmetic and logic unit | 01 | `def:g11:gates-to-arithmetic-unit:alu` |
| flag (status flag) | 01 | `def:g11:gates-to-arithmetic-unit:flag` |
| combinational circuit; sequential circuit | 01 | `def:g11:gates-to-arithmetic-unit:combinational` |
| latch; flip-flop | 01 | `def:g11:gates-to-arithmetic-unit:latch` |
| register (hardware) — recalled word, see C | 01 | (no pair: Book 1 g7 owns *register*) |
| von Neumann architecture | 02 | `def:g11:von-neumann-machine:von-neumann` |
| bus | 02 | `def:g11:von-neumann-machine:bus` |
| instruction set | 02 | `def:g11:von-neumann-machine:instruction-set` |
| assembly language; assembler; label | 02 | `def:g11:von-neumann-machine:assembly` |
| jump; conditional jump | 02 | `def:g11:von-neumann-machine:jump` |
| subroutine; stack pointer | 02 | `def:g11:von-neumann-machine:subroutine` |
| system on a chip | 02 | `def:g11:von-neumann-machine:soc` |
| kernel; system call | 03 | `def:g11:os-and-command-line:kernel` |
| free software | 03 | `def:g11:os-and-command-line:free-software` |
| file-system tree; root directory | 03 | `def:g11:os-and-command-line:fs-tree` |
| absolute path; relative path; working directory | 03 | `def:g11:os-and-command-line:abs-rel` |
| shell; command; option | 03 | `def:g11:os-and-command-line:shell` |
| user; group; permission | 03 | `def:g11:os-and-command-line:permission` |
| redirection; pipe; standard input/output | 03 | `def:g11:os-and-command-line:redirection` |
| layer; encapsulation | 04 | `def:g11:network-protocols:layer` |
| network mask; prefix (IP address is Book 1 g8's, recalled) | 04 | `def:g11:network-protocols:ip-address` |
| routing table; next hop; default route | 04 | `def:g11:network-protocols:routing-table` |
| acknowledgement; timeout; retransmission | 04 | `def:g11:network-protocols:ack` |
| alternating-bit protocol | 04 | `def:g11:network-protocols:alternating-bit` |
| TCP; UDP | 04 | `def:g11:network-protocols:tcp-udp` |
| peer-to-peer network | 04 | `def:g11:network-protocols:p2p` |
| variant (loop variant); termination | 05 | `def:g11:proving-algorithms-correct:variant` |
| loop invariant | 05 | `def:g11:proving-algorithms-correct:invariant` |
| correct algorithm (with respect to a specification) | 05 | `def:g11:proving-algorithms-correct:correct` |
| elementary operation; input size | 06 | `def:g11:cost-of-an-algorithm:elementary` |
| cost (time cost) | 06 | `def:g11:cost-of-an-algorithm:cost` |
| best case; worst case | 06 | `def:g11:cost-of-an-algorithm:cases` |
| constant, linear, quadratic cost | 06 | `def:g11:cost-of-an-algorithm:growth` |
| number of halvings h(n) | 06 | `def:g11:cost-of-an-algorithm:halvings` |
| optimisation problem; objective; optimal solution | 07 | `def:g11:greedy-algorithms:optimisation` |
| greedy algorithm | 07 | `def:g11:greedy-algorithms:greedy` |
| canonical coin system | 07 | `def:g11:greedy-algorithms:canonical` |
| labelled example; feature; class (label) — index `class (label)` | 08 | `def:g11:k-nearest-neighbours:example` |
| training set; test set | 08 | `def:g11:k-nearest-neighbours:training-set` |
| k nearest neighbours (the algorithm; method + index) | 08 | `met:g11:k-nearest-neighbours:knn` |
| error rate | 08 | `def:g11:k-nearest-neighbours:error-rate` |
| scaling (of features) | 08 | `def:g11:k-nearest-neighbours:scaling` |
| module | 09 | `def:g11:modules-and-interfaces:module` |
| interface; implementation | 09 | `def:g11:modules-and-interfaces:interface` |
| library; standard library | 09 | `def:g11:modules-and-interfaces:library` |
| API (application programming interface) | 09 | `def:g11:modules-and-interfaces:api` |
| two-pass assembler; symbol table | 10 | `def:g11:project-toy-machine:two-pass` |
| simulator | 10 | `def:g11:project-toy-machine:simulator` |

### Grade 12
| Term (index key) | Ch. | Label |
|---|---|---|
| recursive function; recursion | 01 | `def:g12:recursion:recursion` |
| base case; recursive case | 01 | `def:g12:recursion:base-case` |
| call stack; frame (stack frame) | 01 | `def:g12:recursion:call-stack` |
| class; instance (object); attribute; method | 02 | `def:g12:classes-and-objects:class` |
| constructor | 02 | `def:g12:classes-and-objects:constructor` |
| encapsulation; class invariant | 02 | `def:g12:classes-and-objects:encapsulation` |
| special method | 02 | `def:g12:classes-and-objects:special-method` |
| inheritance; subclass; overriding | 02 | `def:g12:classes-and-objects:inheritance` |
| programming paradigm (imperative, functional, object) | 02 | `def:g12:classes-and-objects:paradigm` |
| pure function | 02 | `def:g12:classes-and-objects:pure-function` |
| abstract data type | 03 | `def:g12:lists-stacks-queues:adt` |
| linked list; cell (of a linked list) — index `cell (linked list)` | 03 | `def:g12:lists-stacks-queues:linked-list` |
| stack; push; pop; LIFO | 03 | `def:g12:lists-stacks-queues:stack` |
| queue; enqueue; dequeue; FIFO | 03 | `def:g12:lists-stacks-queues:queue` |
| postfix notation | 03 | `def:g12:lists-stacks-queues:postfix` |
| tree; node; root; leaf; parent; child; subtree | 04 | `def:g12:trees:tree` |
| depth; height; size | 04 | `def:g12:trees:height` |
| binary tree | 04 | `def:g12:trees:binary-tree` |
| traversal; preorder; inorder; postorder; breadth-first order | 04 | `def:g12:trees:traversal` |
| binary search tree | 04 | `def:g12:trees:bst` |
| balanced tree; degenerate tree | 04 | `def:g12:trees:balanced` |
| adjacency list; successor; predecessor | 05 | `def:g12:graph-algorithms:adjacency-list` |
| depth-first search | 05 | `def:g12:graph-algorithms:dfs` (method) |
| breadth-first search | 05 | `def:g12:graph-algorithms:bfs` (method) |
| cycle | 05 | `def:g12:graph-algorithms:cycle` |
| Dijkstra's algorithm (method + index) | 05 | `met:g12:graph-algorithms:dijkstra` |
| divide and conquer | 06 | `def:g12:divide-and-conquer:dc` |
| merge (of sorted lists); merge sort | 06 | `def:g12:divide-and-conquer:merge` |
| binary logarithm log₂ (notation) | 06 | `not:g12:divide-and-conquer:log2` |
| fast exponentiation | 06 | `met:g12:divide-and-conquer:fast-power` |
| dynamic programming; subproblem | 07 | `def:g12:dynamic-programming:dp` |
| memoisation | 07 | `def:g12:dynamic-programming:memo` |
| longest common subsequence | 07 | `def:g12:dynamic-programming:lcs` |
| edit distance; alignment | 07 | `def:g12:dynamic-programming:edit-distance` |
| pattern; occurrence | 08 | `def:g12:text-search:pattern` |
| shift table (bad-character) | 08 | `def:g12:text-search:shift-table` |
| Boyer–Moore–Horspool algorithm (method + index) | 08 | `met:g12:text-search:horspool` |
| database; database management system | 09 | `def:g12:relational-databases-sql:database` |
| relation; attribute (relation) — index `attribute (relation)`; domain; row | 09 | `def:g12:relational-databases-sql:relation` |
| primary key; foreign key | 09 | `def:g12:relational-databases-sql:keys` |
| relational schema; integrity constraint | 09 | `def:g12:relational-databases-sql:schema` |
| anomaly (insertion, deletion, update); redundancy | 09 | `def:g12:relational-databases-sql:anomaly` |
| query; SQL | 09 | `def:g12:relational-databases-sql:sql` |
| SQL injection | 09 | `def:g12:relational-databases-sql:injection` |
| process | 10 | `def:g12:processes-and-scheduling:process` |
| process state (ready, running, blocked) | 10 | `def:g12:processes-and-scheduling:states` |
| scheduler; quantum; round robin | 10 | `def:g12:processes-and-scheduling:scheduler` |
| interrupt | 10 | `def:g12:processes-and-scheduling:interrupt` |
| context switch | 10 | `def:g12:processes-and-scheduling:context-switch` |
| race condition; critical section; mutual exclusion; lock | 10 | `def:g12:processes-and-scheduling:race` |
| deadlock | 10 | `def:g12:processes-and-scheduling:deadlock` |
| routing protocol; distance-vector routing; link-state routing | 11 | `def:g12:routing:routing-protocol` |
| hop count; route cost | 11 | `def:g12:routing:metric` |
| convergence; counting to infinity | 11 | `def:g12:routing:convergence` |
| symmetric encryption | 12 | `def:g12:secure-communication:symmetric` |
| key exchange | 12 | `def:g12:secure-communication:key-exchange` |
| public key; private key; public-key encryption | 12 | `def:g12:secure-communication:key-pair` |
| digital signature | 12 | `def:g12:secure-communication:signature` |
| hash function; digest | 12 | `def:g12:secure-communication:hash` |
| salt | 12 | `def:g12:secure-communication:salt` |
| certificate; certificate authority | 12 | `def:g12:secure-communication:certificate` |
| decision problem; decidable problem | 13 | `def:g12:halting-problem:decidable` |
| halting problem (theorem + index) | 13 | `thm:g12:halting-problem:halting` |
| compiler | 13 | `def:g12:halting-problem:compiler` |
| computable function (informal) | 13 | `def:g12:halting-problem:computable` |

Projects g10-11, g11-10, g12-14 define little (listed above); the route planner defines nothing new.

## B. Terms Book 2 recalls from Book 1 (no `\emph{}\index{}` pair; wording from Book 1's frozen DEFINITIONS.md)

Per `OUTLINE.md` "Books 1–2": computer, input/output (g1); processor, memory, storage, port (hardware) (g3); file,
folder, path (file) (g3); RAM, hard disk, SSD, byte units (g4); program, operating system (g4); algorithm, repetition,
condition (g4); bit, byte, binary counting (g5); character code (g5); pixel, red–green–blue (g5); network, Internet,
server, browser, web page, link (g5); variable, assignment, type (g6); for loop (g6); Boolean value, condition (g6);
while loop (g6); function, parameter, argument, return value (g7); list, index (g7); string (g7); fetch–execute cycle,
machine language, register, program counter, clock, core (g7); kinds of error, tracing table (g7); base conversion,
hexadecimal, binary addition, carry (g8); dictionary, key (dictionary), record (g8); text file, table of records,
separator / CSV (g8); linear search, binary search, selection sort, insertion sort (g8); packet, address of a machine, router,
name system, client, server (g8); HTML, CSS, element, tag (g9); logic gate, truth table of a gate, half adder, De
Morgan's laws (g9); grid as a list of lists (g9); pseudo-random number, seed, simulation (g9); cipher, key
(cryptographic), encrypt, decrypt, frequency analysis (g9).

Settled at the sync: see D.

## C. Terms owned by another series (recall box, never defined here)

Mathematics: mean, median, range (g10 `statistics`) — g10-07; proof by induction (g12 `sequences`) — g12-01, g12-04;
logarithm (g12 `exponential-logarithm`, as ln; log₁₀ as ln/ln 10) — g12-06 (log₂ as a notation only); graph,
adjacency matrix, walk (g12 `matrices-graphs`) — g12-05 (the vocabulary *graph/vertex/edge* is defined here first,
g10-09, as the outline's cross-series table says); congruence, gcd, prime, fast powers, miniature RSA, Fermat's little
theorem (g12 `arithmetic`) — g12-12, g12-02 (gcd); Euclid's algorithm (g9 `arithmetic-gcd`) — g11-05, g12-13;
Euclidean distance (geometry, recalled) — g11-08; sets as mathematical objects (Y1 `logic-sets-maps`) — g10-02 names
the Python type only; binomial coefficients (g12 `combinatorics`) — g12-07, g12-10 exercises.
Physics: signals, period, frequency (g10 `signals-and-waves`) — g10-06; sampling theorem, analog-to-digital
conversion (Y2, not re-taught) — g10-06 tells sampling; transistor as a switch (Y3, told) — g11-01; electric circuit
and switch (g3–g8) — g11-01.
Earth and space sciences: satellite positioning (g9 `maps-of-the-earth`) — g10-09.
AI series: machine learning beyond k-NN, named in prose — g11-08.

## D. Sync rulings applied (2026-11-20, `SERIES_DEFINITIONS.md` "Sync decisions")

All nine proposals accepted. Book 2 owns: *protocol* and *port number* (g10-08; g11-04 owns *layer*,
*encapsulation*, *peer-to-peer*); *ASCII* and the one-byte extensions (g10-05); *assembly language*, *assembler*,
*label* (g11-02); bare *tree* (g12-04); *sampling rate*, *bit depth* (g10-06; sampling itself told);
*compiler* (g12-13); *side effect* (g10-01); *paradigm*, *pure function* (g12-02); *interrupt* (g12-10);
*specification* (g10-01); *full adder*, *routing table*, *network mask*, *event*, *permission*, *sensor*,
*actuator*. GROUP BY left to the Year 1 volume (g12-09). *Free software* in g11-03.
Book 2 recalls (no pair): *resolution* (Book 1 g5), *authentication* (Book 1 g5/03), *trace table* (Book 1 g6/02),
*interpreter* (Book 1 g6/01), *character code*, *code table* (Book 1 g5/02), *string method* (Book 1 g7/03),
*folder tree* (g3), *document tree* (g9), *class of an HTML element* (g9/01), *machine language*, *instruction*
(g7), *network switch*, *network interface*, *bit rate* (g8/05), *byte* (g4/01), *bit* (g5/01). *Random walk* is
mathematics, prose only. Figures are uncounted: never `\cref{fig:...}`.

## E. One sense per word (Phase C term config, `tools/term_config/book2_en.py`)

Qualified forms Book 2 defines, and the bare words to protect: *path* (file, Book 1) vs **path (graph)** — define as
"a *path* in a graph" and put bare *path* under `EXTRA_PROTECT` for "absolute path", "relative path", "file path";
*key* (dictionary, cryptographic, Book 1) vs **primary key**, **foreign key**, **public key**, **private key**;
*table* (data) vs **routing table**, **shift table**, **symbol table**, **truth table** (Book 1); *stack* (data type,
g12-03) vs **call stack** (g12-01) and the toy machine's stack (prose + **stack pointer**, g11-02); *cell* (memory cell
of Book 1 g7 / the toy machine) vs **cell (linked list)**; *node* (tree) vs network node (prose only: say *router* or
*vertex*); *root* (tree) vs **root directory** (g11-03); *class* (Python, g12-02) vs **class (label)** of k-NN
(g11-08) — g11-08 defines it as "the *class* (or label) of an example", and g12-02's *class* gets `EXTRA_PROTECT`
inside g11-08; *header* (data table, g10-07) vs **header (HTTP)** (g10-08) vs packet header (g11-04, prose);
*method* (HTTP, g10-08) vs **method** (class, g12-02) vs the `method` environment (not a term); *attribute* (class)
vs **attribute (relation)**; *domain* (column, g10-07; relation, g12-09: one definition, recalled) vs a web domain
(prose: *host*); *frame* (stack frame) vs network frame (prose only); *register* (Book 1) — hardware register
(g11-01) is the same sense; *event* (state machine, g10-10) vs probability event (mathematics, not linked);
*diameter*, *radius*, *centre* (of a graph) vs geometry (mathematics; Book 2 never defines the geometric sense);
*distance* (graph) vs Euclidean distance (k-NN, mathematics: protect in g11-08); *cost* (g11-06) vs route cost (g12-11,
same idea, recalled); *variant* (g11-05) vs ordinary English (STOP outside g11-05); *flag* (g11-01) vs ordinary
English; *session* (HTTP) vs shell session (prose).
