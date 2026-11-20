# Book 4 (University Year 2, `bachelor-2`, prefix `b2`) --- definitions

Phase A, 2026-11-20. Every term Book 4 will define, i.e. carry as
`\emph{term}\index{term}` inside a `definition`, with its owner chapter and the
label of that definition. One label may hold several terms (a definition
environment that defines a family). Labels follow
`def:b2:<chapter-slug>:<name>`.

Status column: **own** = the outline's ownership map gives it to Book 4, or no
map names it and Book 4 is the earliest university book that needs it;
**re-found** = a school notion defined again rigorously, as the map allows;
(the contested entries of Phase A were settled at the sync of 2026-11-20; see the rulings at the end). Words
recalled from Book 3 (Year 1) or the sister series are listed under each
chapter as *Recalls* and are never defined here.

Named theorems and methods that Book 4 owns are indexed in their own
environment (`thm:`, `met:`) and listed at the end of each chapter's table.

## Part I --- C++

### 01 `cpp-classes-raii`
| Term | Label | Status |
|---|---|---|
| reference (C++) | `def:b2:cpp-classes-raii:reference` | own |
| namespace | `def:b2:cpp-classes-raii:namespace` | own |
| class, object, data member, member function | `def:b2:cpp-classes-raii:class` | re-found (g12 `classes-and-objects`); map: Y2 owns *class* |
| access specifier (public, private) | `def:b2:cpp-classes-raii:access` | own |
| constructor (C++ member function), destructor | `def:b2:cpp-classes-raii:constructor` | own (sync: Book 3 owns the constructor of an abstract type; the definition names the C++ sense) |
| class invariant | `def:b2:cpp-classes-raii:class-invariant` | own (distinct from Y1's *loop invariant*) |
| const member function, const-correctness | `def:b2:cpp-classes-raii:const` | own |
| resource, resource acquisition is initialisation (RAII) | `def:b2:cpp-classes-raii:raii` | own |
| exception, throw expression, handler | `def:b2:cpp-classes-raii:exception` | own |
| stack unwinding | `def:b2:cpp-classes-raii:unwinding` | own |
| exception-safety guarantee (basic, strong, no-throw) | `def:b2:cpp-classes-raii:guarantee` | own |

Recalls: pointer, heap allocation, leak, ownership convention (Y1
`pointers-and-arrays`, `dynamic-memory`); stack frame, lifetime (Y1
`c-functions-and-stack`); header file (Y1 `c-modules-make-tests`).

### 02 `cpp-copy-move`
| Term | Label | Status |
|---|---|---|
| copy constructor, copy assignment operator | `def:b2:cpp-copy-move:copy` | own |
| shallow copy, deep copy | `def:b2:cpp-copy-move:deep` | own |
| value semantics, reference semantics | `def:b2:cpp-copy-move:value-semantics` | own |
| value category, lvalue, rvalue | `def:b2:cpp-copy-move:rvalue` | own |
| rvalue reference | `def:b2:cpp-copy-move:rvalue-reference` | own |
| move constructor, move assignment operator, moved-from object | `def:b2:cpp-copy-move:move` | own |
| copy elision | `def:b2:cpp-copy-move:elision` | own |
| rule of zero, rule of five | `def:b2:cpp-copy-move:rules` | own |
| smart pointer, unique pointer, unique ownership | `def:b2:cpp-copy-move:unique-ptr` | own |
| shared pointer, shared ownership, weak pointer | `def:b2:cpp-copy-move:shared-ptr` | own; *reference counting* is Book 5's (sync): the count is described, not named as a term |

Theorem: `prop:b2:cpp-copy-move:growth-moves` (copies or moves made by a growing array, factor $r$).

### 03 `cpp-polymorphism`
| Term | Label | Status |
|---|---|---|
| base class, derived class, inheritance | `def:b2:cpp-polymorphism:inheritance` | re-found (g12 inheritance, first look); map: Y2 owns |
| object slicing | `def:b2:cpp-polymorphism:slicing` | own |
| virtual function, override | `def:b2:cpp-polymorphism:virtual` | own |
| dynamic dispatch, subtype polymorphism | `def:b2:cpp-polymorphism:dispatch` | own (sync: Book 4 owns *subtype polymorphism* and *static polymorphism*; *parametric polymorphism* is Book 5's) |
| dispatch table (vtable), table pointer | `def:b2:cpp-polymorphism:vtable` | own |
| pure virtual function, abstract class | `def:b2:cpp-polymorphism:abstract` | own (sync); the bare word *interface* is not defined |
| composition | `def:b2:cpp-polymorphism:composition` | own |
| substitution principle | `def:b2:cpp-polymorphism:lsp` | own |

### 04 `cpp-templates`
| Term | Label | Status |
|---|---|---|
| function template, class template, template parameter | `def:b2:cpp-templates:template` | own |
| template argument deduction | `def:b2:cpp-templates:deduction` | own |
| template instantiation | `def:b2:cpp-templates:instantiation` | own |
| generic programming | `def:b2:cpp-templates:generic` | own (map) |
| concept (C++), constraint | `def:b2:cpp-templates:concept` | own (term config: STOP *concept* outside ch. 4) |
| static polymorphism | `def:b2:cpp-templates:static-poly` | own |
| template specialisation | `def:b2:cpp-templates:specialisation` | own |

### 05 `cpp-standard-library`
| Term | Label | Status |
|---|---|---|
| container, sequence container, associative container, unordered container | `def:b2:cpp-standard-library:container` | own |
| iterator range | `def:b2:cpp-standard-library:iterator` | own (sync: *iterator* is Book 3's, ch. 15: recalled) |
| iterator category (input, forward, bidirectional, random-access, contiguous) | `def:b2:cpp-standard-library:category` | own |
| iterator invalidation | `def:b2:cpp-standard-library:invalidation` | own |
| generic algorithm | `def:b2:cpp-standard-library:algorithm` | own |
| lambda expression, capture | `def:b2:cpp-standard-library:lambda` | own |
| complexity guarantee | `def:b2:cpp-standard-library:guarantee` | own |

Recalls: dynamic array, amortised cost, linked list, hash table, load factor,
search tree, red-black tree, heap (Y1 Parts IV).

## Part II --- Rust and functional programming

### 06 `rust-ownership`
| Term | Label | Status |
|---|---|---|
| owner, ownership | `def:b2:rust-ownership:ownership` | own (map) |
| move (transfer of ownership) | `def:b2:rust-ownership:move` | own (C++'s *move constructor* is the qualified form, ch. 2) |
| drop | `def:b2:rust-ownership:drop` | own |
| copy type | `def:b2:rust-ownership:copy-type` | own |
| borrow, shared borrow, exclusive borrow | `def:b2:rust-ownership:borrow` | own (map) |
| borrow checker | `def:b2:rust-ownership:checker` | own |
| lifetime (of a reference) | `def:b2:rust-ownership:lifetime` | own; Y1 owns *lifetime of an object*: the definition names the qualified form |
| dangling reference | `def:b2:rust-ownership:dangling` | own |
| slice, string slice | `def:b2:rust-ownership:slice` | own |

Theorem: `prop:b2:rust-ownership:no-race` (aliasing excludes mutation: what the rules exclude; soundness of the full language admitted, pointer to the research literature in prose).

### 07 `rust-enums-and-errors`
| Term | Label | Status |
|---|---|---|
| product type, sum type, algebraic data type | `def:b2:rust-enums-and-errors:adt` | own (map) |
| enumeration (Rust), enum variant | `def:b2:rust-enums-and-errors:enum` | own (sync: *variant* of a loop is Book 3's: the definition says *enum variant*) |
| pattern, pattern matching | `def:b2:rust-enums-and-errors:matching` | own (map) |
| exhaustive match | `def:b2:rust-enums-and-errors:exhaustive` | own |
| option type | `def:b2:rust-enums-and-errors:option` | own |
| result type, error propagation | `def:b2:rust-enums-and-errors:result` | own |
| panic | `def:b2:rust-enums-and-errors:panic` | own |
| recursive type, box | `def:b2:rust-enums-and-errors:recursive` | own |

Recalls: inductive set, structural induction (Y1 `induction-and-termination`); union, enum in C (Y1 `c-strings-structs-files`).

### 08 `rust-traits-and-generics`
| Term | Label | Status |
|---|---|---|
| trait, trait implementation, default method | `def:b2:rust-traits-and-generics:trait` | own |
| trait bound, generic function | `def:b2:rust-traits-and-generics:bound` | own |
| monomorphisation | `def:b2:rust-traits-and-generics:mono` | own |
| trait object, fat pointer | `def:b2:rust-traits-and-generics:trait-object` | own |
| object safety | `def:b2:rust-traits-and-generics:object-safe` | own |
| associated type | `def:b2:rust-traits-and-generics:associated` | own |
| coherence (orphan rule) | `def:b2:rust-traits-and-generics:coherence` | own |
| newtype | `def:b2:rust-traits-and-generics:newtype` | own |
| zero-cost abstraction | `def:b2:rust-traits-and-generics:zero-cost` | own |

### 09 `functional-programming`
| Term | Label | Status |
|---|---|---|
| first-class function, higher-order function | `def:b2:functional-programming:higher-order` | own (map) |
| closure, captured environment | `def:b2:functional-programming:closure` | own (map) |
| map, filter, fold (the operations) | `def:b2:functional-programming:fold` | own (defined as *map operation*, *filter*, *fold*; the bare word *map* is STOP: C++'s `std::map`) |
| lazy iterator, iterator adaptor | `def:b2:functional-programming:lazy` | own; *lazy evaluation* is Book 5's (sync): used, not defined |
| pure function, side effect, referential transparency | `def:b2:functional-programming:pure` | own |
| persistent data structure, structural sharing, path copying | `def:b2:functional-programming:persistent` | own |
| tail call, tail recursion | `def:b2:functional-programming:tail` | own |
| equational reasoning | `def:b2:functional-programming:equational` | own |

Theorems: `thm:b2:functional-programming:map-fusion`, `prop:b2:functional-programming:path-copy` (an insertion copies depth + 1 nodes).

## Part III --- Architecture

### 10 `assembly-and-calling-convention`
| Term | Label | Status |
|---|---|---|
| instruction set architecture | `def:b2:assembly-and-calling-convention:isa` | re-found (g11 `von-neumann-machine`, the toy machine); map: Y2 owns *instruction set* |
| general-purpose register, register file | `def:b2:assembly-and-calling-convention:register` | re-found (g11 registers) |
| immediate | `def:b2:assembly-and-calling-convention:immediate` | own |
| load--store architecture, base-plus-offset addressing | `def:b2:assembly-and-calling-convention:load-store` | own |
| instruction format, opcode | `def:b2:assembly-and-calling-convention:format` | own (sync: *byte order*, *little-endian* and *sign extension* are Book 3's, ch. 6: recalled) |
| assembler directive, label (assembly), pseudo-instruction | `def:b2:assembly-and-calling-convention:directive` | own |
| calling convention, argument register, return-value register | `def:b2:assembly-and-calling-convention:convention` | own (map) |
| caller-saved register, callee-saved register | `def:b2:assembly-and-calling-convention:saved` | own |
| leaf function, prologue, epilogue | `def:b2:assembly-and-calling-convention:prologue` | own (sync: *return address* is Book 3's, ch. 3: recalled) |
| jump table | `def:b2:assembly-and-calling-convention:jump-table` | own |

Recalls: stack frame, call stack (Y1 `c-functions-and-stack`); alignment (Y1 `c-strings-structs-files`); memory of a process, object file, linking (Y1 `compilation-pipeline`); two's complement (g10). Theorems: `prop:b2:assembly-and-calling-convention:li` (the `lui`+`addi` split with the rounding term, proved for every 32-bit constant), `prop:b2:assembly-and-calling-convention:ranges` (reach of branches and jumps).

### 11 `processor-and-pipelining`
| Term | Label | Status |
|---|---|---|
| single-cycle processor | `def:b2:processor-and-pipelining:datapath` | own (sync: *datapath* and *control unit* are Book 3's, ch. 28: recalled) |
| control signal | `def:b2:processor-and-pipelining:control` | own (*control unit* recalled) |
| instruction pipeline, pipeline stage, pipeline register | `def:b2:processor-and-pipelining:pipeline` | own (qualified: Book 3 ch. 8 owns the shell *pipeline*) |
| latency and throughput (of an instruction stream) | `def:b2:processor-and-pipelining:throughput` | own (term config: *throughput* used again in Part V, same sense) |
| hazard: structural, data, control | `def:b2:processor-and-pipelining:hazard` | own |
| forwarding (bypassing) | `def:b2:processor-and-pipelining:forwarding` | own |
| stall (bubble), load-use hazard | `def:b2:processor-and-pipelining:stall` | own |
| branch prediction, branch predictor, misprediction penalty | `def:b2:processor-and-pipelining:prediction` | own |
| saturating counter | `def:b2:processor-and-pipelining:counter` | own |
| cycles per instruction (CPI), performance equation | `def:b2:processor-and-pipelining:cpi` | own |

Recalls: multiplexer, decoder, ALU, register, clock, propagation delay, finite-state machine (Y1 `combinational-circuits`, `sequential-circuits`). Theorem: `prop:b2:processor-and-pipelining:speedup` ($nk/(k+n-1)$).

### 12 `caches`
| Term | Label | Status |
|---|---|---|
| temporal locality, spatial locality | `def:b2:caches:locality` | own (map) |
| memory hierarchy | `def:b2:caches:hierarchy` | own |
| cache, cache line, hit, miss, hit rate | `def:b2:caches:cache` | own (map); the bare words *line*, *hit* go to STOP |
| tag, index, offset (fields of an address) | `def:b2:caches:fields` | own (qualified: *tag field*, *index field*, *offset field*; *index* clashes with ch. 30) |
| direct-mapped cache, set-associative cache, fully associative cache | `def:b2:caches:mapping` | own |
| replacement policy, least recently used (LRU) | `def:b2:caches:lru` | own (sync; Book 5 recalls it for pages) |
| write-through, write-back, write-allocate | `def:b2:caches:write` | own |
| compulsory, capacity and conflict misses | `def:b2:caches:three-c` | own |
| miss penalty, average memory access time | `def:b2:caches:amat` | own |
| loop interchange, blocking (tiling) | `def:b2:caches:blocking` | own |

Theorems: `prop:b2:caches:cyclic` (a fully associative LRU cache of $C$ lines misses every access of a cyclic sweep over $C+1$ lines), `prop:b2:caches:traversal` (misses of row and column order).

## Part IV --- Systems programming

### 13 `processes-and-system-calls`
| Term | Label | Status |
|---|---|---|
| user mode, kernel mode | `def:b2:processes-and-system-calls:modes` | own; Y3 `kernel-and-scheduling` owns *interrupt* and *trap* (used, not defined) |
| system call | `def:b2:processes-and-system-calls:syscall` | own (map) |
| process, process identifier | `def:b2:processes-and-system-calls:process` | re-found (g12); owned by Book 4 (sync): Book 3 says "running program" |
| parent process, child process, process tree | `def:b2:processes-and-system-calls:tree` | own |
| process creation by duplication (`fork`) | `def:b2:processes-and-system-calls:fork` | own (defined in words: ``a \emph{fork}'') |
| program execution (`exec`), argument vector | `def:b2:processes-and-system-calls:exec` | own (*environment variable* is Book 3's, ch. 8: recalled) |
| waiting for a child | `def:b2:processes-and-system-calls:wait` | own (*exit status* is Book 3's, ch. 8: recalled) |
| zombie process, orphan process | `def:b2:processes-and-system-calls:zombie` | own |
| built-in command | `def:b2:processes-and-system-calls:builtin` | own (sync) |

### 14 `files-pipes-signals`
| Term | Label | Status |
|---|---|---|
| file descriptor, descriptor table, open file description, file offset | `def:b2:files-pipes-signals:descriptor` | own (map) |
| buffered input--output, buffer flush | `def:b2:files-pipes-signals:buffering` | own |
| inode, link count | `def:b2:files-pipes-signals:inode` | own (sync; *hard link* and *symbolic link* are Book 3's, ch. 8: recalled; Book 5 owns the on-disk layout) |
| directory entry | `def:b2:files-pipes-signals:dirent` | own |
| descriptor duplication | `def:b2:files-pipes-signals:dup` | own |
| pipe (kernel object), end of file on a pipe | `def:b2:files-pipes-signals:pipe` | own (sync: Book 3 ch. 8 owns the shell *pipeline*; Book 4 the kernel object *pipe*) |
| signal, signal handler, signal disposition | `def:b2:files-pipes-signals:signal` | own |
| async-signal-safe function | `def:b2:files-pipes-signals:async-safe` | own |

Recalls: redirection, permissions (Y1 `the-shell`); file, folder, path (school).

### 15 `threads-and-synchronisation`
| Term | Label | Status |
|---|---|---|
| thread, thread creation, joining | `def:b2:threads-and-synchronisation:thread` | own (map) |
| interleaving | `def:b2:threads-and-synchronisation:interleaving` | own |
| race condition, data race | `def:b2:threads-and-synchronisation:race` | re-found (g12 race condition) |
| atomic operation | `def:b2:threads-and-synchronisation:atomic` | own, informal: an indivisible step (sync; Book 5 owns compare-and-swap, memory orderings, the memory model) |
| critical section, mutual exclusion | `def:b2:threads-and-synchronisation:mutex-property` | re-found (g12 mutual exclusion) |
| lock (mutex) | `def:b2:threads-and-synchronisation:lock` | own (map) |
| condition variable | `def:b2:threads-and-synchronisation:condvar` | own |
| semaphore | `def:b2:threads-and-synchronisation:semaphore` | own (map) |
| bounded buffer (producer--consumer) | `def:b2:threads-and-synchronisation:bounded-buffer` | own |
| barrier (rendezvous) | `def:b2:threads-and-synchronisation:barrier` | own |
| readers--writers lock | `def:b2:threads-and-synchronisation:rwlock` | own |
| starvation | `def:b2:threads-and-synchronisation:starvation` | own (sync); *deadlock* is Book 5's: used, not defined |

Named: `thm:b2:threads-and-synchronisation:peterson` (Peterson's algorithm, indexed), `thm:b2:threads-and-synchronisation:bakery` (the bakery algorithm, indexed), `prop:b2:threads-and-synchronisation:interleavings` ($\binom{m+n}{m}$, counting recalled).

### 16 `sockets`
| Term | Label | Status |
|---|---|---|
| socket, socket address | `def:b2:sockets:socket` | own (map) |
| port number | `def:b2:sockets:port` | re-found (g11 ports); ch. 19 uses it |
| stream socket, datagram socket | `def:b2:sockets:kinds` | own |
| listening socket, connected socket | `def:b2:sockets:listening` | own |
| loopback address | `def:b2:sockets:loopback` | own |
| blocking call, non-blocking descriptor | `def:b2:sockets:blocking` | own |
| event loop, readiness notification (`poll`) | `def:b2:sockets:event-loop` | own |
| message framing, length prefix | `def:b2:sockets:framing` | own (qualified *message framing*; ch. 17 owns *framing* on a link: one definition there, this one says *message framing*) |
| network byte order | `def:b2:sockets:network-order` | own |

## Part V --- Networks

### 17 `link-layer`
| Term | Label | Status |
|---|---|---|
| link, link-layer frame, framing, byte stuffing | `def:b2:link-layer:frame` | own (qualified *link-layer frame*; the bare *frame* is STOP: Y1's stack frame is recalled in ch. 10) |
| error-detecting code, parity bit, checksum | `def:b2:link-layer:edc` | own (map) |
| Internet checksum | `def:b2:link-layer:inet-checksum` | own |
| cyclic redundancy code, generator polynomial | `def:b2:link-layer:crc` | own (map); polynomials with 0/1 coefficients and XOR arithmetic, no field theory (level guard) |
| burst error | `def:b2:link-layer:burst` | own |
| multiple access protocol, collision | `def:b2:link-layer:mac-protocol` | own |
| ALOHA, slotted ALOHA, carrier sense (CSMA/CD), binary exponential backoff | `def:b2:link-layer:aloha` | own |
| MAC address, broadcast address | `def:b2:link-layer:mac-address` | own |
| network switch, switch table, self-learning, flooding | `def:b2:link-layer:switch` | own (qualified *network switch*: physics owns the electric switch) |
| address resolution (ARP) | `def:b2:link-layer:arp` | own |
| hidden terminal | `def:b2:link-layer:hidden` | own |

Theorems: `thm:b2:link-layer:crc-burst` (all bursts of length $\le r$ detected), `prop:b2:link-layer:aloha` ($Ge^{-G}$, maximum $1/e$).

### 18 `network-layer`
| Term | Label | Status |
|---|---|---|
| IP address, network prefix, prefix length, subnet mask | `def:b2:network-layer:prefix` | re-found (g11 address and mask) |
| router, forwarding, routing | `def:b2:network-layer:routing` | re-found (g8 router, g11 routing table) |
| forwarding table, longest-prefix match | `def:b2:network-layer:lpm` | own |
| time to live (of a packet) | `def:b2:network-layer:ttl` | own (ch. 20 says *record lifetime* for DNS) |
| maximum transmission unit, fragmentation | `def:b2:network-layer:fragmentation` | own |
| network address translation, private address | `def:b2:network-layer:nat` | own |
| IPv6 address | `def:b2:network-layer:ipv6` | own |
| distance-vector routing, count to infinity, split horizon | `def:b2:network-layer:dv` | re-found (g12 `routing`); map: Y2 owns *routing algorithms* |
| link-state routing | `def:b2:network-layer:ls` | re-found (g12) |
| autonomous system, path-vector routing | `def:b2:network-layer:as` | own |

Theorem: `thm:b2:network-layer:dv-converge` (synchronous distance vector converges in at most $n-1$ rounds).

### 19 `transport-layer`
| Term | Label | Status |
|---|---|---|
| multiplexing and demultiplexing (by port) | `def:b2:transport-layer:demux` | own |
| reliable data transfer, stop-and-wait | `def:b2:transport-layer:rdt` | re-found (g11 alternating bit) |
| sequence number, cumulative acknowledgement, retransmission timeout, round-trip time | `def:b2:transport-layer:seq` | own |
| sliding window, go-back-N, selective repeat | `def:b2:transport-layer:window` | own (map) |
| TCP connection, three-way handshake, connection state | `def:b2:transport-layer:tcp` | own |
| flow control, receive window | `def:b2:transport-layer:flow-control` | own |
| congestion, congestion window, slow start, AIMD, fast retransmit | `def:b2:transport-layer:congestion` | own (map) |
| fairness, fairness index | `def:b2:transport-layer:fairness` | own |

Theorems: `thm:b2:transport-layer:sr-window` ($W \le 2^{k-1}$), `prop:b2:transport-layer:gbn-window` ($W \le 2^k - 1$), `thm:b2:transport-layer:aimd-fair` (AIMD converges to the fair share).

### 20 `application-layer`
| Term | Label | Status |
|---|---|---|
| domain name, name system (DNS), zone | `def:b2:application-layer:dns` | re-found (g8 name system) |
| resolver, recursive and iterative resolution, authoritative server | `def:b2:application-layer:resolver` | own |
| resource record, record lifetime | `def:b2:application-layer:record` | own |
| persistent connection, head-of-line blocking | `def:b2:application-layer:persistent` | own |
| stream multiplexing (HTTP/2) | `def:b2:application-layer:streams` | own |
| Transport Layer Security (TLS) as a layer, TLS record | `def:b2:application-layer:tls` | own (sync: the layer; *certificate* and the handshake's cryptography are Book 5's, used in prose) |

Recalls: HTTP request and response (g10, re-founded only by the protocol text, no new pair).

## Part VI --- Languages and logic

### 21 `finite-automata`
| Term | Label | Status |
|---|---|---|
| alphabet, word, empty word, length | `def:b2:finite-automata:word` | own (map); the bare *word* is STOP outside Part VI (machine word in ch. 10) |
| language, concatenation, power and star of a language | `def:b2:finite-automata:language` | own |
| prefix, suffix, factor, subword | `def:b2:finite-automata:factor` | own |
| deterministic finite automaton, transition function, accepting state, recognised language | `def:b2:finite-automata:dfa` | own (map; Y1 owns the finite-state machine with outputs) |
| complete automaton | `def:b2:finite-automata:complete` | own |
| accessible state, co-accessible state, trim automaton | `def:b2:finite-automata:trim` | own |
| nondeterministic finite automaton | `def:b2:finite-automata:nfa` | own |
| spontaneous transition ($\varepsilon$-transition), $\varepsilon$-closure | `def:b2:finite-automata:epsilon` | own |
| recognisable language | `def:b2:finite-automata:recognisable` | own |
| product automaton | `def:b2:finite-automata:product` | own |

Named: `met:b2:finite-automata:subset` (the subset construction, indexed), `thm:b2:finite-automata:blowup` ($2^k$ lower bound).

### 22 `regular-languages`
| Term | Label | Status |
|---|---|---|
| regular expression, denoted language | `def:b2:regular-languages:regex` | own (map) |
| regular language | `def:b2:regular-languages:regular` | own (map) |
| extended regular expression | `def:b2:regular-languages:extended` | own |
| linear regular expression, local language | `def:b2:regular-languages:local` | own |
| Glushkov automaton | `def:b2:regular-languages:glushkov` | own |
| residual (left quotient), Myhill--Nerode equivalence | `def:b2:regular-languages:residual` | own |
| minimal automaton | `def:b2:regular-languages:minimal` | own |

Named: `met:b2:regular-languages:thompson` (Thompson's construction), `met:b2:regular-languages:berry-sethi` (the Berry--Sethi algorithm), `met:b2:regular-languages:elimination` (state elimination), `thm:b2:regular-languages:kleene` (Kleene's theorem), `thm:b2:regular-languages:myhill-nerode`, `met:b2:regular-languages:moore` (Moore's minimisation), `thm:b2:regular-languages:pumping` (the pumping lemma). *Decision problem* is Book 5's (sync): the section says "deciding whether" and never defines the term.

### 23 `context-free-languages`
| Term | Label | Status |
|---|---|---|
| context-free grammar, production, terminal, nonterminal, start symbol | `def:b2:context-free-languages:grammar` | own (map) |
| derivation, immediate derivation, generated language, context-free language | `def:b2:context-free-languages:derivation` | own (*derivation* in this sense only; ch. 24 says *proof tree*) |
| parse tree, leftmost derivation, rightmost derivation | `def:b2:context-free-languages:parse-tree` | own |
| ambiguous grammar, weak equivalence | `def:b2:context-free-languages:ambiguous` | own |
| right-linear grammar | `def:b2:context-free-languages:right-linear` | own |
| Chomsky normal form | `def:b2:context-free-languages:cnf` | own |
| pushdown automaton, stack alphabet | `def:b2:context-free-languages:pda` | own |

Named: `met:b2:context-free-languages:cyk` (the CYK algorithm, indexed), `thm:b2:context-free-languages:pumping` (pumping lemma for context-free languages). *Recursive descent* is not defined here (Y3 `top-down-parsing` owns it); the chapter's hand-written recogniser is an exercise.

### 24 `predicate-logic`
| Term | Label | Status |
|---|---|---|
| signature (first-order), term, atomic formula | `def:b2:predicate-logic:term` | own (qualified *first-order signature*; the mathematics book's *signature* of a permutation is another sense, another series) |
| first-order formula, quantifier | `def:b2:predicate-logic:formula` | own (map: predicate logic) |
| free variable, bound variable, scope | `def:b2:predicate-logic:free` | own |
| substitution, capture-avoiding substitution | `def:b2:predicate-logic:substitution` | own |
| structure, variable assignment, satisfaction | `def:b2:predicate-logic:structure` | own |
| model, valid formula, logical consequence (first-order) | `def:b2:predicate-logic:consequence` | own as qualified first-order terms (sync: Book 3 owns *model*, *logical equivalence*, *logical consequence* for propositions; the definition names the first-order sense) |
| sequent, inference rule, proof tree | `def:b2:predicate-logic:sequent` | own |
| natural deduction, introduction rule, elimination rule | `def:b2:predicate-logic:nd` | own (map) |
| soundness, completeness (of a proof system) | `def:b2:predicate-logic:soundness` | own |
| proof checker | `def:b2:predicate-logic:checker` | own |
| resolvent, resolution (first-order, refutation) | `def:b2:predicate-logic:resolution` | own (sync: a section of this chapter; Book 5 recalls for logic programming and Horn-SAT) |
| unifier, most general unifier, occurs check | `def:b2:predicate-logic:unification` | own (sync; Book 5 recalls them for type inference) |
| implication graph (of a 2-CNF formula) | `def:b2:predicate-logic:implication-graph` | own (SCC and 2-SAT as a section; *strongly connected component* is Book 3's, `graph-traversals`: recalled, and its linear-time algorithm told as Book 3 gives it or recalled) |

Theorems: `lem:b2:predicate-logic:substitution`, `thm:b2:predicate-logic:soundness` (proved), `thm:b2:predicate-logic:completeness` (stated, `\admitted`), `met:b2:predicate-logic:unify` (Robinson's unification algorithm), `thm:b2:predicate-logic:mgu` (it returns a most general unifier), `thm:b2:predicate-logic:2sat` (a 2-CNF formula is unsatisfiable iff some variable and its negation share a strongly connected component; linear time). Sequent calculus is told, not defined.

## Part VII --- Algorithms II and data

### 25 `text-algorithms`
| Term | Label | Status |
|---|---|---|
| string matching, occurrence, shift | `def:b2:text-algorithms:matching` | re-found (g12 `text-search`; map: Y2 owns *string matching*) |
| bad-character rule | `def:b2:text-algorithms:bad-char` | re-found (g12 Horspool table) |
| border, failure function | `def:b2:text-algorithms:border` | own |
| string-matching automaton | `def:b2:text-algorithms:automaton` | own |
| rolling hash, spurious hit | `def:b2:text-algorithms:rolling` | own |
| trie | `def:b2:text-algorithms:trie` | own |
| dictionary coder, Lempel--Ziv--Welch coding | `def:b2:text-algorithms:lzw` | own (g10 told the dictionary method only) |

Named: `met:b2:text-algorithms:kmp` (Knuth--Morris--Pratt, indexed), `met:b2:text-algorithms:rabin-karp` (indexed), `thm:b2:text-algorithms:kmp-linear`. Recalls: Huffman codes (Y1 `greedy-proofs`), hash function (Y1 `hash-tables`).

### 26 `flows-and-matchings`
| Term | Label | Status |
|---|---|---|
| flow network, capacity, source, sink | `def:b2:flows-and-matchings:network` | own (map) |
| flow, value of a flow | `def:b2:flows-and-matchings:flow` | own |
| cut of a flow network, capacity of a cut | `def:b2:flows-and-matchings:cut` | own, qualified (sync: *cut of a graph* is Book 3's, ch. 26: recalled) |
| residual network, augmenting path | `def:b2:flows-and-matchings:residual` | own |
| matching, maximum matching, perfect matching | `def:b2:flows-and-matchings:matching` | own (map) |
| alternating path, augmenting path relative to a matching | `def:b2:flows-and-matchings:alternating` | own |
| vertex cover | `def:b2:flows-and-matchings:vertex-cover` | own (sync; Book 5 recalls) |
| edge-disjoint paths | `def:b2:flows-and-matchings:disjoint` | own |

Named: `met:b2:flows-and-matchings:ford-fulkerson`, `thm:b2:flows-and-matchings:maxflow-mincut` (indexed), `met:b2:flows-and-matchings:edmonds-karp` (indexed), `thm:b2:flows-and-matchings:berge`, `thm:b2:flows-and-matchings:konig`, `thm:b2:flows-and-matchings:hall`, `thm:b2:flows-and-matchings:menger`. Recalls: bipartite graph, BFS (Y1 `graph-traversals`).

### 27 `randomised-algorithms`
| Term | Label | Status |
|---|---|---|
| randomised algorithm, Las Vegas algorithm, Monte Carlo algorithm | `def:b2:randomised-algorithms:las-vegas` | own (map) |
| one-sided error, amplification | `def:b2:randomised-algorithms:amplification` | own |
| expected running time | `def:b2:randomised-algorithms:expected-time` | own (expectation itself recalled from the mathematics book) |
| universal family of hash functions | `def:b2:randomised-algorithms:universal` | own (map) |
| Bloom filter, false positive | `def:b2:randomised-algorithms:bloom` | own |
| Fermat witness, Carmichael number | `def:b2:randomised-algorithms:fermat` | own (no harvest hit in the mathematics series) |
| Miller--Rabin witness | `def:b2:randomised-algorithms:miller-rabin` | own |
| edge contraction | `def:b2:randomised-algorithms:contraction` | own |

Named: `thm:b2:randomised-algorithms:quicksort` (expected comparisons $2(n+1)H_n - 4n$), `thm:b2:randomised-algorithms:quickselect`, `thm:b2:randomised-algorithms:carter-wegman`, `cor:b2:randomised-algorithms:chains` (expected chain length $\le 1+\alpha$, the Year 1 promise kept), `prop:b2:randomised-algorithms:bloom-rate`, `thm:b2:randomised-algorithms:miller-rabin` (error $\le 1/4$, `\admitted`), `thm:b2:randomised-algorithms:karger`, `prop:b2:randomised-algorithms:maxsat`. Recalls: random variable, expectation, linearity, independence, geometric law (mathematics, Year 2); quicksort, hash table (Y1).

### 28 `search-and-games`
| Term | Label | Status |
|---|---|---|
| state space, search problem, goal test | `def:b2:search-and-games:state-space` | own |
| iterative deepening | `def:b2:search-and-games:iddfs` | own |
| uniform-cost search | `def:b2:search-and-games:ucs` | own |
| heuristic, admissible heuristic, consistent heuristic | `def:b2:search-and-games:heuristic` | own |
| reachability game, position, game graph | `def:b2:search-and-games:game` | own |
| strategy, memoryless strategy, winning strategy, winning position | `def:b2:search-and-games:strategy` | own |
| attractor | `def:b2:search-and-games:attractor` | own |
| game tree, minimax value, evaluation function | `def:b2:search-and-games:minimax` | own (map) |
| alpha--beta pruning | `def:b2:search-and-games:alpha-beta` | own |

Named: `met:b2:search-and-games:astar` (A*, indexed), `thm:b2:search-and-games:astar-optimal`, `thm:b2:search-and-games:attractor`, `thm:b2:search-and-games:alpha-beta`.

### 29 `trees-and-clustering`
| Term | Label | Status |
|---|---|---|
| example, feature, label, training set, test set | `def:b2:trees-and-clustering:examples` | own (qualified *class label*; *label* is also a LaTeX/assembly word: STOP) |
| supervised learning, unsupervised learning, classifier | `def:b2:trees-and-clustering:learning` | re-found (g11 `k-nearest-neighbours`) |
| confusion matrix, accuracy | `def:b2:trees-and-clustering:confusion` | own |
| overfitting | `def:b2:trees-and-clustering:overfitting` | own |
| $k$-nearest-neighbour classifier | `def:b2:trees-and-clustering:knn` | re-found (g11) |
| $k$-d tree | `def:b2:trees-and-clustering:kd-tree` | own |
| decision tree | `def:b2:trees-and-clustering:decision-tree` | own (map) |
| entropy of a finite distribution, information gain | `def:b2:trees-and-clustering:entropy` | own (sync: moved from Y3; Book 5 recalls and builds codes on it) |
| clustering, centroid, $k$-means cost | `def:b2:trees-and-clustering:clustering` | own (map) |
| hierarchical agglomerative clustering, linkage, dendrogram | `def:b2:trees-and-clustering:hac` | own |

Named: `met:b2:trees-and-clustering:id3` (ID3), `met:b2:trees-and-clustering:lloyd` (Lloyd's algorithm), `thm:b2:trees-and-clustering:lloyd-stops`, `thm:b2:trees-and-clustering:single-linkage` (single linkage = spanning-tree cut, Kruskal recalled from Y1).

### 30 `database-design`
| Term | Label | Status |
|---|---|---|
| functional dependency, trivial dependency | `def:b2:database-design:fd` | own (map) |
| implication of dependencies, Armstrong's axioms | `def:b2:database-design:armstrong` | own |
| attribute closure | `def:b2:database-design:closure` | own (qualified *attribute closure*; ch. 9's *closure* is another sense: STOP the bare word in ch. 30) |
| minimal cover | `def:b2:database-design:cover` | own |
| update, insertion and deletion anomaly | `def:b2:database-design:anomaly` | re-found (g12 anomalies) |
| third normal form, Boyce--Codd normal form | `def:b2:database-design:normal-forms` | own (map) |
| multivalued dependency, fourth normal form | `def:b2:database-design:mvd` | own (sync: MVDs and 4NF in this chapter; the chase is told, not defined) |
| decomposition, lossless-join decomposition, dependency preservation | `def:b2:database-design:decomposition` | own |
| transaction, commit, rollback | `def:b2:database-design:transaction` | own (map) |
| atomicity, consistency, isolation, durability | `def:b2:database-design:acid` | own |
| schedule (of transactions) | `def:b2:database-design:schedule` | own (sync; Book 5 recalls, owns serialisability) |
| dirty read, non-repeatable read, phantom read, lost update, write skew | `def:b2:database-design:anomalies` | own |
| isolation level | `def:b2:database-design:isolation-level` | own |
| index (database) | `def:b2:database-design:index` | own (sync); *query plan* is Book 5's: printed plans are shown, the term is not defined |

Recalls: relation, attribute, key, primary key, foreign key, candidate key, relational algebra, join (Y1 `relational-model`). Theorems: `thm:b2:database-design:armstrong` (sound and complete), `prop:b2:database-design:closure-algo`, `thm:b2:database-design:heath`, `thm:b2:database-design:bcnf-lossless`, `thm:b2:database-design:3nf-synthesis`.

### 31 `project-key-value-server`
| Term | Label | Status |
|---|---|---|
| key--value store | `def:b2:project-key-value-server:kv` | own |
| append-only log, log replay, compaction | `def:b2:project-key-value-server:log` | own (Y3 owns the write-ahead log of a database) |
| thread pool | `def:b2:project-key-value-server:pool` | own |
| sharding (lock striping) | `def:b2:project-key-value-server:shard` | own |
| load test, latency percentile | `def:b2:project-key-value-server:load-test` | own |

## Sync rulings (2026-11-20; `sources/SERIES_DEFINITIONS.md` wins on any difference)

| Term | Ruling for Book 4 |
|---|---|
| process, signal, file descriptor, inode, link count, built-in command, pipe (kernel object) | Book 4 defines (ch. 13, 14). Book 3 owns *exit status*, *environment variable*, *hard link*, *symbolic link*, the shell *pipeline*: recalled |
| atomic operation (informal), starvation, data race | Book 4 defines (ch. 15) |
| LRU | Book 4 defines (ch. 12) |
| TLS as a layer | Book 4 defines (ch. 20) |
| vertex cover | Book 4 defines (ch. 26) |
| entropy, information gain | Book 4 defines (ch. 29) |
| schedule, isolation level, index | Book 4 defines (ch. 30); MVDs and 4NF added, the chase told |
| free variable, bound variable, resolution, unification | Book 4 defines (ch. 24); SCC and 2-SAT a section of ch. 24 |
| subtype polymorphism, static polymorphism, abstract class | Book 4 defines (ch. 3, 4); bare *interface* not defined |
| byte order, sign extension | Book 3 (ch. 6): recalled in ch. 10 and ch. 16 (*network byte order* stays Book 4's, qualified) |
| return address | Book 3 (ch. 3): recalled; ch. 10 defines *leaf function*, *prologue*, *epilogue* |
| iterator | Book 3 (ch. 15): recalled; Book 4 defines iterator range, categories, invalidation, *lazy iterator* |
| cut of a graph | Book 3 (ch. 26): recalled; Book 4 defines the cut of a flow network and its capacity |
| datapath, control unit | Book 3 (ch. 28): recalled in ch. 11 |
| model, logical equivalence, logical consequence | Book 3: ch. 24 defines the first-order forms by qualified names |
| constructor | Book 3 owns the abstract-type sense; ch. 1 names the C++ sense in its definition |
| variant | Book 3 owns the loop variant; ch. 7 says *enum variant* |
| deadlock, decision problem, recursive descent, query plan, reference counting, lazy evaluation, interrupt, trap, certificate | Book 5: used without definition, or avoided |
| Amdahl's law, speed-up | Book 5: ch. 11 never names Amdahl |
| parametric polymorphism | Book 5 |
| amortised analysis, potential | recalled from Book 3 (KMP proof, ch. 25) |

Cross-book references are prose only ("defined in the Year 1 volume"), never `\cref`.

## Term-config notes for Phase C (`tools/term_config/book4_en.py`)

STOP or EXTRA_PROTECT candidates, because Book 4 defines one sense and uses
another: *word* (machine word, ch. 10--12), *frame* (stack frame), *line*
(source line, cache line), *hit*, *map* (`std::map`), *closure* (ch. 9 vs
attribute closure, $\varepsilon$-closure), *index* (array index, cache index
field, database index), *label* (assembly label, class label), *flow* (control
flow vs network flow), *cut*, *capacity* (cache capacity vs flow capacity),
*window* (TCP window vs a GUI window), *state* (automaton state, process state,
connection state), *token*, *move* (C++ vs Rust), *borrow*, *concept*,
*pattern* (string matching vs Rust pattern), *term* (first-order term vs the
everyday word), *structure* (first-order structure vs data structure), *model*,
*example* (the LaTeX environment vs a training example), *feature*.
