# Book 4 (University Year 2) --- progress

## State

- **2026-11-20, Phase A done.** Written: `BRIEFS.md` (31 chapter briefs and the
  programme check), `DEFINITIONS.md` (terms, labels, contested list),
  `RV_PLAN.md` (design of `code/shared/rv/`). No prose, no code, no edits
  outside `sources/book4/`.
- **2026-11-20, sync read.** Rulings applied to `DEFINITIONS.md` (no entry
  left to ask; byte order, sign extension, return address, iterator, cut of a
  graph, datapath, control unit, exit status, environment variable, hard and
  symbolic links recalled from Book 3; resolution, unification, implication
  graph added to ch. 24; MVD and 4NF to ch. 30). BRIEFS: see "Sync changes" at
  its top.
- **2026-11-20, RISC-V stint done: `code/shared/rv/` FROZEN 2026-11-20
  (Book 4)**, first line of `RV.md`. Package `rv/` (isa, asm, machine,
  `__main__`), `RV.md`, `tests/` (118 tests green: golden encodings,
  hypothesis round trips, semantics edge cases, `li` edge values, every fault
  and assembly error, step record, hooks, CLI golden transcripts). Sync
  decisions all in: sbrk (ecall 9), `call`/`tail` = one `jal` (documented),
  labels `[A-Za-z_.][A-Za-z0-9_.]*`, entry `main`, `ra` = exit address so
  `ret` exits with `a0`, `sp` = 0x7ffffff0, `--stats --trace --regs --steps`,
  `Step` record, hooks `.ecalls`, `.on_ecall`, `.on_ebreak`, and a precise
  `.on_trap` (pc left at the trapping instruction, for Book 5's monitor and
  its "forgot pc += 4" exercise). 14 ledger rows `b2:rv-*`, `b2:linux-exit-93`.
  Main session and Book 5 told through this log and the report.
- **2026-11-20, all 31 chapters written.**
- **Phase C in progress:** definitions gap in ch. 15--18 closed (27 added, defcheck clean); Part headings of
  ch. 1--10 kept with their first item; printed listing lines over 95 characters fixed (68: padding shrunk,
  comments shortened, 32 lines split, ranges shifted, run_selfassign recaptured and its line numbers in the
  solution updated); term links applied with a curated `tools/term_config/book4_en.py`.
- **2026-11-20, Phase C done.** Fresh forced build 0/0/0, `gates.sh --log 4` and `gates.sh bachelor-2` OK,
  term links current (`--check`), `test_code.sh` green chapter by chapter after the fixes (see Phase C notes).
- **Next action:** Phase D report.

## Web fetches

| Date | Count | What |
|---|---:|---|
| 2026-11-20 | 7 | 2 searches; the preparatory-class programme annex (PDF); three second-year licence course lists (two PDFs, one page that loaded no course list) |
| 2026-11-20 | 15 | RISC-V stint: riscv-opcodes (3 tables), ISA manual sources (RV32I, M; tree, tags, release list; one 404), psABI calling convention, assembly manual, RARS system calls, Linux unistd.h, the ratified-specifications page (script-rendered, unused) |
| 2026-11-20 | 6 | ch. 1: cppreference (C++20, history, destructor, noexcept, logic_error), Stroustrup's FAQ |
| 2026-11-20 | 5 | ch. 2: cppreference (copy elision, push_back, move constructor twice, C++11 features) |
| 2026-11-20 | 7 | ch. 3: Wikipedia twice (map only, not cited), ACM DL twice (403), Crossref API three times (Liskov 1987, Liskov--Wing 1994, Simula HOPL) |
| 2026-11-20 | 3 | ch. 4: cppreference (constraints, qsort, sort) |
| 2026-11-20 | 6 | ch. 5: cppreference (lower_bound, map, unordered_map, container overview, max_load_factor, vector/insert) |
| 2026-11-20 | 3 | ch. 6: Crossref (RustBelt, metadata and abstract), edition guide (Rust 2021) |
| 2026-11-20 | 1 | ch. 7: std::option docs (Representation, null pointer optimization) |
| 2026-11-20 | 3 | ch. 8: web search + NASA LLIS PDF (Mars Climate Orbiter MIB Phase I report, text extracted locally) |
| 2026-11-20 | 3 | ch. 10: psABI calling convention (riscv-cc.adoc, register table and argument registers), x86-64 psABI (low-level-sys-info.tex), riscv.org About (history) |
| 2026-11-20 | 8 | ch. 11: Wikimedia Commons API (5 searches, 1 file-info query for MIPS R3000A die: CC BY 3.0, Pauli Rautakorpi), 2 image downloads (first URL refused, second the API's 1920 px rendering) |
| 2026-11-20 | 14 | ch. 12: Wikimedia Commons API (3 searches, 4 file-info queries), 4 image downloads (one refused; used: TWSC DDR5 SO-DIMM rear view, CC BY-SA 4.0); Crossref API 3 times (Wilkes 1965, Liptay 1968 search and metadata) |
| 2026-11-20 | 4 | ch. 13: POSIX.1-2024 fork, waitpid, exec (pubs.opengroup.org); man7 proc_pid_status(5) |
| 2026-11-20 | 3 | ch. 14: man7 signal(7), pipe(7), signal-safety(7) |
| 2026-11-20 | 7 | ch. 15: Crossref (Peterson 1981, Lamport 1974), EWD 123 and EWD 310 transcriptions, EWD index pages 01xx and 03xx (dates), cppreference counting_semaphore |
| 2026-11-20 | 4 | ch. 16: RFC 6890, RFC 791, kernel ip-sysctl, man7 socket(7) |
| 2026-11-20 | 11 | ch. 17: RFC 1662 (twice), 1071, 826, 7042 (twice), 894, 1952, 3385, kernel crc32 doc (unused), Crossref Abramson 1970; plus the Commons API for one photograph |
| 2026-11-20 | 13 | ch. 18: RFC 791, 1918, 5737, 3849, 4632, 8200, 5952, 3022, 2453, 2328, 4271, IANA news page (404), NRO 2011; plus the Commons API for one photograph |
| 2026-11-20 | 8 | ch. 19: RFC 768, 9293, 6298, 5681, 6335, 9000, Crossref Mathis 1997, arXiv Jain 1984 |
| 2026-11-20 | 12 | ch. 20: RFC 1034, 1035, 3596, 2606, 9110, 9112, 9113, 9114, 8446 (twice), 5321 (twice) |
| 2026-11-20 | 2 | ch. 21: Crossref (Kleene 1956, Rabin and Scott 1959) |
| 2026-11-20 | 6 | ch. 22: Crossref (Thompson 1968, Glushkov 1961, Berry and Sethi 1986, Nerode 1958), Python `re` docs, POSIX ch. 9 |
| 2026-11-20 | 3 | ch. 23: Crossref (Chomsky 1956, ALGOL 60 report 1960, Younger 1967) |
| 2026-11-20 | 8 | ch. 24: Crossref (Gentzen 1935 twice, one 429; Gödel 1930; Robinson 1965; Aspvall, Plass and Tarjan 1979), SEP entry on Frege, Lean home page, Rocq about page |
| 2026-11-20 | 9 | ch. 25: Crossref (KMP 1977, Boyer-Moore 1977, Karp-Rabin 1987, Welch 1984, Ziv-Lempel 1978 twice, Aho-Corasick 1975 twice; two 429), RFC 1951 |
| 2026-11-20 | 6 | ch. 26: Crossref (Ford-Fulkerson 1956, Edmonds-Karp 1972 twice, one 429; Hall 1935; Menger 1927), Wikipedia (Konig 1931) |
| 2026-11-20 | 7 | ch. 27: Crossref (Hoare 1961, Carter-Wegman 1979, Bloom 1970, Miller 1976, Rabin 1980; a bibliographic query for Karger 1993 found nothing), Wikipedia (Karger 1993) |
| 2026-11-20 | 4 | ch. 28: Crossref (Hart-Nilsson-Raphael 1968, von Neumann 1928 twice after a 429, Knuth-Moore 1975) |
| 2026-11-20 | 4 | ch. 29: Crossref (Quinlan 1986, Lloyd 1982, Bentley 1975), Wikipedia (Lloyd's algorithm, the 1957 date) |
| 2026-11-20 | 9 | ch. 30: SQLite isolation, transaction and EXPLAIN QUERY PLAN pages; PostgreSQL transaction isolation; Crossref (Codd 1970, Haerder-Reuter 1983); Wikipedia (BCNF, 3NF, ACID) |
| **Total** | **201** | budget ~300 |

## Chapters

| Ch. | Pages (body + sol.) | Listings | Outputs | Tests | Figures S/P/AI | Ledger rows |
|---|---|---:|---:|---|---|---:|
| 1 `cpp-classes-raii` | 19 + 4 | 18 files | 15 (1 MEASURED) | 4 C++ test files (File, Fraction, logger, 6 exercise solutions) | 4/0/0 | 5 (+1 source) |
| 2 `cpp-copy-move` | 18 + 4 | 22 files | 16 (1 MEASURED) | 4 C++ test files (growth counts for n = 0..5000, Buffer x2, weak cycle, 4 exercise solutions) | 4/0/0 | 3 |
| 3 `cpp-polymorphism` | 18 + 4 | 22 files | 14 (1 MEASURED) | 4 test files (C++: library on the town's loans with an independent chrono date check, shapes + Triangle, expr + double dispatch; C: fines tables) | 4/0/0 | 4 (+1 source) |
| 4 `cpp-templates` | 14 + 4 | 21 files | 13 (1 MEASURED) | 2 C++ test files (Vec<T> with counts and a throwing copy; 5 exercise solutions incl. compile-time refusals) | 3/0/0 | 3 |
| 5 `cpp-standard-library` | 16 + 4 | 27 files | 16 (4 MEASURED) | 4 C++ test files (word counts of the town's titles + top-k; LRU vs reference; loans, by month, loan desk; interval map vs brute force + three queues in the same order) + 1 pytest (chart table = measured output) | 4/0/0 + 1 chart | 5 |
| 6 `rust-ownership` | 17 + 5 | 34 files | 22 (1 MEASURED) | crate `tests/ownership` (8 tests: longest, slices, first_word, halves, reverse_words with buffer identity, Stack vs Vec + a million-node drop, distinct x2, Dict vs HashMap + town titles); clippy -D warnings clean | 4/0/0 | 2 |
| 7 `rust-enums-and-errors` | 15 + 3 | 25 files | 13 | crate `tests/enums` (10 tests: every planted weather defect, parse errors, monthly tree, simplify preserves eval on 3000 random expressions, BST properties + mirror, checked_div, JSON printer, list, derivative vs central difference on 500 functions, config errors); clippy clean | 3/0/0 | 1 |
| 8 `rust-traits-and-generics` | 16 + 3 | 30 files | 17 (1 MEASURED) | crate `tests/traits` (7 tests: units, V2 operators, fraction lowest terms + padding, largest with NaN, shapes by area, matrices incl. Fibonacci and boolean reachability via newtype, typestate size); clippy clean | 4/0/0 | 2 |
| 9 `functional-programming` | 16 + 3 | 30 files | 16 | crate `tests/functional` (8 tests: map/filter fusion and fold laws on 500 lists, Rc sharing counts, path copying creates depth+1 (depth if present) and leaves old versions intact, sheet versions + node bound, compose, frequencies, persistent queue incl. repeated cost on an old version, persistent map vs BTreeMap snapshots); clippy clean | 4/0/0 | 0 |
| 10 `assembly-and-calling-convention` | 16 + 5 | 26 files + 7 exercise programs | 21 | pytest `tests/test_asm_programs.py` (29 tests on the rv API: every listing's output, the misaligned fault, `li` proposition on 11 constants, check digit and the count 14n + 26 on 7 codes, max/strcmp/struct/switch/fixed-ra exercises, fib calls = jumps 2C(n)+1 for n = 0..11, binary search on 7 keys, hand encodings and decodings) | 5/0/0 | 4 (+2 sources) |
| 11 `processor-and-pipelining` | 14 + 3 | 25 files + 3 exercise files (lui/jal/jalr datapath, backward-taken predictor, rescheduled loop) | 6 session outputs | pytest: `test_datapath.py` (single-cycle model = rv at every step of every chapter program, extended model, imm gen vs assembler, control table), `test_pipeline.py` (hand counts of 5 sequences, cycles = n + 4 + stalls + flushed on 7 programs x 6 configurations, ideal gain, one stall per load-use for 4 consumer kinds, rescheduled loop, backward-taken, forwarding unit = newest writer), `test_predictor.py` (two-bit proposition on synthetic loops, printed counts), `test_figures.py` (cpi.dat = output = model); 64 tests | 5/1/0 + 1 chart | 0 (photo credit in `images/book4/CREDITS.md`) |
| 12 `caches` | 19 + 4 | 28 files (Python simulator + rv trace, 7 measured C programs, getconf session) + 1 exercise file | 15 (7 MEASURED) | pytest `test_cache.py` (field split incl. the laptop's L1, hand traces DM and 2-way, write policies and flush counts, cyclic proposition for C = 4, 8, 32, traversal proposition DM and fully associative, 3C counts add up, matrix_sum trace 128/1024, blur row order = N^2/16 and strips 3N^2/16 - 2N, exercise traces, wrong-bits run), `test_figures.py` (sweep.dat = output; plateaus rise L1 < L2 < L3 < memory); 20 tests | 6/1/0 + 1 chart | 2 (+2 sources) |
| 13 `processes-and-system-calls` | 15 + 5 | 21 files (C17: hello/strace session, syscall cost, fork, tree, exec, wait statuses, zombie/orphan via /proc, cd in a child, minish + parser, budget session, exercise programs) + 5 exercise files (runit, xargs_lite, cd -, && and ||, ptree) | 16 (1 MEASURED) | C `tests/minish_test.c` (split, $?, run_list on a fake run, cd -), pytest `test_procs.py` (minish end-to-end: statuses, 127, cd built in, exit; 2^3 processes and depth counts; runit incl. 143; xargs batches and worst status; ptree output); 8 tests | 5/0/0 | 4 (+4 sources) |
| 14 `files-pipes-signals` | 15 + 7 | 30 files (C17: descriptors, offsets, shared offset after fork, copy + strace read-count session, buffer timing, fork-duplicated buffer, links session, same inode, redirect, pipeline library + driver, forgotten close, SIGINT, SIGCHLD reaping, SIGPIPE, 2 exercise programs; fit_copy.py) + 5 exercise files (mycp, tee, capture, minish2 with < > \| &) | 18 (2 MEASURED) | C `tests/pipeline_test.c` (capture: cat, status 3, 300 000 bytes without deadlock; run_pipeline: data and last-stage status), pytest `test_tools.py` (mycp bytes + mode + no overwrite for 4 buffer sizes, tee and -a, minish2 end-to-end with a background job, copy law by strace for 5 (n, b)), `test_figures.py` (copy_times.dat = output, law, shape); 10 tests | 4/0/0 + 1 chart | 6 (+3 sources) |
| 15 `threads-and-synchronisation` | 18 + 7 | 27 files (C17: last seat, race (MEASURED), Peterson + bakery library and demo, bounded buffer with conditions, semaphores, barrier, philosophers timed + ordered, TSan session with trim.sh, 2 exercise programs; C++: counter_threads, bounded_queue.hpp + pc_cpp; Rust: race_refused (E0373), arc_mutex, channel_pc; Python: interleavings.py explorer, office_model, cond_model, bakery_model, sem_outcomes) + 4 exercise files (barrier2, safe_counter.hpp, rwlock.rs) | 21 (1 MEASURED) | pytest `test_interleavings.py` (binomial and multinomial counts, counter outcomes, flag lock, Peterson and swapped Peterson 60/12, office 20/12, 70, 12 870, cond if/while, bakery with and without choosing, semaphore outputs), `test_figures.py`; C `counter_test.c` (Peterson, bakery n = 2..8, reusable barrier 2000 rounds); C++ `pc_test.cpp` (FIFO, 4x4 sums, SafeCounter); crate `rust_sync` (writer-preferring RwLockW: exclusion, preference); 14 + 3 tests | 4/0/1 + 1 chart | 7 (+7 sources) |
| 16 `sockets` | 12 + 5 | 22 files (C17: net.c library (listen, connect, send_all, recv_all, framing), echo pair, partial recv, stream vs datagram boundaries, byte order, forgotten htons, directory service (directory.c, servers.c with fork/threads/poll, directory_server.c), Python client, demo session, load test session (MEASURED), 4 exercise programs) + 4 exercise files (linereader, count_server, chat) | 10 (1 MEASURED) | C `framing_test.c` (300 random frames round trip and cut frames, 1-byte trickle through recv_msg and the line reader, counting server 4x50 lines, chat server 3 clients), pytest `test_directory.py` (3 designs end to end against the CSV tables, error replies), `test_figures.py` | 5/0/0 + 1 chart | 4 (+4 sources) |
| 17 `link-layer` | 14 + 5 | 22 files (Python: hook, byte stuffing, parity and parity grid, Internet checksum, crc.py (division, CRC-16, CRC-32 bitwise and by table vs zlib), long division, burst check, random errors 2^24, slotted ALOHA, backoff, Ethernet frame with ARP, switch, ARP caches, 4 exercise programs; C crc32.c) + 2 exercise files (parity2d, crc8) | 18 | pytest `test_crc.py` (three CRC-32s = zlib, CRC-16 = division, codewords divisible, ex. 4 remainder, burst counts, CRC-8, C output = zlib), `test_checksum.py` (RFC 1071 worked example, receiver ffff, grid corrects all 48 single flips, stuffing round trip), `test_switch.py`, `test_figures.py` | 3/0/0 + 1 chart + 1 photo + 1 AI | 11 (+9 sources) |
| 18 `network-layer` | 13 + 5 | 17 files (Python: traceroute on the town, cidr.py vs ipaddress, trie LPM, linear LPM (NORUN), bench (MEASURED), IPv4 header + forward, NAT, fragmentation, IPv6 expansion, distance vector (rounds + count to infinity), poisoned reverse, link state (NORUN), town network DV vs Dijkstra + router failure, 2 exercise bugs) + 3 exercise files (contains, aggregate, ipv6_compress) | 13 (1 MEASURED) | pytest `test_cidr.py` (hypothesis vs ipaddress: network/broadcast, contains, aggregate = collapse_addresses, IPv6 compress/expand), `test_lpm.py` (trie = linear on 300 prefixes, <= 32 steps, header forward, NAT, fragments), `test_routing.py` (DV = Dijkstra on 60 random graphs in <= n-1 rounds, count-to-infinity +1 per round), `test_figures.py` | 4/0/0 + 1 chart + 1 photo | 13 (+11 sources) |
| 19 `transport-layer` | 11 + 4 | 17 files (Python: channel.py simulator (NORUN), stop-and-wait, go-back-N, selective repeat, SR window too wide, hook file copy across a bad link, RTO estimator, TCP state machine, UDP header, AIMD and the throughput law, two-flow fairness, loopback bulk transfer (MEASURED), 3 exercise programs: wrong GBN ack, fast retransmit, RTT unfairness) | 14 (1 MEASURED) | pytest `test_protocols.py` (hypothesis seeds: SW, GBN at W = 2^k - 1, SR at W = 2^(k-1) deliver the exact stream under loss and duplication; reordering only with k = 8, W = 31), `test_window_limits.py` (staged SR failure, window asserts, RTO rules, state machine, law within 3 % at small p, AIMD fair, MIMD keeps the ratio), `test_figures.py` | 3/0/0 + 2 charts | 10 (+8 sources) |
| 20 `application-layer` | 13 + 4 | 19 files (Python: dns_message.py (wire format, compression, backward-only pointers), zone.py (root, test, brenmoor.test servers; NORUN), resolve.py (iterative), dns_demo (UDP 44200), resolver_cache (rT/(1+rT)), http_server.py (NORUN), http_demo (raw request; 20 vs 1 connections), hol_blocking model, visit.py hook, budget.py, TLS session tls_demo.sh (openssl self-signed cert, tls_echo, tls_wrong_name, tls_overhead via MemoryBIO; the three .py NORUN), 4 exercise programs) + 2 exercise files (chunked, caching_resolver) | 13 | pytest `test_dns.py` (hypothesis round trips of all six types, compressed <= plain, loops and forward pointers rejected, resolution + caching resolver with a hand-moved clock), `test_http.py` (keep-alive + HEAD + 404 on one connection, dechunk, cache law), `test_tls.py` (skipped without openssl: verified, wrong name refused, 22 bytes per record) | 5/0/1 | 15 (+10 sources) |
| 21 `finite-automata` | 13 + 4 | 13 files (Rust: automaton.rs library (Dfa: run_from, complete, complement, accessible, co_accessible, count_accepted; Nfa: closure, step, accepts, determinise; kth_from_end; product; NORUN), dfa_demo hook (table + loop), epsilon, subset, blowup (k = 1..12, all 8 386 560 pairs at k = 12 told apart), product (+ trim), simulate_vs_determinise (MEASURED), 6 exercise programs) + 2 exercise files (factor_aba, multiples) | 12 (1 MEASURED) | crate `tests/automata` (subset = simulation on 60 random NFAs with spontaneous moves, all words up to length 10 or 7; blow-up exactly 2^k for k <= 10 and the language checked; product/complement by brute force; trim; exercises vs brute force) | 3/0/0 | 2 (+2 sources) |
| 22 `regular-languages` | 15 + 1 | 17 files (Rust: regex.rs library (Re tree, smart constructors, recursive-descent parser with classes/ranges/+/?/{m,n}, `lang` denotation, Berry-Sethi `walk`, bit-set `Matcher`; NORUN), dfa.rs library (determinise Glushkov, Moore, minimise, `difference` BFS, state elimination; NORUN), glushkov, thompson, eliminate, minimise, equivalent, engine_compare (MEASURED), minimise_bench (MEASURED), streets (town data), 7 exercise programs; Python backtracking.py (MEASURED, each n in its own process with a 60 s timeout)) + exercises/hopcroft.rs | 16 (3 MEASURED) | crate `tests/regex` (engine and DFA vs denotation on all words up to length 8 for 14 samples, steps <= (m+1)n, parse errors, minimisation canonical (isomorphism by joint walk), Hopcroft = Moore, elimination round trip); pytest on the chart data | 4 + 1 chart | 6 (+6 sources) |
| 23 `context-free-languages` | 17 + 2 | 19 files (Rust: grammar.rs library (Sym, parse, show, nullable, `words`/`generated` fixed point, `leftmost` BFS, `cnf` START/TERM/BIN/DEL/UNIT, `reachable`, `cyk` with split count, `accepts`; NORUN), count.rs (tree counts on spans; NORUN), pda.rs (Move/Pda, bounded search, `from_grammar`; NORUN), hook, derive, ambiguity, cnf, cyk, count_trees, pda_demo, markup, cyk_cost (MEASURED), 8 exercise programs) + exercises descent.rs, bigcount.rs | 17 (1 MEASURED) | crate `tests/grammars` (CNF shape + CYK = generated words on 9 grammars up to length 8 or 6, split count = (n^3-n)/6, tree counts = Catalan in u128 and big integers, unambiguity of the levelled grammar, grammar PDA = generated words, leftmost derivations valid step by step, descent recogniser) | 5 | 3 (+3 sources) |
| 24 `predicate-logic` | 18 + 4 | 23 files (Python: formulas.py (terms, formulas, `free`, capture-avoiding `subst`, parser, printer; NORUN), structures.py (finite structures, satisfaction with an atom counter, `counterexamples`, the town as a structure; NORUN), checker.py (natural deduction, rules for all connectives, raa, forall i/e with side conditions, `extra` rules; NORUN), proofs.py, proofs_more.py, exists_rules.py, unify.py (Robinson + resolvents; NORUN), twosat.py (implication graph + Kosaraju; NORUN), evaluate, substitution_demo, cost, check_demo, unify_demo, refute, twosat_demo, library, 7 exercise programs) | 15 | pytest: test_formulas (hypothesis: substitution lemma, free variables of a substitution, show/parse round trip on random formulas; capture; town rules), test_checker (accepted proofs, propositional conclusions are tautological consequences, 6 refused steps, discharged hypothesis), test_unify_twosat (hypothesis: unifier unifies, most general against random unifiers, occurs check; 2-SAT = brute force on random 5-variable formulas) | 5/0/0 (forest tree with binding arrows, rules table and 4 proof trees in mathpartir, countermodel, implication graph) | 7 (+7 sources) |
| 25 `text-algorithms` | 15 + 4 | 26 files (Python: text_gen.py (the town archive, 1,503 lines from loans and weather; NORUN), naive, boyer_moore (bad-character rule), kmp (failure + search stopping when the pattern no longer fits; prints tables), kmp_automaton, rabin_karp, trie (+ compressed view), lzw (encode with log, decode with the special case), search (hook), rk_demo, trie_demo, lzw_demo, ratio (Huffman / LZW growing widths / zlib), archive_problem, 9 exercise programs incl. Aho-Corasick; C: kmp_bench.c MEASURED) | 18 (1 MEASURED) | pytest: test_matching (hypothesis: 5 matchers + automaton = startswith, KMP <= 2n - m, Rabin-Karp with q = 7; Aho-Corasick and multi-pattern RK; pi = longest border by brute force; naive worst case), test_lzw_trie (round trip on random bytes and the archive, a^n formula to 2000, trie words = filtered sorted set), test_figures | 4/0/0 + 1 chart (bad-character jump, KMP border shift, automaton of ababc, compressed trie, measured naive vs KMP) | 7 (+7 sources) |
| 26 `flows-and-matchings` | 14 + 4 | 20 files (Python: maxflow.py (Network, residual, BFS paths, augment with cancelling, max_flow with a path-finder parameter, min_cut; NORUN), town_net.py (roads as a network, rule: speed - 10 buses an hour; NORUN), matching.py (NORUN), town_flow (hook), flow, bad_example (narrowest vs shortest paths, 2C vs 2), matching_demo, hall (Hall violator from the min cut), disjoint_paths (Menger on the town), selection (project selection by min cut, checked over 32 choices), bus_plan (problem), 8 exercise programs) | 16 | pytest: test_flow (hypothesis: max flow = brute-force min cut on random 6-vertex networks, integrality and conservation, narrowest-path rule gives the same value; bad example 2C vs 2; matching = brute force = flow value; Konig cover size = matching; town numbers) | 4/0/0 (network with flow/capacity and the min cut, residual network with the augmenting path through a reverse edge, the bad example, matching with an augmenting path) | 5 (+5 sources) |
| 27 `randomised-algorithms` | 15 + 4 | 27 files (Python: town.py, quicksort.py (count, first/random pivot, Fisher-Yates), primality.py (Fermat, Miller-Rabin, amplified test), karger.py (contraction by unions over a random edge order) NORUN; sorted_input (hook), quicksort_rand, quicksort_trace (figure, NOPRINT), quickselect, universal_hash (Carter-Wegman draw, adversarial multiples of m), bloom (+ bloom_small), fermat_mr, random_prime, maxsat, karger_demo, friends_problem, 10 exercise programs incl. reservoir, skip list, Las Vegas non-residue) | 19 (1 NOPRINT) | pytest: test_random (quicksort sorts, sorted input quadratic, exact expectation by recurrence = 2(n+1)H_n - 4n to n = 29, quickselect, Carter-Wegman universal exhaustively for p = 31, m = 6, no Bloom false negatives, Miller-Rabin = trial division to 3,000 and Carmichael liars <= 1/4, Karger cut valid and >= brute-force min cut, success >= bound, Fisher-Yates uniform exhaustively n = 4, skip-list search), test_figures | 3/2/0 (quicksort recursion tree, Bloom bits, Karger contractions; charts: longest chain fixed vs universal, Bloom rate vs formula) | 6 (+6 sources) |
| 28 `search-and-games` | 14 + 4 | 21 files (Python: state_space.py (BFS, depth-limited, iterative deepening, A* with an `order` log; h = 0 is uniform cost), games.py (attractor with counters, layers, memoryless strategy), town_map.py (places, coordinates, roads with one-way) NORUN; eight_puzzle (hook), town_astar, attractor (matches + small game with draws), tictactoe (5,478 positions, 549,946 nodes), alphabeta (random trees, best-first ordering = Knuth-Moore formula exactly), minimax_demo, robot_problem (delivery A* over (place, stops left); pursuit game of 1,800 positions by attractor; alpha-beta on noughts and crosses), 8 exercise programs) | 15 | pytest: test_search (hypothesis: A* = Dijkstra with admissible straight-line h on random geometric graphs; town h consistent; BFS = IDDFS = A* depths on the 8-puzzle), test_games (hypothesis: attractor = brute-force fixpoint, strategy lowers the layer; alpha-beta = minimax, best-first count <= formula; matches game; tic-tac-toe value), test_figures (town map .tex regenerates identically; puzzle .dat) | 4/1/1 (8-puzzle state space, town map with Dijkstra vs A* expansions and route, small game with both attractors, alpha-beta tree with cut leaves; chart: states expanded vs depth, log scale; AI image: chess at a cafe) | 3 (+3 sources) |
| 29 `trees-and-clustering` | 15 + 4 | 19 files (Python, standard library only: dataset.py (seeded loans with the planted rule prior >= 2 and distance >= 2500 plus label noise, five planted blobs, twelve named points, 60 members; NORUN), id3 (hook: recovers the rule at depth 2), knn, kdtree, overfit, confusion, kmeans, kmeanspp, hac, loans_problem, 9 exercise programs) | 17 | pytest: test_learning (hypothesis: k-d nearest = brute force; Lloyd cost never increases, step by step; single linkage = Kruskal cut for every k; information gain >= 0; ID3 recovers the rule on noiseless data; entropy values; scaling helps k-NN), test_figures (all figure files regenerate identically) | 4/2/1 (k-d partition, decision tree, k-means three panels, points + single-linkage dendrogram; charts: binary entropy with a chord, accuracy vs depth; AI image: returns desk) | 4 (+4 sources) |
| 30 `database-design` | 18 + 4 | 21 files (Python + SQL: fd.py (closure, keys, minimal cover, BCNF violation and decomposition, 3NF test and synthesis, the chase, preservation; NORUN), wide_build.sql (NORUN), wide_table.sql (hook: member 55's move, 11 of 12 lines), fd_demo, no_preserving, decomposed.sql (lost 0, invented 0), rollback, lost_update (read-then-write, BEGIN IMMEDIATE, update expression), dirty_read (shared cache, read_uncommitted), schedules (simulator: uncommitted, committed, snapshot first-committer-wins; five anomalies), explain.sql, index_timing (MEASURED), redesign (problem), 7 exercise programs incl. exo_selectivity (MEASURED)) | 18 (2 MEASURED) | pytest: test_fd (hypothesis: closure = Armstrong saturation; chase lossless = join round trip on random repaired instances; BCNF parts have no violation; synthesis lossless + preserving + 3NF; 2^(n-k) superkeys), test_sql (decomposition round trip; schedules table), test_figures (index chart data) | 4/0/0 (dependency arrows, BCNF decomposition tree, lost-update timeline, index chart log-log; isolation table) | 9 (+9 sources) |
| 31 `project-key-value-server` | 13 + 3 | 27 files (Rust, standard library only: protocol.rs (Command, Reply, parse, MAX_LINE 1024), store.rs (Store trait, OneLock, Sharded with read-write locks per shard), log.rs (CRC-32, length-prefixed records, replay, open cuts the torn tail, rewrite = compaction by temp file, sync, rename, directory sync), server.rs (one at a time, thread per connection, pool), client.rs (NORUN: the five modules), demo, crash_demo (torn record staged by hand), load (MEASURED), 10 exercise programs incl. exo_pipeline (MEASURED); exercises/mset.rs) | 13 (2 MEASURED) | Cargo crate tests/kv: 10 unit tests (protocol round trip, both stores = a plain map, 8 threads lose nothing, CRC check value, replay of every prefix, a flipped byte stops replay at its record, torn tail cut, compaction replays the same map, MSET atomic under load) + end_to_end.rs (kvserver binary over TCP, killed with SIGKILL, acknowledged prefix durable; guard kills the child on drop); pytest test_figures | 4/0/1 (architecture, record bytefield, crash timeline, load chart; test table; rack AI image) | 0 |

- **Ch. 1 notes.** As briefed, except: the class with an invariant is `Fraction` (not a counter); the
  LeakSanitizer idea of the hook was dropped (glibc keeps every `FILE` reachable, so LSan reports
  nothing): the hook counts open descriptors with `fcntl` before and after instead (3 -> 13; C++: 3 -> 3);
  the problem's write failure uses `/dev/full` (the text says it is a Linux device). Exercise 12's
  `Matrix` uses copy-and-swap assignment (the implicit one breaks the invariant on a throwing copy: the
  solution says so; ch. 2 returns to it). Body 19 pp is above the ~14 target, like Books 3 and 5 (15-18):
  printed ranges were already trimmed once (mains not shown when they repeat); later chapters print fewer
  exercise listings.

- **Ch. 31 notes.** Project chapter: milestones (protocol, store, log, server, load test), 12 exercises
  (4/5/3), no weekend problem. Ports 44310--44319. A DEL of a missing key is not logged. The kill test
  spawns the `kvserver` binary and kills it with SIGKILL: a single `write` is never torn by a killed process,
  so the test checks that every acknowledged change survives, and the torn record is staged by hand in
  `crash_demo`. A tail of zeros has a valid CRC (CRC-32 of nothing is 0): the parse of the payload catches it,
  and the text says so. Over TCP sharding barely matters (about 150 us per round trip); exercise 12
  (pipelining) shows the round trip is the cost. No web fetch.

## For the shared docs

- See `BRIEFS.md`, "For the shared docs (Phase A traps)".
- **Ch. 2 notes.** Brief defect fixed: the named result said "fewer than $n/(r-1)$ transfers", which the run
  itself refutes (1023 transfers for n = 1000, r = 2); the true bound is $\frac{r}{r-1}(n-1)$, nearly reached
  just above a power of two (exercise 11 proves tightness). The S1/S2 figures share one drawing (shallow | deep).
  Exercise 2's ASan run goes through a clean-environment session (`run_selfassign.sh`, the Book 3 pattern):
  a heap-use-after-free report prints stack addresses that depend on the caller's environment (OLDPWD), so the
  plain capture did not rerun byte for byte. `counting.hpp` is named `tracked.hpp`; a `pipeline.cpp` listing was
  added for the problem.
- **Ch. 3 notes.** The hook is the fines `switch` in C (`fines_switch.c`) rather than `shapes_switch.c`; the town
  data has books only, so the three kinds are policies by genre (comics; science and history = study; the
  rest standard) and maps appear only as the planned fourth kind. The library demo runs as a session
  (`run_library.sh`, `copy=` the two CSVs). The Simula box cites Stroustrup's FAQ and the HOPL paper's
  Crossref record (Wikipedia is not a source; ACM DL refuses scripts). `ctor_order.cpp` added; the virtual
  call in a constructor is exercise 5. New source key CROSSREF in the Book 4 ledger.
- **Ch. 4 notes.** The hook is `int_vec.c` (int and `void *` arrays). `generic_stack.cpp` and
  `tests/stack_test.cpp` dropped (the heap of exercise 10 covers a generic container with a comparator);
  `sort_qsort.c` + `sort_std.cpp` became one MEASURED program `sort_compare.cpp` timing both on the same
  input. S2 (compile pipeline) and S1 (one template, instantiations) are one figure. `Vec<T>::reserve` gives
  the strong guarantee (builds the new block before destroying the old; tested with a throwing copy).
  Exercise 12's largest row is N = 67, not 66 (C(67,33) < 2^64 < C(68,34)). Fixed a series-wide pitfall in
  my files: `\&`, `\{`, `\}` inside `\code{}` print the backslash (\code detokenizes); now bare.
- **Ch. 5 notes.** The red-black tree figure was read from libstdc++'s own nodes (a scratch program walking
  `_Rb_tree_node_base`) and recomputed by CLRS insertion: same shape and colours. Buckets figure from
  `buckets.cpp`'s output (13 buckets). ASan stack-use-after-return needs `ASAN_OPTIONS=detect_stack_use_after_return=1`
  with GCC 11: shown on the session line. `onecs.sty` append (under `% Book 4:`): `\DisableLigatures[<,>,-]` for
  tt, since T1 lmtt printed `--` in `\code{}` as an en dash (series-wide: affects every `--it`, `--release`,
  `--version` in every book; the listings were unaffected). Two `Overfull \vbox` in the one-page index (multicol
  balancing) remain: they depend on the index length; recheck at Phase C, before touching the entry file.
  Book 5's ledger has 5 problems (its CROSSREF keys), not mine. Exercise 12 and Part IV of the problem rest on
  MEASURED listings printed in the solutions (`exo_workload`, `crossover`): crossover sorted vector vs map at about
  10^4 keys.
- **Ch. 6 notes.** Rust 1.97's panic message prints the thread id (`thread 'main' (625201) panicked`), a
  per-run number: `char_boundary.rs` installs a panic hook that prints location and message only, and the caption
  says why. The C dictionary (`dict.h`, open addressing) carries the three bugs as `-DBUG=1/2/3` (use after
  free across a growth, double free of a borrowed word, words kept in a reused `getline` buffer); `dict_bugs.rs`
  writes the same three with `--cfg bug1/2/3`: E0499, E0507, E0597. `\code{}` cannot print non-ASCII under
  pdfTeX (detokenize splits the UTF-8 bytes: `Café` printed `CafÃ©`): non-ASCII words go in prose. Page
  budget: chapters 1-6 average 17 pp + 4 of solutions; tightening from ch. 7 (fewer printed outputs, shorter
  problems' statements).
- **Ch. 7 notes.** Weather log defects from the run: 6 missing temperatures (lines 60, 213, 457, 616, 648, 717),
  2 error codes -99.0 (59, 706), 1 duplicate (332, Riverside 2025-06-14); 722 readings kept. `#` inside a macro
  argument (an `\omoutput` caption) is a fatal "Illegal parameter number"; inside exercise/problem bodies
  `\code{#...}` prints `##`: write such code in prose. **Series-wide sty fix (append, `% Book 4:`):** the
  weekend-problem look-ahead of `\section` stopped at the `\label{sec:...:problem}` every chapter writes, so the
  page broke after the heading and left it alone at a page foot (Books 3 and 4 at least); it now steps over
  `\label`s and emits them after the heading. Other books' pagination moves at their next build.
- **Ch. 8 notes.** At opt-level 3, `trip_speed_typed` and `trip_speed_raw` are merged by LLVM into one body
  (same section, same 0xbd bytes; `-C llvm-args=-enable-merge-functions=false` does not stop it): the problem's
  named result is stated on that. `-C symbol-mangling-version=v0` + `nm -C` shows `mono::largest::<u32>`/`<f64>`
  with no hash. rustc 1.97 says "dyn compatible" for object safety: the definition gives both names. `impl Add
  for bool` is an orphan-rule error: exercise 10 uses a newtype `Reach(bool)`.
- **Ch. 9 notes.** Stack overflow aborts with SIGABRT; bash prints its own `Aborted` job line with a PID: the
  session runs the program under `sh -c '...; exit $?' 2>/dev/null` and prints the status itself. At opt-level 3
  the non-tail recursion still overflows a 1 MiB thread stack (shown). The spreadsheet run: 100 cells, 1000 edits,
  5891 distinct nodes under the bound 8100 (100100 for full copies); exactly 7 nodes shared by versions 0 and
  1000. Listing lines over ~94 characters wrap in print (many in ch. 1-6 do): kept under 95 from ch. 9 on.
- **Ch. 10 notes.** As briefed, with these changes: no separate `encoding.sh` (the `rv=asm` directive on
  `constants.S` and `exo_encode.S --fields` does it); `strcmp`, `max`, `bsearch`, `fib`, `switch2`, `loan_fine` and
  the fixed `exo_ra` are exercise programs tested through the rv Python API (capture runs `listings/` only, so their
  results are stated in the solutions, checked by the test). The register file is a table, not a drawing. Problem:
  `count.S` prints the check digit and `--stats` gives exactly 14n + 26 instructions (a = 14, b = 26), checked on
  1, 2, 4, 7 and 9 digits. Labels named `s1`, `s2` collide with register names in rv's `la` (it reads them as
  registers): data labels must not be register names. Piping `rv run --stats` into `head` gives a BrokenPipe
  traceback: use `sed -n`. gcc 13 `-O1` prints `endbr64` and `notrack jmp` (CET): the text explains `endbr64` in one
  sentence. Ledger: `b2:rv-cc-saved`, `b2:rv-cc-args`, `b2:x86-64-args`, `b2:rv-origin` (sources X86-64-PSABI,
  RISCV-ABOUT).
- **Page projection (after ch. 10).** Chapters 1-10: 165 pp of body + 39 of solutions, 20.4 per chapter against
  the band's ~14 (+ solutions). Projected Book 4: 31 x 20.4 = about 630 pp of chapters, plus front matter and
  index, about 650 pp, against the outline's estimate of about 450: some 45 % OVER, not under, so no depth is
  being compressed (the 15 % rule concerns compression). The excess is listings and captured outputs, which the
  run file says make chapters longer. Steps to keep it from growing: listing lines under 95 characters (no wraps),
  output ranges instead of whole outputs, and no repeated outputs between chapter and solutions.
- **Ch. 11 notes.** The model is a timing model on rv's `Step` records (in-order, every source needed in EX,
  branches resolved in EX with penalty 2, `jal` 1, `jalr` 2, a perfect target buffer for predicted-taken
  branches); the identity cycles = n + 4 + stalls + flushed holds by construction and is tested. Values: bubble
  sort of 16 (65 inversions) 964 instructions, CPI 1.961 / 1.512 / 1.272 (no forwarding / forwarding / + two-bit);
  named result "CPI from 1.961 to 1.272". On `collatz.S` a one-bit predictor (315 misses) is worse than "not taken"
  (186); two-bit 161. Photograph: MIPS R3000A die (Commons, CC BY 3.0), the book's first. The brief's
  "speed-up" proposition is stated as "ideal gain of a pipeline" (sync: speed-up is never defined here). Ruff's
  line limit is 88, not 95: Python listings are written to 88. **Layout trap:** a problem's `Part ...` heading
  can be stranded at a page foot because the list after it opens with a breakable penalty;
  `\begin{enumerate}[resume, beginpenalty=10000]` (and `\par\nopagebreak` after the heading) fixes it. Ch. 11
  uses it; Phase C should sweep ch. 1-10 for the same strand.
- **Ch. 12 notes.** Cache simulator `cache.py` (OrderedDict per set, LRU, write-back/through, write-allocate);
  `matrix_sum.S` on rv: 1 KiB DM, 32-byte lines: rows 128 misses, columns 1024 (896 conflicts: a column uses 8 of
  32 sets). Measured on the laptop: rows vs columns ~30x; pointer-chase sweep plateaus ~1.1 / ~4 / ~20 / ~150 ns,
  the last step before the L3's 24 MiB (TLB, shared L3: said without numbers); matmul n = 1024 ijk ~10x slower
  than ikj, and blocking is SLOWER than ikj at 1024 (B fits in L3) but faster at 2048 (ikj time x19 for x8
  arithmetic): the text says so. AoS/SoA ~4x. Problem: box blur, simulator N = 256 in a 4 KiB 4-way cache:
  rows 4096 misses (1/16 per pixel), columns 72 704 (exactly 224 x 256 + 30 x 512), strips 3N^2/16 - 2N;
  measured rows ~9x faster than columns (the L2 absorbs the column misses). Widest strip w = 224 (rows start in
  the same set) checked privately by simulation. The 3C classifier is exercise 7, its output printed in the
  text. Photograph: back of two DDR5 SO-DIMMs (Commons, CC BY-SA 4.0); history box Wilkes 1965 / Liptay 1968
  (`b2:cache-wilkes`, `b2:cache-360-85`). `-std=c17` hides `clock_gettime`: `_POSIX_C_SOURCE 200809L` first.
  bytefield needs `bitwidth` around 0.95em for 32 bits with 4-bit labelled fields. 19 pp: the longest so far.
- **Ch. 13 notes.** `strace -qq -e trace=` outputs are byte-stable; `strace -c` is stable once the time columns are
  dropped (awk on $4 and $NF) and PATH is pinned (`PATH=/usr/bin`), else each PATH entry costs a failed execve.
  Budget: minish running `echo hi` = 162 calls, empty script 41, echo alone 115: one command adds 121 = 5 in the
  shell (read, ioctl from isatty, write, clone, wait4) + set_robust_list in the child + 115 in echo (verified on a
  per-pid trace). `fork` after buffered `printf` duplicated lines (wait_status): fflush before fork; `_exit` loses
  an unflushed child line (cd_child). Inside `\code{}` write `$` and `&` bare: `\$` and `\&` print their
  backslash (detokenize). `/proc/<pid>/task/<pid>/children` exists here (ptree sorts by name). No PID printed
  anywhere. Book 2's g12 chapter is still a placeholder: the recall names Book 2 without a reference.
- **Ch. 14 notes.** `strace -P file` traces only calls on that file, so the read count of a copy is exact
  (100 001 ... 3 for n = 100 000), but it prints a "Requested path resolved" note unless given an absolute path:
  the count loop lives in `reads.sh` with `-P "$PWD/in.txt"`. Measured 4 MiB copy: time ~ reads at small b
  (1619 ms at b = 1), flat past ~2 KiB; fitted a ~375 ns per read+write, c ~0.2 ns/byte, crossover b ~1.7 KiB;
  `putc` ~240x faster than b = 1 (glibc flushes a file stream in 4096-byte writes: checked with strace). Ex. 5's
  point: a `printf` without newline is duplicated by fork on a terminal too. Ex. 9 differs from the brief (the
  k-stage builder is the chapter's own listing): `capture(argv, input)`, with the two-full-pipes deadlock as the
  question. minish2's children must unblock SIGCHLD (the mask survives exec). Ex. 8's corollary needs "every
  stage reads to the end" (head does not). The brief's `strace -c` session became the `-P` count. The brief's
  POSIX `stat` ledger row was not needed (fields named in the text, no numbers).
- **Ch. 15 notes.** Explorer `interleavings.py`: steps (label, guard, action), memoised path counts per state, so
  the bakery's 1.05e11 schedules (3 threads, one pass) cost 4579 states and the two-pass 6.7e24 in about a second.
  "Inside" = next step labelled "critical section". Named result: atomic take, 2 windows x 4 customers x 2 steps,
  6 seats: 12 870 schedules, 0 bad; locked: 70 = C(8,4). `race.c` uses relaxed atomic load + store (defined
  behaviour, still loses updates): 1/2/4/8 threads lost 0/~45/~73/~83 %; MEASURED, chart regenerated from the
  output (rerunning capture changes the numbers: regenerate `lost.dat` after any capture of race). ThreadSanitizer
  works here only under `setarch -R` (else "unexpected memory mapping"); the session pipes through `trim.sh` to drop
  pid, addresses and module offsets. The philosophers' deadlock is made deterministic by a barrier before releasing
  the left fork. "deadlock" is Book 5's term: used, recalled from Book 2, never defined; data race, starvation,
  thread, lock, semaphore, condition variable, atomic operation (informal), critical section, interleaving defined
  here. Exercise models whose outputs the solutions print live in listings/ (outputs only come from listings).
  First AI illustration of the book (ticket office, Codex, 65 s). Brief deviations: no `mutex_counter.c` (race.c
  holds the mutex and atomic versions), Rust `race_refused.rs` shows E0373 (ch. 6 already printed E0499).
- **Ch. 16 notes.** Ports 44160-44169 all used by listings; tests reuse 44164 (wrong_port never binds it) and 44166
  (the demo's). `tools/test_code.sh` compiles every `*_test.c` as a C test: a listing named `load_test.c` was taken
  for one; renamed `loadtest.c`. Child processes that print must `exit` (not `_exit`) or `fflush`, else the line is
  lost when stdout is a file. The load test (4000 one-request connections per design, 8 client threads) gives
  about 12-13k / 26-30k / 45-54k requests per second (process / thread / poll); each capture leaves 12 000
  TIME_WAIT sockets for a minute, so two captures within a minute are the most to run (28 231 ephemeral ports).
  Solutions of ex. 11 and Q22-24 quote the printed run: never recapture `load` without updating them and
  `designs.dat`. Brief deviations: echo server and client merged into `echo_pair.c`; `partial_recv.c` prints only
  yes/no, so it is not MEASURED; `udp_pair.c` became `boundaries.c` (TCP and UDP side by side).
- **Ch. 17 notes.** All Python except `crc32.c`; no NORUN, no MEASURED (the ALOHA, backoff and random-error
  simulations are seeded). CRC-16 is x^16 + x^12 + x^5 + 1 (PPP's FCS-16 polynomial, RFC 1662), MSB first, start
  0, so codeword checks are plain divisibility: bursts <= 16 bits on a 48-bit frame: 1 114 111 tried, 0 pass;
  length 17: exactly 32 (= positions); 2^24 random patterns: 256 pass (expected 256, all even weight). Ethernet's
  CRC-32 generator sourced from RFC 3385 (0x104C11DB7), zlib/gzip's from RFC 1952; frame sizes from the installed
  `if_ether.h` (ledger source LINUX-IF-ETHER). Brief deviations: the CRC long division (S2) and the switch table
  (S4) are printed outputs, not TikZ; one photograph (RJ45 plug, CC BY-SA 3.0) instead of two, the AI image covering
  the switch ports; ex. 11 checks CRC-16 bursts by the x^i B reduction (lengths 17 and 18) instead of an exhaustive
  CRC-32 run (2^31 patterns, too slow in Python); ex. 4 uses the message 1101 0011. TikZ trap: a colour given as a
  bare option on a node with `fill=white` also sets its fill; use `text=colour`.
- **Ch. 18 notes.** Every printed address is in 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, 2001:db8::/32 or
  (NAT only) 192.168.0.0/16; ch. 17 used 10.0.0.x for ARP (private, ledgered here). The hook is a simulated
  traceroute over the town (router k = 198.51.100.k, Dijkstra next hops), never a real one (it would print the
  author's provider). Town network: 30 routers, 53 links (road 1's one-way ignored), DV by length 8 changing rounds =
  Dijkstra; by hops 7; Lighthouse Cafe router crash: count to infinity 15 rounds (min distance = r + 1).
  Poisoned reverse: line cured in 2 rounds, triangle + D still 15 (trace checked: the stale route circles A->B->C).
  Bench (laptop): linear 218/879/3581 us vs trie 1.9/2.4/2.9 us per lookup at 250/1000/4000 prefixes; solutions of
  ex. 11 quote them loosely. Brief deviations: S5 DV tables are a printed output; fragment.py's code appears only in
  ex. 9's solution (the text prints its output); ipv6_text.py expands, the exercise compresses. The IANA 2011 news
  URL is gone (404); the NRO release sources the date.
- **Ch. 19 notes.** Everything runs in a seeded discrete-event simulator (`channel.py`: 50 ms one way, 1 ms per
  packet). Finding: the GBN and SR window limits assume a FIFO channel; with reordering (jitter) a late old ack or
  packet is misread once reordering exceeds the slack M - W, so the demos use no jitter at full windows and the
  tests reorder only with k = 8, W = 31; the text says TCP's 32-bit byte numbers exist for that reason. Receivers
  record the time of the last delivery (the last timer event overstated transfer times). Fast retransmit that resent
  only the base was slower than plain GBN; it goes back N at the third duplicate ack (54.0 s -> 24.7 s, same packets
  sent). Law check: periodic losses -9.3/-4.6/-2.5/-1.7 % at p = 0.01..0.0003, random +1.7..+6.7 %. Bulk transfer
  (laptop, port 44192): receive buffer 4096 / 65536 / default ~ 0.8-1 / 4.9-5.5 / 5.6-5.9 GB/s; text quotes no
  number. Brief deviation: the TCP state diagram is a printed run of `tcp_states.py` plus a handshake/close timeline
  (TikZ) with the states marked, not a full automaton drawing; the stop-and-wait timeline became the
  sliding-window figure. QUIC is in a `dated{2026}` box.
- **Page projection (after ch. 19, before ch. 20).** Chapters 1-19: 295 pp of body (printed pp. 2-296) + about
  99 of solutions (pp. 311-409), 20.7 per chapter; chapters 11-19 alone: 14.6 pp of body each (131 pp), plus about
  5 of solutions, about 19.5. Projected: 393 + 12 x 19.5 = about 627 pp of chapters, plus front matter and index,
  about 650 pp (the PDF now has 422 with 12 placeholder chapters) against the outline's ~450: about 45 % OVER, as
  at ch. 10; nothing is being compressed, so the 15 % rule does not apply. The body per chapter is now close to the
  band's ~14; the excess is solutions with printed listings and outputs. Kept: one-range listings, output ranges,
  no repeated outputs.
- **Definition-map check (after ch. 19).** A script comparing `DEFINITIONS.md` labels with the written chapters
  found chapters 1-14 and 19 complete, but chapters 15-18 merged or left in prose 27 mapped definitions
  (15: barrier, bounded-buffer, mutex-property, race, rwlock; 16: blocking, kinds, listening, loopback,
  network-order, port; 17: aloha, arp, burst, edc, hidden, inet-checksum, mac-address, mac-protocol, switch;
  18: as, dv, fragmentation, ipv6, ls, routing, ttl). Ch. 19's seven were added at once. **Phase C task:** give
  each its `definition` (or record the merge in `DEFINITIONS.md` and an EXTRA mapping) before running the linker.
  From ch. 20 on, run the check at each chapter's end.
- **Ch. 20 notes.** Zone `brenmoor.test` (`.test` reserved, RFC 2606): www A 127.0.0.1 (this machine, so the demos
  connect), AAAA 2001:db8::80, mail 192.0.2.25, MX 10, TXT, library CNAME www; the toy network's servers at
  192.0.2.53 (root), 198.51.100.53 (test), 203.0.113.53 (brenmoor.test). The reader refuses any pointer not strictly
  before the current stretch (stronger than the RFC, which says only "prior occurrence"); the proposition is stated
  for that rule. TLS session: the certificate is made in the session's directory by a hidden `openssl req` line
  (EC P-256, one day), so nothing secret is kept in the repo; cipher printed TLS_AES_256_GCM_SHA384, 22 bytes per
  record (5 + 1 + 16). The check_prose gate allows e-mail addresses only at example.org/com/net: the SMTP dialogue
  uses `ada@example.org` -> `clerk@example.net`, not the town. Brief deviations: S2 (iterative resolution) is drawn
  on the name tree (S1) as numbered arrows, plus the printed trace; S4 (HTTP/1.1 vs HTTP/2 timeline) is the printed
  `hol_blocking` model, with HTTP/3 added; the HTTP/2 frame header is a bytefield instead. All seven DEFINITIONS
  labels are present (checked by the script).
- **Coordinator note (echo_input tracebacks), 2026-11-20.** Checked: no Book 4 output prints a Python traceback (no
  `Traceback`, `runpy` or `echo_input` in any `code/bachelor-2/*/outputs/*.txt`), so no `\omoutput` range hid
  those frames; nothing to recapture.
- **Ch. 21 notes.** All Rust; listings reach the library with `#[allow(dead_code)] mod automaton;` (a listing that
  is also a module, `dfa_demo.rs`, makes its two functions `pub` so `exo_runs.rs` can reuse them). Measured (laptop):
  NFA with ordered sets 100-180 ns/letter, with bits 5-8, DFA 4-6 ns/letter up to k = 10 but 62-96 at k = 16 (65 536
  states, cache misses) after an 80 ms build. Brief deviations: S3 is the NFA only (the 8-state DFA is the printed
  table of `subset.rs`), S4 and S5 are one figure (the product with its useless states greyed); the measured
  comparison is in the text, ex. 11's solution prints the bit simulation. Build trap: two `latexmk` runs on the same
  entry at once (a background run still going) left a truncated aux/idx and "errors 2"; a single clean rerun fixed it.
- **Ch. 22 notes.** 17 pp (322-338). Measured (laptop): Python `re` on `(a|a)*b` and a^n doubles per a, 6.6 s at
  n = 27; the Glushkov matcher 2n - 1 unions, 73 ms for 10^7 letters; Moore vs Hopcroft within a factor 2 either way
  (Moore needs only k + 1 ~ log n rounds on that family), so ex. 11's question asks why the gain is small. Brief
  deviations: the brief's `regex_ast.rs` + `parse.rs` are one library `regex.rs`; S4 is the minimal automaton drawn
  (the class table is the printed output); S3 uses "ends with b", not the multiples of 3 (those are an output).
  `onecs.sty` append: `literate` for ε and ∅ in listings (pdflatex stops on them: "Invalid UTF-8 byte sequence");
  the global `\lstset` did not reach `\omoutput` (style `omout` re-applies `style=om`), so a second append
  redefines style `om` with the longer list (all other keys copied unchanged); thompson.rs prints `a?b?c` anyway. Capture trap: `capture_output.py CH minimise` matches every stem *starting* with
  `minimise`, so it re-measured `minimise_bench` too; text adjusted to the new numbers.
- **Ch. 23 notes.** 14 pp (339-352). Outputs now print ε (second `onecs.sty` append). The tree counter needs the
  "each non-nullable symbol takes at least one letter" bound or E -> E + E recurses on the same span. CNF adds the
  new start only when the start is nullable and used on a right side (the expression grammar then keeps E). Markup
  notices use \code{} in text and solutions, since < > * in math get relation spacing. Brief deviations: no
  propositional-formula listing (the grammar is given in the text); `pda.rs` is the library and `pda_demo.rs` prints.
  Cross-book refs to Book 5 are in words ("the Year 3 volume's chapters on parsing"), never \cref.
- **Ch. 24 notes.** 18 pp (353-370), solutions about 4. Brief deviations: the sync added unification, resolution and
  2-SAT (sections 7-8, with `met:unify`, `thm:mgu`, `thm:2sat`), so exercises 3 (unification) and 4 (implication
  graph) replace the brief's evaluator and naive-evaluation exercises; the checker has the forall rules in the text
  (the wrong forall-introduction is the demo), so exercise 9 adds the exists rules through `check(..., extra)`.
  Year 1 refs must be in words too: `\cref{def:b1:...}` is undefined in Book 4 (no cross-document refs). mathpartir
  \inferrule works in omfigure and in inline math; two trees side by side stack when too wide, which reads fine.
  A bracket in an \omcode caption (`$A[y/x]$`) breaks the build ("\ttfamily invalid in math mode"): reword. The
  evaluation shows a real data defect: 4 books are out to two members at once (loans table), used in the problem.
- **Ch. 25 notes.** 15 pp (371-385). KMP stops when the pattern no longer fits (`i - q > n - m`), which gives the
  exact 2n - m of the theorem (checked exhaustively on {a,b} up to n = 12, and attained on a^n with a^(m-1)b, ex. 8);
  without the stop the count is 2n - 1. The archive is generated from the town's loans and weather tables
  (`text_gen.py`, no download, no randomness). Brief deviations: exercise 3 is the period shift after an occurrence
  (the BM listing already finds all occurrences); exercise 8 is "the bound is attained" (the theorem is proved in the
  text); exercise 10 is the rigorous random-prime version of the spurious-hit bound (the proposition is stated under a
  model). Forest edge labels: a `\forestset{el/.style=...}` with `pos=0.72` and wide `s sep`; midway labels collide.
- **Ch. 26 notes.** 14 pp (387-400). Brief deviations: S1 and S3 are one figure (the flow with its cut drawn), so 4
  figures; the propositions flow-across-cut and the distance-monotonicity lemma are stated in the text with their proofs
  in exercises 8 and 11, as the brief's exercise list asks; Hall is proved in the text from Konig (short), and from
  max-flow min-cut in exercise 10; listing `matching.py` relies on the admitted fact that a left vertex with no
  augmenting path never gets one later. Found while writing: in the town, widening road 16 (in the BFS-side minimum cut)
  gains nothing, because the cut nearest the ground (the five roads into the ground) also has 120; only roads in every
  minimum cut (11, 20) help, and then the depot's own roads (140) bind. The problem is built on that. `add_edge` adds up
  capacities on a repeated pair: a test that added slot-to-sink edges once per reader found it.
- **Ch. 27 notes.** 15 pp (401-415). Data finding: the brief's problem assumed "three groups joined by a few bridges,
  person 40 set aside"; the friendship table actually covers people 1-39 only, in two groups (29 and 10) with no
  friendship between them, and many people with one friend, so the minimum cut is 0 overall and 1 in the larger group
  (7 bridges, all found about equally). The problem was rebuilt on that: hand contractions on the 10-person group, the
  larger group (min cut 1, 7 cuts, 73 % success against a 0.25 % bound), and its 2-core (22 people, min cut 2, 15 cuts,
  the 9-person community split found in 5.6 % against 0.43 %). Brief deviations: Carter-Wegman is proved in the text
  (short), so exercise 10 is the longest-chain bound E[L] <= 1 + sqrt(n) under universality; Fisher-Yates and the
  comparison probability are stated in the text with proofs in exercises 11 and 8; `shuffle_bias.py` is
  `exo_shuffle.py`; the test of the chart data is in `tests/`, not `figures/`. Adversarial keys for the universal
  family are random multiples of m: an arithmetic progression of multiples gives a heavy-tailed chain law whose
  1,000-draw mean exceeded the expectation bound, which would have confused the reader.
- **Ch. 28 notes.** 13 pp (426-438). Brief deviations: the problem's pursuit game is robot-to-the-Library against a
  rival that catches it by sharing a place (1,800 positions: 784 robot, 202 rival, 814 draws), roads taken both ways
  on foot; alpha-beta measured on random trees b = 4, d = 8 (511 of 65,536 best first, exactly the formula) and on
  noughts and crosses (7,330 of 255,168 games); the best-case proposition is admitted, with the Knuth-Moore
  characterisation sketched. Iterative deepening on the 8-puzzle expands about 7 times what BFS does at depth 20, well
  above b/(b-1), because the state space is a graph: said in solution 3. A* with 3x the straight line returns a longer
  route Bus Depot -> Bakery Corner (4,800 against 4,360 m). Found and fixed: `\admitted` inside a `proof` printed
  "Proof. Proof." (also in ch. 27, fixed there); `\admitted` is a whole proof by itself.
- **Ch. 29 notes.** 15 pp (440-454). Brief deviations: the binary-entropy chart is an extra figure (the concavity proof
  of gain >= 0 reads off it); a lemma `lem:b2:trees-and-clustering:centroid` is added for the Lloyd proof; Lloyd's
  termination is proved in solution 8 through D(a), the cost with centroids, because the recorded cost depends on two
  consecutive assignments; exercise 9 (complete linkage) works on the twelve named points, since on the planted blobs all
  three linkages agree; exercise 6 (identifier column) found that the gain ratio does NOT save ID3 here (0.093 for the
  loan number against 0.064 for late returns): the solution says so. Data: one validation split of the problem gives
  30.2 % late in training and 21.7 % in test, by chance (two standard deviations), discussed in the problem. Lloyd 1957
  is sourced from Wikipedia only (Crossref has the 1982 paper, no note on 1957).
- **Ch. 30 notes.** 18 pp (444-461). Brief deviations: `transaction.sql` dropped, because the frozen `sqlrun`
  commits after every non-query statement, so BEGIN/ROLLBACK in a .sql listing fail ("cannot rollback - no transaction
  is active"); the transaction is shown in Python (`rollback.py`) and the text says the runner commits after each
  statement (reported for the shared docs). SQLite shows only dirty reads (shared cache + read_uncommitted) and the lost
  update; the other anomalies are shown on a small schedule simulator (three read rules), and the standard's table is
  sourced from PostgreSQL's page. Town data findings: due = out + 21 on every loan and the 80 titles are distinct, so
  out -> due and title -> book hold in the data without being rules (exercise 9 and problem Q4-Q5); one of the 24 streets
  has no member, so the decomposed streets table has 23 rows. MVD/4NF: one definition with the book-author-keyword
  example, the chase told in exercise 5, not defined. The index chart reads the captured MEASURED output; on this
  laptop the index is ~960x faster at 1M rows (two recaptures gave 960 and 1476 under load: the text says "about a
  thousand"), and the selectivity crossover lies between 5 % and 10 %.
- **Phase C notes.**
  - **Port ranges sit inside Linux's ephemeral range (32768-60999).** A client that closes first leaves its
    ephemeral port in TIME_WAIT for a minute, and a socket that connected without `SO_REUSEADDR` blocks any later
    `bind` of that port, even with `SO_REUSEADDR` on the server. Ch. 16's `loadtest.c` (12,000 short connections)
    so made fixed ports of chapters 16 and 20 fail at random in a full `test_code.sh bachelor-2` run, and it can do
    the same to another book's range while both run. Fix (not printed): the load generator's client sockets set
    `SO_REUSEADDR` before `connect` (checked: a client TIME_WAIT then no longer blocks a bind). Any series tool or
    book that opens thousands of connections should do the same. A VS Code server listens on 127.0.0.1:44931 on
    this machine (not a Book 4 port).
  - Long listing lines: 68 printed lines over 95 characters in ch. 1-8 (and one in ch. 13). Comment padding shrunk,
    11 comments shortened, 32 lines split with every later `\omcode` range to the same file shifted; one ASan output
    recaptured (`run_selfassign`), whose line numbers the solution quotes (now 15 and 29).
  - Term links: 4141 links, 626 linkable terms. Stoplist of about 100 ordinary words or words with another sense
    in the book (cache, frame, flow, cut, child, parent, window, matching, word, language, index, sequence...),
    protections for "sequence" (harvested from sequent), Poisson process, "in process", group commit,
    good-suffix and "-fold" words.
  - Figure pass over 127 figure pages: three label overlaps fixed (pipe wiring of ch. 14, regex timing legend of
    ch. 22, decision-tree edge labels of ch. 29). 10 rasters: 6 AI images (JPEG, no grey stub), 4 photographs.
  - Ch. 16's load output recaptured on a busy machine (3662 / 7331 / 10917 requests per second, ratio 3.0): the
    solution's model numbers were redone from it (r = 91.6 us, f = 45 and 180 us, q >= 18).
  - Two more flaky outputs made deterministic: ch. 16 `exo_loop` (the server's echo reached a client that had
    already closed, so a reset sometimes turned one `recv` into -1: the client now reads the echo first; printed
    range 25-30) and ch. 1's staged failures `const_error` and `exo_dangling` now carry `capture: exit` on a blank
    unprinted line (status 1, and -11 for the segmentation fault, which the caption now explains).
