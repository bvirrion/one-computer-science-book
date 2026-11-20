# Data ledger --- Book 5

Book 5's own rows. Shared rows and the rules are in `sources/data_ledger.md`.
Owned by the Book 5 writer; other books may cite these rows read-only.

## Sources

| key | source | URL |
|---|---|---|
| RISCV-PSABI | RISC-V ELF psABI, calling convention (riscv-cc.adoc, integer register convention and argument passing) | https://github.com/riscv-non-isa/riscv-elf-psabi-doc |
| py-sys | Python 3.12 documentation, `sys.getrefcount` | https://docs.python.org/3.12/library/sys.html |
| py-gc | Python 3.12 documentation, `gc.collect` | https://docs.python.org/3.12/library/gc.html |
| rust-rc | Rust standard library documentation, module `std::rc` | https://doc.rust-lang.org/std/rc/index.html |
| posix-mkctx-6 | The Open Group Base Specifications Issue 6 (IEEE Std 1003.1, 2004 Edition), makecontext page | https://pubs.opengroup.org/onlinepubs/009695399/functions/makecontext.html |
| posix-xrat-7 | The Open Group Base Specifications Issue 7 (POSIX.1-2017), Rationale B.3.1 System Interfaces Removed in this Version | https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_xsh_chap03.html |
| usenix-lottery | USENIX conference page of the OSDI '94 paper Lottery Scheduling: Flexible Proportional-Share Resource Management, and its legacy proceedings page | https://www.usenix.org/conference/osdi-94/lottery-scheduling-flexible-proportional-share-resource-management |
| RISCV-PRIV | RISC-V Instruction Set Manual, Volume II: Privileged Architecture, source src/priv/machine.adoc (main branch on the access date) | https://github.com/riscv/riscv-isa-manual/blob/main/src/priv/machine.adoc |
| RISCV-PRIV-S | RISC-V Instruction Set Manual, Volume II: Privileged Architecture, source src/priv/supervisor.adoc and its bytefield figures src/priv/images/bytefield/sv32va.edn, sv32pte.edn (main branch on the access date) | https://github.com/riscv/riscv-isa-manual/blob/main/src/priv/supervisor.adoc |
| man-getrusage | Linux man-pages, getrusage(2) | https://man7.org/linux/man-pages/man2/getrusage.2.html |
| man-mmap | Linux man-pages, mmap(2) | https://man7.org/linux/man-pages/man2/mmap.2.html |
| man-fork | Linux man-pages, fork(2), NOTES | https://man7.org/linux/man-pages/man2/fork.2.html |
| kernel-ext2 | Linux kernel documentation, The Second Extended Filesystem (filesystems/ext2) | https://docs.kernel.org/filesystems/ext2.html |
| hd-photo | Commons description page of File:Laptop-hard-drive-exposed.jpg (Evan-Amos) | https://commons.wikimedia.org/wiki/File:Laptop-hard-drive-exposed.jpg |
| ewd123 | E. W. Dijkstra Archive, transcription of EWD 123, Cooperating sequential processes (Technological University, Eindhoven) | https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html |
| ewd310 | E. W. Dijkstra Archive, transcription of EWD 310, Hierarchical ordering of sequential processes | https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD310.html |
| ms96 | M. M. Michael and M. L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC '96, the authors' copy | https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf |
| cppref-mo | cppreference.com, C reference, memory_order (since C11) | https://en.cppreference.com/w/c/atomic/memory_order |
| posix-cond-wait | The Open Group Base Specifications Issue 8 (IEEE Std 1003.1-2024), pthread_cond_wait | https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_wait.html |
| lamport-multi | L. Lamport, How to make a multiprocessor computer that correctly executes multiprocess programs, the author's copy | https://lamport.azurewebsites.net/pubs/multi.pdf |
| wp-deadlock | Wikipedia, Deadlock (computer science), raw wikitext on the access date | https://en.wikipedia.org/wiki/Deadlock_(computer_science) |
| tso-cacm | P. Sewell et al., x86-TSO: a rigorous and usable programmer's model for x86 multiprocessors, CACM 53(7), the authors' copy | https://www.cl.cam.ac.uk/~pes20/weakmemory/cacm.pdf |
| riscv-csrs | RISC-V Instruction Set Manual, Volume II: Privileged Architecture, source src/priv/csrs.adoc, CSR Address Mapping Conventions (main branch on the access date) | https://github.com/riscv/riscv-isa-manual/blob/main/src/priv/csrs.adoc |
| riscv-hyp | RISC-V Instruction Set Manual, Volume II: Privileged Architecture, source src/priv/hypervisor.adoc, Hypervisor Extension (main branch on the access date) | https://github.com/riscv/riscv-isa-manual/blob/main/src/priv/hypervisor.adoc |
| robin-irvine | J. S. Robin and C. E. Irvine, Analysis of the Intel Pentium's ability to support a secure virtual machine monitor, Proceedings of the 9th USENIX Security Symposium (USENIX copy) | https://www.usenix.org/legacy/events/sec2000/full_papers/robin/robin.pdf |
| man-namespaces | Linux man-pages, namespaces(7) | https://man7.org/linux/man-pages/man7/namespaces.7.html |
| kernel-cgroup2 | Linux kernel documentation, Control Group v2 (admin-guide/cgroup-v2) | https://docs.kernel.org/admin-guide/cgroup-v2.html |
| posix-getrlimit | The Open Group Base Specifications Issue 8 (IEEE Std 1003.1-2024), getrlimit, setrlimit | https://pubs.opengroup.org/onlinepubs/9799919799/functions/getrlimit.html |
| man-chroot | Linux man-pages, chroot(2) | https://man7.org/linux/man-pages/man2/chroot.2.html |
| sep-turing-machine | Stanford Encyclopedia of Philosophy, "Turing Machines" (substantive revision 21 May 2025) | https://plato.stanford.edu/entries/turing-machine/ |
| sep-recursive-functions | Stanford Encyclopedia of Philosophy, "Recursive Functions" | https://plato.stanford.edu/entries/recursive-functions/ |
| bbchallenge-2025 | The bbchallenge Collaboration et al., Determination of the fifth Busy Beaver value, arXiv:2509.12337 (v1 15 Sep 2025, v2 23 Mar 2026) | https://arxiv.org/abs/2509.12337 |
| wiki-pilot-ace | Wikipedia, "Pilot ACE" (article source, citing D. M. Yates, Turing's Legacy, Science Museum) | https://en.wikipedia.org/wiki/Pilot_ACE |
| wiki-pcp | Wikipedia, "Post correspondence problem" (article source) | https://en.wikipedia.org/wiki/Post_correspondence_problem |
| wiki-savitch | Wikipedia, "Savitch's theorem" (article source) | https://en.wikipedia.org/wiki/Savitch%27s_theorem |
| wiki-time-hierarchy | Wikipedia, "Time hierarchy theorem" (article source) | https://en.wikipedia.org/wiki/Time_hierarchy_theorem |
| wiki-space-hierarchy | Wikipedia, "Space hierarchy theorem" (article source) | https://en.wikipedia.org/wiki/Space_hierarchy_theorem |
| wiki-tqbf | Wikipedia, "True quantified Boolean formula" (article source) | https://en.wikipedia.org/wiki/True_quantified_Boolean_formula |
| wiki-immerman | Wikipedia, "Immerman-Szelepcsenyi theorem" (article source) | https://en.wikipedia.org/wiki/Immerman%E2%80%93Szelepcs%C3%A9nyi_theorem |
| wiki-cobham | Wikipedia, "Cobham's thesis" (article source) | https://en.wikipedia.org/wiki/Cobham%27s_thesis |
| wiki-cook-levin | Wikipedia, "Cook-Levin theorem" (article source) | https://en.wikipedia.org/wiki/Cook%E2%80%93Levin_theorem |
| wiki-karp21 | Wikipedia, "Karp's 21 NP-complete problems" (article source) | https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems |
| wiki-garey-johnson | Wikipedia, "Computers and Intractability" (article source) | https://en.wikipedia.org/wiki/Computers_and_Intractability |
| wiki-2sat | Wikipedia, "2-satisfiability" (article source) | https://en.wikipedia.org/wiki/2-satisfiability |
| wiki-christofides | Wikipedia, "Christofides algorithm" (article source) | https://en.wikipedia.org/wiki/Christofides_algorithm |
| wiki-walksat | Wikipedia, "WalkSAT" (article source) | https://en.wikipedia.org/wiki/WalkSAT |
| wiki-sat | Wikipedia, "Boolean satisfiability problem" (article source) | https://en.wikipedia.org/wiki/Boolean_satisfiability_problem |
| wiki-set-cover | Wikipedia, "Set cover problem" (article source) | https://en.wikipedia.org/wiki/Set_cover_problem |
| wiki-dpll | Wikipedia, "DPLL algorithm" (article source) | https://en.wikipedia.org/wiki/DPLL_algorithm |
| wiki-cdcl | Wikipedia, "Conflict-driven clause learning" (article source) | https://en.wikipedia.org/wiki/Conflict-driven_clause_learning |
| wiki-chaff | Wikipedia, "Chaff algorithm" (article source) | https://en.wikipedia.org/wiki/Chaff_algorithm |
| wiki-lin-kernighan | Wikipedia, "Lin-Kernighan heuristic" (article source) | https://en.wikipedia.org/wiki/Lin%E2%80%93Kernighan_heuristic |
| wiki-kraft | Wikipedia, "Kraft-McMillan inequality" (article source) | https://en.wikipedia.org/wiki/Kraft%E2%80%93McMillan_inequality |
| wiki-reed-solomon | Wikipedia, "Reed-Solomon error correction" (article source) | https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction |
| wiki-hamming-code | Wikipedia, "Hamming code" (article source) | https://en.wikipedia.org/wiki/Hamming_code |
| wiki-noisy-channel | Wikipedia, "Noisy-channel coding theorem" (article source) | https://en.wikipedia.org/wiki/Noisy-channel_coding_theorem |
| wiki-crc | Wikipedia, "Cyclic redundancy check" (article source) | https://en.wikipedia.org/wiki/Cyclic_redundancy_check |
| wiki-hoare-logic | Wikipedia, "Hoare logic" (article source) | https://en.wikipedia.org/wiki/Hoare_logic |
| wiki-model-checking | Wikipedia, "Model checking" (article source) | https://en.wikipedia.org/wiki/Model_checking |
| wiki-binary-search | Wikipedia, "Binary search" (article source) | https://en.wikipedia.org/wiki/Binary_search |
| wiki-ctl | Wikipedia, "Computation tree logic" (article source) | https://en.wikipedia.org/wiki/Computation_tree_logic |
| wiki-ltl | Wikipedia, "Linear temporal logic" (article source) | https://en.wikipedia.org/wiki/Linear_temporal_logic |
| sqlite-fileformat | SQLite, "Database File Format" | https://www.sqlite.org/fileformat.html |
| sqlite-pragma | SQLite, "Pragma statements supported by SQLite" (page_size) | https://www.sqlite.org/pragma.html |
| sqlite-eqp | SQLite, "EXPLAIN QUERY PLAN" | https://www.sqlite.org/eqp.html |
| wiki-linear-hashing | Wikipedia, "Linear hashing" (article source) | https://en.wikipedia.org/wiki/Linear_hashing |
| wiki-extendible-hashing | Wikipedia, "Extendible hashing" (article source) | https://en.wikipedia.org/wiki/Extendible_hashing |
| wiki-bplus-tree | Wikipedia, "B+ tree" (article source) | https://en.wikipedia.org/wiki/B%2B_tree |
| sqlite-analyze | SQLite, "ANALYZE" | https://www.sqlite.org/lang_analyze.html |
| sqlite-locking | SQLite, "File Locking And Concurrency In SQLite Version 3" | https://www.sqlite.org/lockingv3.html |
| sqlite-wal | SQLite, "Write-Ahead Logging" | https://www.sqlite.org/wal.html |
| sqlite-isolation | SQLite, "Isolation In SQLite" | https://www.sqlite.org/isolation.html |
| sqlite-transaction | SQLite, "Transaction" | https://www.sqlite.org/lang_transaction.html |
| sqlite-trigger | SQLite, "CREATE TRIGGER" | https://www.sqlite.org/lang_createtrigger.html |
| wiki-snapshot-isolation | Wikipedia, "Snapshot isolation" (article source) | https://en.wikipedia.org/wiki/Snapshot_isolation |
| wiki-2pl | Wikipedia, "Two-phase locking" (article source) | https://en.wikipedia.org/wiki/Two-phase_locking |
| wiki-aries | Wikipedia, "Algorithms for Recovery and Isolation Exploiting Semantics" (article source) | https://en.wikipedia.org/wiki/Algorithms_for_Recovery_and_Isolation_Exploiting_Semantics |
| wiki-isolation | Wikipedia, "Isolation (database systems)" (article source) | https://en.wikipedia.org/wiki/Isolation_(database_systems) |
| wiki-cray-1 | Wikipedia, "Cray-1" (article source) | https://en.wikipedia.org/wiki/Cray-1 |
| wiki-vector-clock | Wikipedia, "Vector clock" (article source) | https://en.wikipedia.org/wiki/Vector_clock |
| wiki-two-generals | Wikipedia, "Two Generals' Problem" (article source) | https://en.wikipedia.org/wiki/Two_Generals%27_Problem |
| wiki-rpc | Wikipedia, "Remote procedure call" (article source) | https://en.wikipedia.org/wiki/Remote_procedure_call |
| wiki-chandy-lamport | Wikipedia, "Chandy--Lamport algorithm" (article source) | https://en.wikipedia.org/wiki/Chandy%E2%80%93Lamport_algorithm |
| raft-site | The Raft Consensus Algorithm, project page (raft.github.io) | https://raft.github.io/ |
| wiki-raft | Wikipedia, "Raft (algorithm)" (article source) | https://en.wikipedia.org/wiki/Raft_(algorithm) |
| wiki-cap | Wikipedia, "CAP theorem" (article source) | https://en.wikipedia.org/wiki/CAP_theorem |
| wiki-2pc | Wikipedia, "Two-phase commit protocol" (article source) | https://en.wikipedia.org/wiki/Two-phase_commit_protocol |
| wiki-pacelc | Wikipedia, "PACELC design principle" (article source) | https://en.wikipedia.org/wiki/PACELC_design_principle |
| fips197 | NIST FIPS 197-upd1, Advanced Encryption Standard (AES), 2023 update (PDF) | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf |
| fips180-4 | NIST FIPS 180-4, Secure Hash Standard (PDF) | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf |
| sp800-38a | NIST SP 800-38A, Recommendation for Block Cipher Modes of Operation (PDF) | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf |
| rfc8439 | RFC 8439, ChaCha20 and Poly1305 for IETF Protocols | https://www.rfc-editor.org/rfc/rfc8439.txt |
| rfc2104 | RFC 2104, HMAC: Keyed-Hashing for Message Authentication | https://www.rfc-editor.org/rfc/rfc2104.txt |
| py-hashlib | Python documentation, hashlib | https://docs.python.org/3/library/hashlib.html |
| py-hmac | Python documentation, hmac | https://docs.python.org/3/library/hmac.html |
| py-secrets | Python documentation, secrets | https://docs.python.org/3/library/secrets.html |
| wiki-kerckhoffs | Wikipedia, "Kerckhoffs's principle" (article source) | https://en.wikipedia.org/wiki/Kerckhoffs%27s_principle |
| wiki-enigma | Wikipedia, "Enigma machine" (article source) | https://en.wikipedia.org/wiki/Enigma_machine |
| commons-enigma | Wikimedia Commons, File:Enigma (crittografia) - Museo scienza e tecnologia Milano.jpg, file page and metadata | https://commons.wikimedia.org/wiki/File:Enigma_(crittografia)_-_Museo_scienza_e_tecnologia_Milano.jpg |
| wiki-ae | Wikipedia, "Authenticated encryption" (article source) | https://en.wikipedia.org/wiki/Authenticated_encryption |
| wiki-padding-oracle | Wikipedia, "Padding oracle attack" (article source) | https://en.wikipedia.org/wiki/Padding_oracle_attack |
| wiki-padding | Wikipedia, "Padding (cryptography)" (article source) | https://en.wikipedia.org/wiki/Padding_(cryptography) |
| wiki-sha2 | Wikipedia, "SHA-2" (article source) | https://en.wikipedia.org/wiki/SHA-2 |
| rfc8446 | RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3 | https://www.rfc-editor.org/rfc/rfc8446.txt |
| rfc5869 | RFC 5869, HMAC-based Extract-and-Expand Key Derivation Function (HKDF) | https://www.rfc-editor.org/rfc/rfc5869.txt |
| rfc7748 | RFC 7748, Elliptic Curves for Security | https://www.rfc-editor.org/rfc/rfc7748.txt |
| rfc7914 | RFC 7914, The scrypt Password-Based Key Derivation Function | https://www.rfc-editor.org/rfc/rfc7914.txt |
| rfc8018 | RFC 8018, PKCS #5: Password-Based Cryptography Specification Version 2.1 | https://www.rfc-editor.org/rfc/rfc8018.txt |
| sp800-57 | NIST SP 800-57 Part 1 Rev. 5, Recommendation for Key Management, May 2020 (PDF) | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf |
| sp800-63b-4 | NIST SP 800-63B-4, Digital Identity Guidelines: Authentication and Authenticator Management (HTML) | https://pages.nist.gov/800-63-4/sp800-63b.html |
| wiki-bsgs | Wikipedia, "Baby-step giant-step" (article source) | https://en.wikipedia.org/wiki/Baby-step_giant-step |
| wiki-rsa | Wikipedia, "RSA cryptosystem" (article source) | https://en.wikipedia.org/wiki/RSA_cryptosystem |
| wiki-hasse | Wikipedia, "Hasse's theorem on elliptic curves" (article source) | https://en.wikipedia.org/wiki/Hasse%27s_theorem_on_elliptic_curves |
| wiki-schnorr | Wikipedia, "Schnorr signature" (article source) | https://en.wikipedia.org/wiki/Schnorr_signature |
| wiki-pss | Wikipedia, "Probabilistic signature scheme" (article source) | https://en.wikipedia.org/wiki/Probabilistic_signature_scheme |
| wiki-fdh | Wikipedia, "Full Domain Hash" (article source) | https://en.wikipedia.org/wiki/Full_Domain_Hash |
| wiki-stack-overflow | Wikipedia, "Stack buffer overflow" (article source) | https://en.wikipedia.org/wiki/Stack_buffer_overflow |
| wiki-morris | Wikipedia, "Morris worm" (article source) | https://en.wikipedia.org/wiki/Morris_worm |
| wiki-bop | Wikipedia, "Buffer overflow protection" (article source) | https://en.wikipedia.org/wiki/Buffer_overflow_protection |
| wiki-aslr | Wikipedia, "Address space layout randomization" (article source) | https://en.wikipedia.org/wiki/Address_space_layout_randomization |
| wiki-stride | Wikipedia, "STRIDE model" (article source) | https://en.wikipedia.org/wiki/STRIDE_model |
| wiki-owasp | Wikipedia, "OWASP" (article source) | https://en.wikipedia.org/wiki/OWASP |
| wiki-least-privilege | Wikipedia, "Principle of least privilege" (article source) | https://en.wikipedia.org/wiki/Principle_of_least_privilege |
| wiki-confused-deputy | Wikipedia, "Confused deputy problem" (article source) | https://en.wikipedia.org/wiki/Confused_deputy_problem |
| wiki-csp | Wikipedia, "Content Security Policy" (article source) | https://en.wikipedia.org/wiki/Content_Security_Policy |
| gcc-instrumentation | GCC manual, Program Instrumentation Options | https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html |
| asan-docs | Clang documentation, AddressSanitizer | https://clang.llvm.org/docs/AddressSanitizer.html |
| py-sqlite3 | Python documentation, sqlite3 | https://docs.python.org/3/library/sqlite3.html |
| py-subprocess | Python documentation, subprocess | https://docs.python.org/3/library/subprocess.html |
| py-html | Python documentation, html | https://docs.python.org/3/library/html.html |
| mdn-set-cookie | MDN Web Docs, Set-Cookie header | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie |
| wiki-design-patterns | Wikipedia, "Design Patterns" (article source) | https://en.wikipedia.org/wiki/Design_Patterns |
| wiki-solid | Wikipedia, "SOLID" (article source) | https://en.wikipedia.org/wiki/SOLID |
| wiki-refactoring | Wikipedia, "Code refactoring" (article source) | https://en.wikipedia.org/wiki/Code_refactoring |
| wiki-mutation-testing | Wikipedia, "Mutation testing" (article source) | https://en.wikipedia.org/wiki/Mutation_testing |
| wiki-mvc | Wikipedia, "Model-view-controller" (article source) | https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller |
| wiki-metamorphic | Wikipedia, "Metamorphic testing" (article source) | https://en.wikipedia.org/wiki/Metamorphic_testing |
| wiki-characterization-test | Wikipedia, "Characterization test" (article source) | https://en.wikipedia.org/wiki/Characterization_test |
| wiki-technical-debt | Wikipedia, "Technical debt" (article source) | https://en.wikipedia.org/wiki/Technical_debt |
| wiki-ci | Wikipedia, "Continuous integration" (article source) | https://en.wikipedia.org/wiki/Continuous_integration |
| wiki-quickcheck | Wikipedia, "QuickCheck" (article source) | https://en.wikipedia.org/wiki/QuickCheck |
| wiki-information-hiding | Wikipedia, "Information hiding" (article source) | https://en.wikipedia.org/wiki/Information_hiding |
| wiki-test-double | Wikipedia, "Test double" (article source) | https://en.wikipedia.org/wiki/Test_double |
| wiki-uml | Wikipedia, "Unified Modeling Language" (article source) | https://en.wikipedia.org/wiki/Unified_Modeling_Language |
| py-sys-monitoring | Python documentation, sys.monitoring | https://docs.python.org/3/library/sys.monitoring.html |
| hypothesis-api | Hypothesis documentation, API reference (settings) | https://hypothesis.readthedocs.io/en/latest/reference/api.html |
| git-githooks | Git documentation, githooks | https://git-scm.com/docs/githooks |
| wiki-sketchpad | Wikipedia, "Sketchpad" (article source) | https://en.wikipedia.org/wiki/Sketchpad |
| wiki-zbuffer | Wikipedia, "Z-buffering" (article source) | https://en.wikipedia.org/wiki/Z-buffering |
| wiki-pick | Wikipedia, "Pick's theorem" (article source) | https://en.wikipedia.org/wiki/Pick%27s_theorem |
| wiki-gouraud | Wikipedia, "Gouraud shading" (article source) | https://en.wikipedia.org/wiki/Gouraud_shading |
| wiki-phong | Wikipedia, "Phong reflection model" (article source) | https://en.wikipedia.org/wiki/Phong_reflection_model |
| wiki-ray-tracing | Wikipedia, "Ray tracing (graphics)" (article source) | https://en.wikipedia.org/wiki/Ray_tracing_(graphics) |
| netpbm-ppm | Netpbm documentation, PPM format specification | https://netpbm.sourceforge.net/doc/ppm.html |
| w3c-png3 | W3C, Portable Network Graphics (PNG) Specification (Third Edition) | https://www.w3.org/TR/png-3/ |
| raft-paper | D. Ongaro and J. Ousterhout, In Search of an Understandable Consensus Algorithm (Extended Version), raft.github.io | https://raft.github.io/raft.pdf |
| rust-file | Rust standard library documentation, std::fs::File (sync_all) | https://doc.rust-lang.org/std/fs/struct.File.html |
| wiki-amdahl | Wikipedia, "Amdahl's law" (article source) | https://en.wikipedia.org/wiki/Amdahl%27s_law |
| wiki-gustafson | Wikipedia, "Gustafson's law" (article source) | https://en.wikipedia.org/wiki/Gustafson%27s_law |
| wiki-prefix-sum | Wikipedia, "Prefix sum" (article source) | https://en.wikipedia.org/wiki/Prefix_sum |
| wiki-parallel-analysis | Wikipedia, "Analysis of parallel algorithms" (article source) | https://en.wikipedia.org/wiki/Analysis_of_parallel_algorithms |
| crossref | Crossref REST API, the DOI registration record of a paper | https://api.crossref.org/works/<doi> |
| ibm-fortran | IBM, *Fortran* (IBM history pages) | https://www.ibm.com/history/fortran |
| lex-paper | M. E. Lesk and E. Schmidt, *Lex -- A Lexical Analyzer Generator* Bell Laboratories (text of the paper; the copies read are undated) | https://cs.utexas.edu/~novak/lexpaper.htm |
| reps-tr | T. Reps, *Maximal-Munch Tokenization in Linear Time*, abstract page and TR 1347 record, University of Wisconsin | https://research.cs.wisc.edu/wpis/abstracts/toplas98b.abs.html |
| kl-core | Commons description page of File:KL_CoreMemory.jpg (Konstantin Lanzet) | https://commons.wikimedia.org/wiki/File:KL_CoreMemory.jpg |
| nasa-704 | NASA photograph GPN-2000-001881 (L-1957-00989), Commons description page | https://commons.wikimedia.org/wiki/File:IBM_Electronic_Data_Processing_Machine_-_GPN-2000-001881.jpg |

## Rows

| id | quantity | value | unit | source | accessed |
|---|---|---|---|---|---|
| b3:fortran-1957 | first Fortran compiler, for the IBM 704 | 1957 | year | ibm-fortran | 2026-11-20 |
| b3:thompson-1968 | K. Thompson, Regular expression search algorithm, CACM 11(6) 419--422 | June 1968 | date | crossref | 2026-11-20 |
| b3:lex-rules | lex (Lesk and Schmidt, Bell Laboratories): how a match is chosen | longest match, then the rule given first | rule | lex-paper | 2026-11-20 |
| b3:reps-1998 | T. Reps, Maximal-munch tokenization in linear time, TOPLAS 20(2) 259--273 | March 1998 | date | crossref | 2026-11-20 |
| b3:nasa-704-photo | IBM 704 at NACA Langley, photograph date | 1957-03-21 | date | nasa-704 | 2026-11-20 |
| b3:pratt-1973 | V. R. Pratt, Top down operator precedence, POPL '73, 41--51 | 1973 | year | crossref | 2026-11-20 |
| b3:lewis-stearns-1968 | P. M. Lewis and R. E. Stearns, Syntax-directed transduction, JACM 15(3) 465--488 (LL(k) grammars) | July 1968 | date | crossref | 2026-11-20 |
| b3:knuth-1965 | D. E. Knuth, On the translation of languages from left to right, Information and Control 8(6) 607--639 (LR(k)) | December 1965 | date | crossref | 2026-11-20 |
| b3:deremer-1971 | F. L. DeRemer, Simple LR(k) grammars, CACM 14(7) 453--460 | July 1971 | date | crossref | 2026-11-20 |
| b3:algol60-1960 | J. W. Backus et al., Report on the algorithmic language ALGOL 60, CACM 3(5) 299--311 | May 1960 | date | crossref | 2026-11-20 |
| b3:church-1932 | A. Church, A set of postulates for the foundation of logic, Annals of Mathematics 33(2) 346--366 (the λ-notation) | April 1932 | date | crossref | 2026-11-20 |
| b3:church-rosser-1936 | A. Church and J. B. Rosser, Some properties of conversion, Trans. AMS 39(3) 472--482 | 1936 | year | crossref | 2026-11-20 |
| b3:newman-1942 | M. H. A. Newman, On theories with a combinatorial definition of "equivalence", Annals of Mathematics 43(2) 223--243 | April 1942 | date | crossref | 2026-11-20 |
| b3:debruijn-1972 | N. G. de Bruijn, Lambda calculus notation with nameless dummies, Indagationes Mathematicae 75(5) 381--392 | 1972 | year | crossref | 2026-11-20 |
| b3:kahn-1987 | G. Kahn, Natural semantics, STACS 87, LNCS 247, 22--39 | 1987 | year | crossref | 2026-11-20 |
| b3:hindley-1969 | J. R. Hindley, The principal type-scheme of an object in combinatory logic, Trans. AMS 146, from p. 29 | December 1969 | date | crossref | 2026-11-20 |
| b3:milner-1978 | R. Milner, A theory of type polymorphism in programming, JCSS 17(3) 348--375 | December 1978 | date | crossref | 2026-11-20 |
| b3:damas-milner-1982 | L. Damas and R. Milner, Principal type-schemes for functional programs, POPL '82, 207--212 | 1982 | year | crossref | 2026-11-20 |
| b3:wright-felleisen-1994 | A. K. Wright and M. Felleisen, A syntactic approach to type soundness, Information and Computation 115(1) 38--94 | November 1994 | date | crossref | 2026-11-20 |
| b3:mairson-1990 | H. G. Mairson, Deciding ML typability is complete for deterministic exponential time, POPL '90, 382--401 | 1990 | year | crossref | 2026-11-20 |
| b3:rv-preserved | registers preserved across calls (integer register convention) | sp and s0--s11 (callee-saved) yes; ra, t0--t6, a0--a7 no | --- | RISCV-PSABI | 2026-11-20 |
| b3:rv-args | argument and return registers | eight argument registers a0--a7, the first two also used to return values; a scalar of at most XLEN bits in one register, or on the stack if none is left | --- | RISCV-PSABI | 2026-11-20 |
| b3:sethi-ullman-1970 | R. Sethi and J. D. Ullman, The generation of optimal code for arithmetic expressions, JACM 17(4) 715--728 | October 1970 | date | crossref | 2026-11-20 |
| b3:aho-ganapathi-tjiang-1989 | A. V. Aho, M. Ganapathi and S. W. K. Tjiang, Code generation using tree matching and dynamic programming, TOPLAS 11(4) 491--516 | October 1989 | date | crossref | 2026-11-20 |
| b3:leroy-2009 | X. Leroy, Formal verification of a realistic compiler, CACM 52(7) 107--115 | July 2009 | date | crossref | 2026-11-20 |
| b3:kildall-1973 | G. A. Kildall, A unified approach to global program optimization, POPL '73, 194--206 | 1973 | year | crossref | 2026-11-20 |
| b3:kam-ullman-1977 | J. B. Kam and J. D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3) 305--317 | 1977 | year | crossref | 2026-11-20 |
| b3:cytron-1991 | R. Cytron, J. Ferrante, B. K. Rosen, M. N. Wegman and F. K. Zadeck, Efficiently computing static single assignment form and the control dependence graph, TOPLAS 13(4) 451--490 | October 1991 | date | crossref | 2026-11-20 |
| b3:chaitin-1982 | G. J. Chaitin, Register allocation and spilling via graph coloring, SIGPLAN '82 Symposium on Compiler Construction, 98--101 | 1982 | year | crossref | 2026-11-20 |
| b3:mccarthy-1960 | J. McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, CACM 3(4) 184--195 | April 1960 | date | crossref | 2026-11-20 |
| b3:collins-1960 | G. E. Collins, A method for overlapping and erasure of lists, CACM 3(12) 655--657 | December 1960 | date | crossref | 2026-11-20 |
| b3:cheney-1970 | C. J. Cheney, A nonrecursive list compacting algorithm, CACM 13(11) 677--678 | November 1970 | date | crossref | 2026-11-20 |
| b3:dijkstra-onthefly-1978 | E. W. Dijkstra, L. Lamport, A. J. Martin, C. S. Scholten and E. F. M. Steffens, On-the-fly garbage collection, CACM 21(11) 966--975 | November 1978 | date | crossref | 2026-11-20 |
| b3:lieberman-hewitt-1983 | H. Lieberman and C. Hewitt, A real-time garbage collector based on the lifetimes of objects, CACM 26(6) 419--429 | June 1983 | date | crossref | 2026-11-20 |
| b3:ungar-1984 | D. Ungar, Generation scavenging, ACM SIGSOFT/SIGPLAN symposium on practical software development environments, 157--167 | 1984 | year | crossref | 2026-11-20 |
| b3:py-getrefcount-plus-one | sys.getrefcount counts the temporary reference held by its own argument, so it is generally one higher than expected; immortal objects have very large counts (3.12) | one higher | rule | py-sys | 2026-11-20 |
| b3:py-gc-collect-returns | gc.collect() with no arguments runs a full collection and returns the number of unreachable objects found | number found | rule | py-gc | 2026-11-20 |
| b3:rust-rc-cycle | A cycle between Rc pointers will never be deallocated; Weak is used to break cycles (a tree: strong Rc from parent to children, Weak from children back to parents); Weak::upgrade returns None once the value is dropped | never | rule | rust-rc | 2026-11-20 |
| b3:core-plane-bits | Core memory plane in the photograph: 32 x 32 cores storing 1024 bits (128 bytes) | 1024 | bits | kl-core | 2026-11-20 |
| b3:ucontext-obsolescent | getcontext, makecontext and swapcontext are marked obsolescent (OB XSI) in Issue 6; application usage: they can be replaced using POSIX threads | obsolescent | status | posix-mkctx-6 | 2026-11-20 |
| b3:ucontext-removed | getcontext, makecontext and swapcontext are listed among the system interfaces removed in Issue 7 (POSIX.1-2017 rationale B.3.1), with the advice to rewrite applications to use POSIX threads | removed | status | posix-xrat-7 | 2026-11-20 |
| b3:corbato-1962 | F. J. Corbato, M. Merwin-Daggett and R. C. Daley, An experimental time-sharing system, AIEE-IRE spring joint computer conference, May 1962, 335ff | May 1962 | date | crossref | 2026-11-20 |
| b3:liu-layland-1973 | C. L. Liu and J. W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, JACM 20(1) 46--61 | January 1973 | date | crossref | 2026-11-20 |
| b3:waldspurger-weihl-1994 | C. A. Waldspurger and W. E. Weihl (MIT Laboratory for Computer Science), Lottery scheduling: flexible proportional-share resource management, OSDI '94 | 1994 | year | usenix-lottery | 2026-11-20 |
| b3:rv-mepc | When a trap is taken into M-mode, mepc is written with the address of the instruction that was interrupted or that encountered the exception; MRET reads mepc implicitly | mepc | rule | RISCV-PRIV | 2026-11-20 |
| b3:rv-mcause | When a trap is taken into M-mode, mcause is written with a code indicating the event; its Interrupt bit is set if the trap was caused by an interrupt | mcause | rule | RISCV-PRIV | 2026-11-20 |
| b3:rv-mtvec | mtvec holds the trap vector configuration: a vector base address and a vector mode | mtvec | rule | RISCV-PRIV | 2026-11-20 |
| b3:rv-mtimecmp | A machine timer interrupt becomes pending whenever mtime is greater than or equal to mtimecmp (unsigned); it stays posted until mtimecmp exceeds mtime, typically by writing mtimecmp | mtime >= mtimecmp | rule | RISCV-PRIV | 2026-11-20 |
| b3:sv32-va | Sv32 virtual address: VPN[1] in bits 31--22 (10 bits), VPN[0] in bits 21--12 (10 bits), page offset in bits 11--0 (12 bits); 4 KiB pages | 10 + 10 + 12 | bits | RISCV-PRIV-S | 2026-11-20 |
| b3:sv32-pte | Sv32 page-table entry of four bytes: PPN[1] bits 31--20, PPN[0] bits 19--10, RSW bits 9--8, then D, A, G, U, X, W, R, V in bits 7 to 0 | 4 bytes | layout | RISCV-PRIV-S | 2026-11-20 |
| b3:sv32-ppn | Sv32 translates the 20-bit VPN into a 22-bit physical page number; the 12-bit offset is untranslated (34-bit physical addresses in the spec's example) | 22 bits | bits | RISCV-PRIV-S | 2026-11-20 |
| b3:sv32-table | Sv32 page tables have 2^10 PTEs of four bytes; a page table is exactly the size of a page, page-aligned; the root's physical page number is in satp | 1024 x 4 B | size | RISCV-PRIV-S | 2026-11-20 |
| b3:sv32-rwx | V = 0: invalid; R = W = X = 0: a pointer to the next level, otherwise a leaf; writable pages must be readable (W without R reserved); translation steps: a = satp.ppn x PAGESIZE, PTE at a + vpn[i] x PTESIZE, i from LEVELS - 1 | rule | rule | RISCV-PRIV-S | 2026-11-20 |
| b3:sv32-megapage | Any level of PTE may be a leaf, so Sv32 also supports 4 MiB megapages, aligned to 4 MiB | 4 MiB | size | RISCV-PRIV-S | 2026-11-20 |
| b3:sv32-ad | Each leaf PTE has an accessed bit A (read, written or fetched since A was last cleared) and a dirty bit D (written since D was last cleared); either hardware sets them or, with Svade, a page fault lets software do it | A, D | rule | RISCV-PRIV-S | 2026-11-20 |
| b3:rv-asid | satp holds the root table's physical page number and an address-space identifier (ASID); ASIDMAX is 9 bits for Sv32 and 16 for Sv39 | 9 / 16 bits | bits | RISCV-PRIV-S | 2026-11-20 |
| b3:rv-sfence | SFENCE.VMA orders updates of the page tables and invalidates cached address-translation entries, for all addresses or one, for all ASIDs or one | SFENCE.VMA | rule | RISCV-PRIV-S | 2026-11-20 |
| b3:sv39 | Sv39: 39-bit virtual addresses in 4 KiB pages; a 27-bit VPN translated through a three-level table into a 44-bit PPN; tables of 2^9 PTEs of eight bytes; 2 MiB megapages and 1 GiB gigapages | 9 + 9 + 9 + 12 | bits | RISCV-PRIV-S | 2026-11-20 |
| b3:belady-1966 | L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) 78--101 | 1966 | year | crossref | 2026-11-20 |
| b3:belady-nelson-shedler-1969 | L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, CACM 12(6) 349--353 | June 1969 | date | crossref | 2026-11-20 |
| b3:denning-1968 | P. J. Denning, The working set model for program behavior, CACM 11(5) 323--333 | May 1968 | date | crossref | 2026-11-20 |
| b3:mattson-1970 | R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) 78--117 | 1970 | year | crossref | 2026-11-20 |
| b3:linux-minflt | Linux getrusage: ru_minflt counts the page faults serviced without any I/O activity, ru_majflt those that required I/O | ru_minflt | rule | man-getrusage | 2026-11-20 |
| b3:linux-map-shared | mmap MAP_SHARED: updates to the mapping are visible to other processes mapping the same region and, for a file mapping, are carried through to the underlying file; msync controls when | MAP_SHARED | rule | man-mmap | 2026-11-20 |
| b3:linux-fork-cow | Under Linux, fork() is implemented using copy-on-write pages: its cost is duplicating the parent's page tables and creating a task structure | copy on write | rule | man-fork | 2026-11-20 |
| b3:rv-stval | When a trap is taken into S-mode, stval is written with exception-specific information; for a page-fault exception a nonzero stval holds the faulting virtual address | stval | rule | RISCV-PRIV-S | 2026-11-20 |
| b3:sv48-sv57 | Sv48 translates through a four-level page table, Sv57 through a five-level page table | 4 / 5 levels | count | RISCV-PRIV-S | 2026-11-20 |
| b3:ext2-pointers | An ext2 inode holds pointers to the first 12 data blocks, one pointer to an indirect block, one to a doubly-indirect block and one to a trebly-indirect block | 12 / 1 / 1 / 1 | layout | kernel-ext2 | 2026-11-20 |
| b3:ext2-blocksize | ext2 blocks are of a fixed size of 1024, 2048 or 4096 bytes (8192 on Alpha systems) | 1, 2, 4 KiB | size | kernel-ext2 | 2026-11-20 |
| b3:ext2-file-limit | ext2 file size limit by block size: 16 GB with 1 kB blocks, 256 GB with 2 kB, 2048 GB with 4 kB and with 8 kB | 16 / 256 / 2048 GB | size | kernel-ext2 | 2026-11-20 |
| b3:rosenblum-ousterhout-1992 | M. Rosenblum and J. K. Ousterhout, The design and implementation of a log-structured file system, ACM TOCS 10(1) 26--52 | February 1992 | date | crossref | 2026-11-20 |
| b3:patterson-gibson-katz-1988 | D. A. Patterson, G. Gibson and R. H. Katz, A case for redundant arrays of inexpensive disks (RAID), SIGMOD '88, 109--116 | 1988 | year | crossref | 2026-11-20 |
| b3:hd-photo | The photograph shows a 500 GB 2.5-inch Western Digital Scorpio Blue SATA hard disk, opened; taken 29 August 2013 | 2.5 inch | photo | hd-photo | 2026-11-20 |
| b3:coffman-1971 | E. G. Coffman, M. Elphick and A. Shoshani, System deadlocks, ACM Computing Surveys 3(2) 67--78 | June 1971 | date | crossref | 2026-11-20 |
| b3:ewd123-banker | Dijkstra's notes Cooperating sequential processes (EWD 123) have a section 6, The Problem of the Deadly Embrace, whose 6.1 is The Banker's Algorithm | section 6.1 | rule | ewd123 | 2026-11-20 |
| b3:ewd310-philosophers | EWD 310 poses the problem of the Five Dining Philosophers (thinking and eating, two forks per plate, neighbours cannot eat together); the naive solution, a binary semaphore per fork, is rejected for the deadly embrace when all five take their left fork | five philosophers | rule | ewd310 | 2026-11-20 |
| b3:dijkstra-1971 | E. W. Dijkstra, Hierarchical ordering of sequential processes, Acta Informatica 1(2) 115--138 | 1971 | year | crossref | 2026-11-20 |
| b3:hoare-1974 | C. A. R. Hoare, Monitors, CACM 17(10) 549--557 | October 1974 | date | crossref | 2026-11-20 |
| b3:lampson-redell-1980 | B. W. Lampson and D. D. Redell, Experience with processes and monitors in Mesa, CACM 23(2) 105--117 | February 1980 | date | crossref | 2026-11-20 |
| b3:lamport-1979 | L. Lamport, How to make a multiprocessor computer that correctly executes multiprocess programs, IEEE Transactions on Computers C-28(9) 690--691 | September 1979 | date | crossref | 2026-11-20 |
| b3:sewell-2010 | P. Sewell, S. Sarkar, S. Owens, F. Zappa Nardelli and M. O. Myreen, x86-TSO, CACM 53(7) 89--97 | July 2010 | date | crossref | 2026-11-20 |
| b3:herlihy-wing-1990 | M. P. Herlihy and J. M. Wing, Linearizability: a correctness condition for concurrent objects, TOPLAS 12(3) 463--492 | July 1990 | date | crossref | 2026-11-20 |
| b3:michael-scott-1996 | M. M. Michael and M. L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC '96, 267--275 | 1996 | year | crossref | 2026-11-20 |
| b3:treiber-1986 | R. K. Treiber, Systems programming: coping with parallelism, RJ 5118, IBM Almaden Research Center (reference 21 of Michael and Scott, who use Treiber's non-blocking stack as their free list) | April 1986 | date | ms96 | 2026-11-20 |
| b3:ms-aba | The ABA problem: a compare-and-swap may succeed when it should not if, between the read and the CAS, others change A to B and back to A; the common solution is a modification counter with the pointer, incremented on each successful CAS, which makes ABA extremely unlikely, not impossible | modification counter | rule | ms96 | 2026-11-20 |
| b3:ms-queue | The Michael--Scott queue is a singly linked list with Head and Tail pointers; Head always points to a dummy node, the first in the list; Tail points to the last or second-to-last node; it uses compare-and-swap with modification counters | dummy node | rule | ms96 | 2026-11-20 |
| b3:c11-seqcst-default | The default behaviour of all C atomic operations is sequentially consistent ordering; a memory_order argument can weaken it (relaxed, consume, acquire, release, acq_rel, seq_cst) | memory_order_seq_cst | rule | cppref-mo | 2026-11-20 |
| b3:x86-release-acquire | On strongly ordered systems such as x86, release-acquire ordering is automatic for most operations: no additional CPU instructions are issued, only compiler optimisations are restricted | x86 | rule | cppref-mo | 2026-11-20 |
| b3:posix-spurious | Spurious wakeups from pthread_cond_wait may occur; since the return implies nothing about the predicate, the predicate should be re-evaluated | spurious wakeup | rule | posix-cond-wait | 2026-11-20 |
| b3:lamport-sc | Lamport calls a multiprocessor sequentially consistent if the result of any execution is the same as if the operations of all the processors were executed in some sequential order, and the operations of each processor appear in this sequence in the order specified by its program | sequentially consistent | rule | lamport-multi | 2026-11-20 |
| b3:coffman-conditions | The four conditions are known as the Coffman conditions from their first description in the 1971 article by Coffman, Elphick and Shoshani (System Deadlocks, ACM Computing Surveys 3(2)) | Coffman conditions | rule | wp-deadlock | 2026-11-20 |
| b3:ms-helping | In the Michael--Scott enqueue, a thread that finds Tail not pointing to the last node tries to swing Tail to the next node (CAS), then retries; after linking its node it tries to swing Tail to it | swing Tail | rule | ms96 | 2026-11-20 |
| b3:tso-sb | On x86 the store-buffering test's final state with both reads 0 is allowed; microarchitecturally it is a visible consequence of store buffering: if each processor has a FIFO buffer of pending writes, the reads can occur before the writes have propagated from the buffers to main memory | allowed | rule | tso-cacm | 2026-11-20 |
| b3:popek-goldberg-1974 | G. J. Popek and R. P. Goldberg, Formal requirements for virtualizable third generation architectures, CACM 17(7) 412--421 | July 1974 | date | crossref | 2026-11-20 |
| b3:robin-irvine-2000 | J. S. Robin and C. E. Irvine, Analysis of the Intel Pentium's ability to support a secure virtual machine monitor, 9th USENIX Security Symposium, Denver, 14--17 August 2000 | August 2000 | date | robin-irvine | 2026-11-20 |
| b3:sensitive-def | Sensitive instructions are those that would interfere with the state of the VMM or host OS if executed directly in a VM; privileged instructions cause a trap (general protection exception) outside the most privileged domain; if all sensitive instructions are privileged, the processor is considered virtualizable, and all of them trap to the VMM, which emulates them | rule | rule | robin-irvine | 2026-11-20 |
| b3:vmm-types | A Type I VMM runs on a bare machine, an operating system with virtualization mechanisms; a Type II VMM runs as an application on a host OS; a system run in the virtual environment is a guest OS | Type I, Type II | rule | robin-irvine | 2026-11-20 |
| b3:goldberg-vm | Goldberg's definition (thesis, Harvard, 1972): a VM is a hardware-software duplicate of a real existing computer system in which a statistically dominant subset of the virtual processor's instructions execute on the host processor in native mode; a complete software interpreter emulating every instruction does not meet it | statistically dominant subset | rule | robin-irvine | 2026-11-20 |
| b3:pentium-17 | Examining every member of the Pentium instruction set, seventeen instructions violate the requirement (sensitive and unprivileged), making the processor non-virtualizable; among them SGDT, SIDT, SLDT and SMSW | 17 | count | robin-irvine | 2026-11-20 |
| b3:csr-privilege | csr[9:8] encode the lowest privilege level that can access a CSR (10 = hypervisor); csr[11:10] = 11 means read-only; access without sufficient privilege raises an illegal-instruction (or virtual-instruction) exception | csr[9:8] | rule | riscv-csrs | 2026-11-20 |
| b3:csr-custom | CSR addresses 0x5C0--0x5FF are custom read/write supervisor-level CSRs, not redefined by future standard extensions | 0x5C0--0x5FF | rule | riscv-csrs | 2026-11-20 |
| b3:rv-hypervisor | The RISC-V hypervisor extension virtualizes the supervisor-level architecture to host guest operating systems atop a type-1 or type-2 hypervisor, and adds a second stage of translation from guest physical to supervisor physical addresses | hypervisor extension | rule | riscv-hyp | 2026-11-20 |
| b3:rv-two-stage | With V = 1, two-stage translation: VS-stage (vsatp) to a guest physical address, then G-stage (hgatp) to a supervisor physical address; accesses made for VS-stage translation, such as reads and writes of VS-level page tables, are themselves subject to G-stage translation | VS-stage, G-stage | rule | riscv-hyp | 2026-11-20 |
| b3:namespace-def | A namespace wraps a global system resource in an abstraction that makes processes inside it appear to have their own isolated instance; one use of namespaces is to implement containers | namespace | rule | man-namespaces | 2026-11-20 |
| b3:namespace-types | Linux namespace types and what they isolate: Cgroup (cgroup root directory), IPC (System V IPC, POSIX message queues), Network (network devices, stacks, ports), Mount (mount points), PID (process IDs), Time (boot and monotonic clocks), User (user and group IDs), UTS (hostname and NIS domain name) | 8 types | count | man-namespaces | 2026-11-20 |
| b3:cgroup-def | cgroup is a mechanism to organize processes hierarchically and distribute system resources along the hierarchy; memory.max is the memory usage hard limit, and when usage reaches it and cannot be reduced the OOM killer is invoked in the cgroup | memory.max | rule | kernel-cgroup2 | 2026-11-20 |
| b3:rlimit-as | RLIMIT_AS is the maximum size of total available memory of the process, in bytes; beyond it malloc() and mmap() fail with ENOMEM | RLIMIT_AS | rule | posix-getrlimit | 2026-11-20 |
| b3:chroot-not-security | chroot changes an ingredient in pathname resolution and does nothing else; it is not intended for any kind of security purpose, neither to fully sandbox a process nor to restrict filesystem system calls; it needs CAP_SYS_CHROOT on Linux | chroot | rule | man-chroot | 2026-11-20 |
| b3:turing-1936 | A. M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proc. London Math. Soc. s2-42(1) 230--265; cited as Turing 1936--7 | 1936--37 | date | crossref | 2026-11-20 |
| b3:turing-universal | Turing constructed the universal Turing machine in that paper (sec. 6) and used it to prove that there are problems no Turing machine computes; the halting problem was originally formulated by Turing | 1936--37 | rule | sep-recursive-functions | 2026-11-20 |
| b3:church-1936 | A. Church, An unsolvable problem of elementary number theory, American Journal of Mathematics 58(2) 345 | April 1936 | date | crossref | 2026-11-20 |
| b3:ct-thesis | Church--Turing thesis: for any computable problem there is a Turing machine which computes it; also Turing's thesis or Church's thesis; Kleene first used the word thesis (1943) | thesis | rule | sep-turing-machine | 2026-11-20 |
| b3:models-equivalent | The functions computable by a Turing machine, the total functions among the partial recursive functions (closing primitive recursion under unbounded minimisation), the functions representable in combinatory logic, and those computable by Shepherdson and Sturgis's unlimited register machines (1963) are each equal to the general recursive functions | same class | rule | sep-recursive-functions | 2026-11-20 |
| b3:kleene-mu | Kleene introduced (1943) the standard form of the general recursive functions using the minimisation (mu) operator | 1943 | date | sep-turing-machine | 2026-11-20 |
| b3:multitape-hartmanis | Hartmanis and Stearns (1965) proved that any n-tape Turing machine reduces to a single-tape one, and used multitape machines as closer to actual computers | 1965 | date | sep-turing-machine | 2026-11-20 |
| b3:ackermann-1928 | W. Ackermann, Zum Hilbertschen Aufbau der reellen Zahlen, Mathematische Annalen 99, 118--133 | December 1928 | date | crossref | 2026-11-20 |
| b3:ackermann-not-pr | Ackermann (1928) gave a function computable by a nested recursion that is not primitive recursive; Peter (1935) gave a two-argument function pi of the same growth directly; it is not primitive recursive | not primitive recursive | rule | sep-recursive-functions | 2026-11-20 |
| b3:rice-1953 | H. G. Rice, Classes of recursively enumerable sets and their decision problems, Trans. AMS 74(2) 358--366; Theorem (Rice 1953): a non-trivial index set is undecidable | 1953 | date | crossref | 2026-11-20 |
| b3:post-1946 | E. L. Post, A variant of a recursively unsolvable problem, Bull. AMS 52(4) 264--268; the Post correspondence problem, undecidable, introduced by Post in 1946 | 1946 | date | crossref | 2026-11-20 |
| b3:pcp-undecidable | The Post correspondence problem is an undecidable decision problem; the usual proof builds an instance whose match exists if and only if a Turing machine accepts its input | undecidable | rule | wiki-pcp | 2026-11-20 |
| b3:rado-1962 | T. Rado, On non-computable functions, Bell System Technical Journal 41(3) 877--884; the busy beaver introduced as one of the simplest examples of an uncomputable function | May 1962 | date | crossref | 2026-11-20 |
| b3:bb-definition | S(n) is the maximum number of steps an n-state 2-symbol Turing machine can perform from the all-zero tape before halting; Sigma(n) is the most 1s left (counted with the halting step) | S(n), Sigma(n) | rule | bbchallenge-2025 | 2026-11-20 |
| b3:bb-values | S(1) = 1, S(2) = 6, S(3) = 21, S(4) = 107 proved before; S(5) = 47,176,870 and Sigma(5) = 4,098 proved with the Coq proof assistant, enumerating 181,385,789 machines; Sigma(2) = 4; S(6) > 2 uparrow^3 5 | S(5) = 47,176,870 | count | bbchallenge-2025 | 2026-11-20 |
| b3:bb-2024 | the Coq proof Coq-BB5 was released in the spring of 2024 by a contributor of the online bbchallenge collaboration; the paper followed in September 2025 | 2024, 2025 | date | bbchallenge-2025 | 2026-11-20 |
| b3:pilot-ace | Pilot ACE: one of the first computers built in the United Kingdom, at the National Physical Laboratory, a cut-down version of Turing's full ACE design; first ran in 1950; shown at the Science Museum, London | 1950 | date | wiki-pilot-ace | 2026-11-20 |
| b3:hartmanis-stearns-1965 | J. Hartmanis and R. E. Stearns, On the computational complexity of algorithms, Trans. AMS 117, 285--306 | 1965 | date | crossref | 2026-11-20 |
| b3:stearns-hartmanis-lewis-1965 | R. E. Stearns, J. Hartmanis and P. M. Lewis, Hierarchies of memory limited computations, 6th Symposium on Switching Circuit Theory and Logical Design, 179--190 | 1965 | date | crossref | 2026-11-20 |
| b3:time-hierarchy | time hierarchy theorem (deterministic): for time-constructible f, DTIME(o(f(n))) is strictly contained in DTIME(f(n) log f(n)); DTIME(n^a) strictly in DTIME(n^b) iff a < b; P strictly contained in EXPTIME | P != EXP | rule | wiki-time-hierarchy | 2026-11-20 |
| b3:space-hierarchy | space hierarchy theorem: for space-constructible f and g in o(f), SPACE(g(n)) strictly contained in SPACE(f(n)), deterministic or nondeterministic | strict | rule | wiki-space-hierarchy | 2026-11-20 |
| b3:savitch-1970 | W. J. Savitch, Relationships between nondeterministic and deterministic tape complexities, JCSS 4(2) 177--192 | April 1970 | date | crossref | 2026-11-20 |
| b3:savitch-thm | Savitch's theorem: for space-constructible f in Omega(log n), NSPACE(f(n)) is contained in DSPACE(f(n)^2); corollaries PSPACE = NPSPACE and NL contained in L^2; the proof is an algorithm for st-connectivity | f^2 | rule | wiki-savitch | 2026-11-20 |
| b3:stockmeyer-meyer-1973 | L. J. Stockmeyer and A. R. Meyer, Word problems requiring exponential time, STOC '73, 1--9 | 1973 | date | crossref | 2026-11-20 |
| b3:tqbf-complete | TQBF is the canonical PSPACE-complete problem; the recursive algorithm shows it is in PSPACE; many QBF solvers exist despite it | PSPACE-complete | rule | wiki-tqbf | 2026-11-20 |
| b3:immerman-1988 | N. Immerman, Nondeterministic space is closed under complementation, SIAM J. Comput. 17(5) 935--938 | October 1988 | date | crossref | 2026-11-20 |
| b3:szelepcsenyi-1988 | R. Szelepcsenyi, The method of forced enumeration for nondeterministic automata, Acta Informatica 26(3) 279--284 | November 1988 | date | crossref | 2026-11-20 |
| b3:immerman-thm | Immerman--Szelepcsenyi theorem: nondeterministic space classes are closed under complementation, NL = co-NL; proved independently in 1987; st-connectivity is NL-complete | NL = co-NL | rule | wiki-immerman | 2026-11-20 |
| b3:cobham-edmonds | Cobham's thesis (Cobham--Edmonds thesis): problems can be feasibly computed only if they lie in P; Cobham's 1965 paper The intrinsic computational difficulty of functions and Edmonds's 1965 Paths, trees, and flowers | 1965 | rule | wiki-cobham | 2026-11-20 |
| b3:edmonds-1965 | J. Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17, 449--467 | 1965 | date | crossref | 2026-11-20 |
| b3:cook-1971 | S. A. Cook, The complexity of theorem-proving procedures, STOC '71, 151--158 | 1971 | date | crossref | 2026-11-20 |
| b3:levin-1973 | L. Levin, Universal search problems (in Russian), Problems of Information Transmission 9(3) 115--116; Levin considered search problems and gave six NP-complete search problems | 1973 | date | wiki-cook-levin | 2026-11-20 |
| b3:cook-levin | Cook--Levin theorem: SAT is NP-complete; named after Cook and Levin; the proof by polynomial-time many-one reduction is due to Karp, based on Cook's earlier proof with a different notion of reducibility; NP-completeness developed in parallel in North America and the Soviet Union | SAT NP-complete | rule | wiki-cook-levin | 2026-11-20 |
| b3:karp-1972 | R. M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 85--103; 21 problems shown NP-complete by reductions from SAT; Karp introduced completeness by polynomial-time many-one reduction | 21 problems, 1972 | count | crossref | 2026-11-20 |
| b3:karp-list | Karp's 21 problems include satisfiability, 3-SAT, clique, vertex cover, chromatic number, Hamiltonian cycle (directed and undirected), knapsack, exact cover, set packing | list | rule | wiki-karp21 | 2026-11-20 |
| b3:garey-johnson-1979 | M. R. Garey and D. S. Johnson, Computers and Intractability: A Guide to the Theory of NP-Completeness (1979), with an appendix of over 300 NP-hard problems | 1979, over 300 | count | wiki-garey-johnson | 2026-11-20 |
| b3:aspvall-1979 | B. Aspvall, M. F. Plass and R. E. Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, IPL 8(3) 121--123; linear-time 2-SAT by strongly connected components of the implication graph | March 1979 | date | crossref | 2026-11-20 |
| b3:johnson-1974 | D. S. Johnson, Approximation algorithms for combinatorial problems, JCSS 9(3) 256--278 | December 1974 | date | crossref | 2026-11-20 |
| b3:lovasz-1975 | L. Lovasz, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13(4) 383--390 | 1975 | date | crossref | 2026-11-20 |
| b3:greedy-set-cover | the greedy set cover finds a cover at most H(n) times the minimum, H(n) the n-th harmonic number, at most ln n + 1 (Johnson 1974, Lovasz 1975) | H(n) | rule | wiki-set-cover | 2026-11-20 |
| b3:christofides | Christofides algorithm for metric TSP, within 3/2 of optimal; Christofides published it in 1976, Serdyukov found it independently (published 1978) | 3/2, 1976 | rule | wiki-christofides | 2026-11-20 |
| b3:davis-putnam-1960 | M. Davis and H. Putnam, A computing procedure for quantification theory, JACM 7(3) 201--215 | July 1960 | date | crossref | 2026-11-20 |
| b3:dll-1962 | M. Davis, G. Logemann and D. Loveland, A machine program for theorem-proving, CACM 5(7) 394--397 | July 1962 | date | crossref | 2026-11-20 |
| b3:grasp-1999 | J. P. Marques-Silva and K. A. Sakallah, GRASP: a search algorithm for propositional satisfiability, IEEE Trans. Computers 48(5) 506--521 | May 1999 | date | crossref | 2026-11-20 |
| b3:chaff-2001 | M. W. Moskewicz, C. F. Madigan, Y. Zhao, L. Zhang and S. Malik, Chaff, Proc. 38th Design Automation Conference, 530--535 | 2001 | date | crossref | 2026-11-20 |
| b3:dowling-gallier-1984 | W. F. Dowling and J. H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, J. Logic Programming 1(3) 267--284 | October 1984 | date | crossref | 2026-11-20 |
| b3:walksat | WalkSAT picks an unsatisfied clause at random and flips one of its variables, the one breaking fewest satisfied clauses or, with some probability, a random one | rule | rule | wiki-walksat | 2026-11-20 |
| b3:held-karp-1962 | M. Held and R. M. Karp, A dynamic programming approach to sequencing problems, J. SIAM 10(1) 196--210 | March 1962 | date | crossref | 2026-11-20 |
| b3:lin-kernighan-1973 | S. Lin and B. W. Kernighan, An effective heuristic algorithm for the traveling-salesman problem, Operations Research 21(2) 498--516 | April 1973 | date | crossref | 2026-11-20 |
| b3:3sat-threshold | Selman, Mitchell and Levesque (1996) found a phase transition for random 3-SAT, from almost certainly satisfiable to almost certainly unsatisfiable, at a clause-to-variable ratio of about 4.26, difficulty measured in DPLL recursive calls | 4.26 | count | wiki-sat | 2026-11-20 |
| b3:dpll-history | DPLL refines the Davis--Putnam algorithm, a resolution-based procedure of Davis and Putnam (1960) | 1960 | rule | wiki-dpll | 2026-11-20 |
| b3:cdcl-origin | conflict-driven clause learning was proposed by Marques-Silva and Sakallah (1996, 1999), GRASP; CDCL learns clauses and backtracks non-chronologically | 1996, 1999 | rule | wiki-cdcl | 2026-11-20 |
| b3:chaff | Chaff is an instance of DPLL with a number of enhancements for efficient implementation; Moskewicz, Madigan, Zhao, Zhang, Malik, DAC 2001 | 2001 | rule | wiki-chaff | 2026-11-20 |
| b3:lin-kernighan | Lin--Kernighan is a local search heuristic for the symmetric TSP that looks for a new tour whose symmetric difference with the current one is not too large | rule | rule | wiki-lin-kernighan | 2026-11-20 |
| b3:walksat-1993 | B. Selman, H. Kautz and B. Cohen, Local search strategies for satisfiability testing, Second DIMACS Implementation Challenge, October 1993 (final version 1996) | 1993 | date | wiki-walksat | 2026-11-20 |
| b3:shannon-1948 | C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3) 379--423 | July 1948 | date | crossref | 2026-11-20 |
| b3:noisy-channel | the noisy-channel coding theorem, stated by Shannon in 1948: for a channel of capacity C and rate R < C, codes exist with error probability arbitrarily small | 1948 | rule | wiki-noisy-channel | 2026-11-20 |
| b3:kraft-mcmillan | Kraft's inequality was published by Kraft in 1949, for prefix codes (attributing the analysis to Redheffer); McMillan (1956) proved it independently for uniquely decodable codes | 1949, 1956 | rule | wiki-kraft | 2026-11-20 |
| b3:mcmillan-1956 | B. McMillan, Two inequalities implied by unique decipherability, IRE/IEEE Trans. Information Theory 2(4) 115--116 | December 1956 | date | crossref | 2026-11-20 |
| b3:huffman-1952 | David Huffman, A method for the construction of minimum-redundancy codes, Proc. IRE 40(9) 1098--1101 | September 1952 | date | crossref | 2026-11-20 |
| b3:hamming-1950 | R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2) 147--160 | April 1950 | date | crossref | 2026-11-20 |
| b3:hamming-history | Richard Hamming invented Hamming codes in 1950 to correct errors of punched card readers; he worked at Bell Labs on the relay-based Model V computer fed by punched paper tape | 1950 | rule | wiki-hamming-code | 2026-11-20 |
| b3:reed-solomon-1960 | I. S. Reed and G. Solomon, Polynomial codes over certain finite fields, J. SIAM 8(2) 300--304 | June 1960 | date | crossref | 2026-11-20 |
| b3:rs-uses | Reed--Solomon codes are used in CDs, DVDs, Blu-ray discs and QR codes; the compact disc (1982) was the first mass-produced consumer use; nearly all two-dimensional bar codes, QR among them, use them to read a partly damaged code | 1982 | rule | wiki-reed-solomon | 2026-11-20 |
| b3:cyclic-burst | cyclic codes are particularly well suited to detecting burst errors, contiguous runs of erroneous symbols, common on many channels | rule | rule | wiki-crc | 2026-11-20 |
| b3:hoare-1969 | C. A. R. Hoare, An axiomatic basis for computer programming, CACM 12(10) 576--580 | October 1969 | date | crossref | 2026-11-20 |
| b3:hoare-floyd | Hoare logic was proposed in 1969 by Tony Hoare; its ideas were seeded by Robert W. Floyd, who had published a similar system for flowcharts; also called Floyd--Hoare logic | 1969 | rule | wiki-hoare-logic | 2026-11-20 |
| b3:dijkstra-1975 | E. W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, CACM 18(8) 453--457 | August 1975 | date | crossref | 2026-11-20 |
| b3:clarke-emerson-1981 | CTL was first proposed by E. M. Clarke and E. A. Emerson in 1981, to synthesise synchronisation skeletons of concurrent programs | 1981 | rule | wiki-ctl | 2026-11-20 |
| b3:queille-sifakis-1982 | J. P. Queille and J. Sifakis, Specification and verification of concurrent systems in CESAR, LNCS, 337--351 | 1982 | date | crossref | 2026-11-20 |
| b3:mc-turing-2007 | model checking began with the work of Clarke, Emerson, Queille and Sifakis; Clarke, Emerson and Sifakis shared the 2007 Turing Award for founding and developing the field | 2007 | rule | wiki-model-checking | 2026-11-20 |
| b3:pnueli-1977 | LTL was first proposed for formal verification of programs by Amir Pnueli in 1977; Pnueli received the 1996 Turing Award for introducing temporal logic into computing science | 1977, 1996 | rule | wiki-ltl | 2026-11-20 |
| b3:pnueli-turing | Pnueli received the 1996 Turing award for seminal work introducing temporal logic into computing science | 1996 | rule | wiki-model-checking | 2026-11-20 |
| b3:bsearch-overflow | with fixed-size integer indices, computing the midpoint as (L+R)/2 can overflow even when L and R are in range; with L, R nonnegative, L + (R-L)/2 avoids it | rule | rule | wiki-binary-search | 2026-11-20 |
| b3:sqlite-header | the first 100 bytes of an SQLite database file are its header, multibyte fields big-endian: offset 0, 16 bytes, "SQLite format 3" and a zero byte; offset 16, 2 bytes, page size (1 means 65536); 18 and 19 write/read format versions (1 legacy, 2 WAL); 20 reserved bytes per page; 24 file change counter; 28 database size in pages; 44 schema format number (1 to 4); 56 text encoding (1 = UTF-8) | layout | layout | sqlite-fileformat | 2026-11-20 |
| b3:sqlite-btree-page | an SQLite b-tree page is, in order: the 100-byte file header (page 1 only), an 8-byte (leaf) or 12-byte (interior) page header, the cell pointer array, unallocated space, the cell content area, the reserved region | layout | layout | sqlite-fileformat | 2026-11-20 |
| b3:sqlite-page-size | an SQLite page size is a power of two from 512 to 65536; the default was almost always 1024 bytes for many years and became 4096 with version 3.12.0 (2016-03-29) | 4096 | size | sqlite-pragma | 2026-11-20 |
| b3:sqlite-eqp | in EXPLAIN QUERY PLAN output, "SCAN" is a full-table scan, "SEARCH" visits only a subset of the rows; an index holding every column the query needs shows as USING COVERING INDEX; the output format is for interactive debugging and may change between releases | rule | rule | sqlite-eqp | 2026-11-20 |
| b3:bayer-mccreight-1972 | R. Bayer and E. M. McCreight, Organization and maintenance of large ordered indexes, Acta Informatica 1(3) 173--189 | 1972 | year | crossref | 2026-11-20 |
| b3:comer-1979 | D. Comer, The ubiquitous B-tree, ACM Computing Surveys 11(2) 121--137 (June 1979); it notes the B+ tree's use in IBM's VSAM | June 1979 | date | crossref | 2026-11-20 |
| b3:fagin-1979 | R. Fagin, J. Nievergelt, N. Pippenger and H. R. Strong, Extendible hashing --- a fast access method for dynamic files, ACM TODS 4(3) 315--344 | September 1979 | date | crossref | 2026-11-20 |
| b3:litwin-1980 | linear hashing, a hash table that grows or shrinks one bucket at a time, was invented by W. Litwin in 1980 (Proc. 6th VLDB, 212--223) | 1980 | year | wiki-linear-hashing | 2026-11-20 |
| b3:oneil-1996 | P. O'Neil, E. Cheng, D. Gawlick and E. O'Neil, The log-structured merge-tree (LSM-tree), Acta Informatica 33(4) 351--385 | June 1996 | date | crossref | 2026-11-20 |
| b3:sqlite-btrees | SQLite keeps one table b-tree per rowid table, keyed by a 64-bit signed integer with all data in the leaves, and one index b-tree per index, with arbitrary keys and no data; an interior page holds K keys and K+1 child pointers | rule | rule | sqlite-fileformat | 2026-11-20 |
| b3:selinger-1979 | P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, SIGMOD 1979 | 1979 | year | crossref | 2026-11-20 |
| b3:graefe-1993 | G. Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2) 73--169 | June 1993 | date | crossref | 2026-11-20 |
| b3:volcano-1994 | G. Graefe, Volcano --- an extensible and parallel query evaluation system, IEEE TKDE 6(1) 120--135 | 1994 | year | crossref | 2026-11-20 |
| b3:ioannidis-1991 | Y. E. Ioannidis and S. Christodoulakis, On the propagation of errors in the size of join results, SIGMOD 1991, 268--277 | 1991 | year | crossref | 2026-11-20 |
| b3:sqlite-nested | all joins in SQLite are implemented using nested scans; EXPLAIN QUERY PLAN prints one SCAN or SEARCH record per nested loop | rule | rule | sqlite-eqp | 2026-11-20 |
| b3:sqlite-analyze | ANALYZE gathers statistics about tables and indices and stores them in internal tables where the query optimizer uses them to choose plans; it is never required | rule | rule | sqlite-analyze | 2026-11-20 |
| b3:sqlite-stat1 | sqlite_stat1(tbl, idx, stat): per index, stat lists the approximate number of rows, then for N > 1 the average number of rows sharing the first N-1 columns' values; with idx NULL, stat is the approximate number of rows of the table | layout | layout | sqlite-fileformat | 2026-11-20 |
| b3:eswaran-1976 | K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11) 624--633 | November 1976 | date | crossref | 2026-11-20 |
| b3:bernstein-goodman-1981 | P. A. Bernstein and N. Goodman, Concurrency control in distributed database systems, ACM Computing Surveys 13(2) 185--221 | June 1981 | date | crossref | 2026-11-20 |
| b3:berenson-1995 | H. Berenson, P. Bernstein, J. Gray, J. Melton, E. O'Neil and P. O'Neil, A critique of ANSI SQL isolation levels, SIGMOD 1995, 1--10 | 1995 | year | crossref | 2026-11-20 |
| b3:berenson-si | snapshot isolation exhibits none of the anomalies the SQL-92 standard prohibits, yet is not serialisable; Berenson et al. used it to criticise the standard's definitions | rule | rule | wiki-snapshot-isolation | 2026-11-20 |
| b3:eswaran-2pl | Eswaran et al. 1976 define transaction, consistency and schedule, show that consistency requires that a transaction cannot request new locks after releasing a lock, and propose predicate locks (paper abstract) | rule | rule | crossref | 2026-11-20 |
| b3:fekete-si-first | snapshot isolation was first described in Berenson et al. 1995 and was implemented by Oracle and Microsoft SQL Server; it does not guarantee serializability in all cases (paper abstract) | rule | rule | crossref | 2026-11-20 |
| b3:fekete-2005 | A. Fekete, D. Liarokapis, E. O'Neil, P. O'Neil and D. Shasha, Making snapshot isolation serializable, ACM Transactions on Database Systems 30(2) 492--528 | June 2005 | date | crossref | 2026-11-20 |
| b3:cahill-2008 | M. J. Cahill, U. Röhm and A. D. Fekete, Serializable isolation for snapshot databases, SIGMOD 2008, 729--738 | June 2008 | date | crossref | 2026-11-20 |
| b3:fekete-theory | Fekete et al. 2005 develop a theory characterising when non-serialisable executions occur under SI, and discuss how to modify program logic so that serialisability is guaranteed (paper abstract) | rule | rule | crossref | 2026-11-20 |
| b3:cahill-dangerous | Cahill et al. 2008 showed that write-skew anomalies can be prevented by detecting and aborting dangerous triplets of concurrent transactions | rule | rule | wiki-snapshot-isolation | 2026-11-20 |
| b3:ssi-postgres | serializable snapshot isolation was adopted in PostgreSQL 9.1, where it is the Serializable level | PostgreSQL 9.1 | version | wiki-snapshot-isolation | 2026-11-20 |
| b3:mohan-1992 | C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh and P. Schwarz, ARIES, ACM Transactions on Database Systems 17(1) 94--162 | March 1992 | date | crossref | 2026-11-20 |
| b3:aries-principles | ARIES: write-ahead logging, repeating history during redo, logging changes during undo; designed for steal, no-force; analysis, redo and undo phases; used by IBM Db2 and Microsoft SQL Server | rule | rule | wiki-aries | 2026-11-20 |
| b3:2pl-serialisable | two-phase locking guarantees conflict serialisability | rule | rule | wiki-2pl | 2026-11-20 |
| b3:repeatable-read-phantom | at repeatable read a lock-based implementation keeps read and write locks to the end of the transaction but no range locks, so phantom reads can occur | rule | rule | wiki-isolation | 2026-11-20 |
| b3:sqlite-serializable | transactions in SQLite are serializable; changes made in one connection are invisible to the others before commit | rule | rule | sqlite-isolation | 2026-11-20 |
| b3:sqlite-wal-snapshot | in WAL mode SQLite exhibits snapshot isolation: a read transaction sees the database as it was when it started; readers do not block writers and a writer does not block readers; one writer at a time | rule | rule | sqlite-wal | 2026-11-20 |
| b3:sqlite-locks | rollback-journal locks SHARED, RESERVED, PENDING, EXCLUSIVE: many SHARED readers; one RESERVED writer-to-be; PENDING waits for readers to clear; EXCLUSIVE needed to write the file | rule | rule | sqlite-locking | 2026-11-20 |
| b3:sqlite-begin | BEGIN DEFERRED (the default) starts no transaction until the database is first accessed; BEGIN IMMEDIATE starts a write transaction at once and may fail with SQLITE_BUSY if another write transaction is active | rule | rule | sqlite-transaction | 2026-11-20 |
| b3:sqlite-upgrade | a read transaction is upgraded to a write transaction at its first write if possible; if another connection has already modified the database or is modifying it, the upgrade is not possible and the write fails with SQLITE_BUSY | rule | rule | sqlite-transaction | 2026-11-20 |
| b3:sqlite-raise | when a trigger calls RAISE(ABORT, message) the ON CONFLICT processing is performed, the current query terminates and SQLITE_CONSTRAINT is returned with the message | rule | rule | sqlite-trigger | 2026-11-20 |
| b3:amdahl-1967 | G. M. Amdahl, Validity of the single processor approach to achieving large scale computing capabilities, AFIPS Spring Joint Computer Conference 1967, 483 | 1967 | year | crossref | 2026-11-20 |
| b3:amdahl-named | Amdahl's law is named after Gene Amdahl and was presented at the AFIPS Spring Joint Computer Conference in 1967 | 1967 | year | wiki-amdahl | 2026-11-20 |
| b3:gustafson-1988 | J. L. Gustafson, Reevaluating Amdahl's law, Communications of the ACM 31(5) 532--533 | May 1988 | date | crossref | 2026-11-20 |
| b3:gustafson-barsis | Gustafson's law is named after John L. Gustafson and his colleague Edwin H. Barsis, presented in Reevaluating Amdahl's Law in 1988 | 1988 | year | wiki-gustafson | 2026-11-20 |
| b3:brent-1974 | R. P. Brent, The parallel evaluation of general arithmetic expressions, Journal of the ACM 21(2) 201--206 | April 1974 | date | crossref | 2026-11-20 |
| b3:brent-scheduling | the scheduling theorem of the work-time analysis of parallel algorithms is due to Brent (1974) | 1974 | year | wiki-parallel-analysis | 2026-11-20 |
| b3:hillis-steele-1986 | W. D. Hillis and G. L. Steele Jr., Data parallel algorithms, Communications of the ACM 29(12) 1170--1183; the shorter-span, not work-efficient prefix sum | December 1986 | date | wiki-prefix-sum | 2026-11-20 |
| b3:blelloch-1989 | G. E. Blelloch, Scans as primitive parallel operations, IEEE Transactions on Computers 38(11) 1526--1538 | 1989 | year | crossref | 2026-11-20 |
| b3:blumofe-leiserson-1999 | R. D. Blumofe and C. E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5) 720--748: the first provably good work-stealing scheduler, expected time T1/P + O(T_inf) for fully strict computations (abstract) | September 1999 | date | crossref | 2026-11-20 |
| b3:cray-1 | Cray-1: designed by Seymour Cray, made by Cray Research; announced 1975, first installed at Los Alamos National Laboratory in 1976; first supercomputer to successfully implement the vector processor design; 160 MFLOPS; eighty sold | 1976 | year | wiki-cray-1 | 2026-11-20 |
| b3:lamport-1978 | L. Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7) 558--565 | July 1978 | date | crossref | 2026-11-20 |
| b3:fidge-mattern-1988 | vector clocks canonically cited to C. J. Fidge, Timestamps in message-passing systems that preserve the partial ordering (11th Australian Computer Science Conference, February 1988) and to F. Mattern's work of 1988; the generalisation from scalar to vector time was developed several times, apparently independently | 1988 | year | wiki-vector-clock | 2026-11-20 |
| b3:chandy-lamport-1985 | K. M. Chandy and L. Lamport, Distributed snapshots: determining global states of distributed systems, ACM Transactions on Computer Systems 3(1) 63--75; the algorithm assumes FIFO channels, no failures, and lets any process initiate | February 1985 | date | crossref, wiki-chandy-lamport | 2026-11-20 |
| b3:akkoyunlu-1975 | E. A. Akkoyunlu, K. Ekanadham and R. V. Huber, Some constraints and tradeoffs in the design of network communications, SOSP 1975, 67--74: first published statement and impossibility proof of the two generals problem (told with two groups of gangsters) | 1975 | year | crossref, wiki-two-generals | 2026-11-20 |
| b3:gray-1978 | the name Two Generals Paradox given by Jim Gray in Notes on Data Base Operating Systems, 1978 | 1978 | year | wiki-two-generals | 2026-11-20 |
| b3:birrell-nelson-1984 | A. D. Birrell and B. J. Nelson, Implementing remote procedure calls, ACM Transactions on Computer Systems 2(1) 39--59 (Xerox PARC, Cedar) | February 1984 | date | crossref, wiki-rpc | 2026-11-20 |
| b3:nelson-1981 | Bruce Jay Nelson generally credited with coining the term remote procedure call, in his 1981 PhD thesis at Xerox PARC / Carnegie Mellon | 1981 | year | wiki-rpc | 2026-11-20 |
| b3:raft-2014 | D. Ongaro and J. Ousterhout, In Search of an Understandable Consensus Algorithm; a shorter version received a Best Paper Award at the 2014 USENIX Annual Technical Conference; Raft designed as an alternative to Paxos, meant to be more understandable | 2014 | year | raft-site, wiki-raft | 2026-11-20 |
| b3:flp-1985 | M. J. Fischer, N. A. Lynch and M. S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2) 374--382 | April 1985 | date | crossref | 2026-11-20 |
| b3:gilbert-lynch-2002 | S. Gilbert and N. Lynch, Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services, ACM SIGACT News 33(2) 51--59 | June 2002 | date | crossref, wiki-cap | 2026-11-20 |
| b3:brewer-2000 | E. A. Brewer, Towards Robust Distributed Systems, keynote at Principles of Distributed Computing (PODC) 2000; the CAP theorem also named Brewer's theorem | 2000 | year | wiki-cap | 2026-11-20 |
| b3:paxos-1998 | L. Lamport, The part-time parliament, ACM Transactions on Computer Systems 16(2) 133--169 (Paxos) | May 1998 | date | crossref | 2026-11-20 |
| b3:gifford-1979 | D. K. Gifford, Weighted voting for replicated data, SOSP 1979, 150--162 | 1979 | year | crossref | 2026-11-20 |
| b3:crdt-2011 | M. Shapiro, N. Preguica, C. Baquero and M. Zawirski, Conflict-Free Replicated Data Types, SSS 2011, LNCS 386--400 | 2011 | year | crossref | 2026-11-20 |
| b3:pacelc | PACELC first described by Daniel Abadi in a blog post of 2010, clarified in a paper of 2012 (Consistency Tradeoffs in Modern Distributed Database System Design: CAP is Only Part of the Story, IEEE Computer 45(2) 37--42) | 2010; 2012 | year | wiki-pacelc, crossref | 2026-11-20 |
| b3:2pc-blocking | two-phase commit is a blocking protocol: a participant that has voted to commit blocks until it receives commit or rollback, and if the coordinator fails permanently some participants never resolve their transactions | -- | -- | wiki-2pc | 2026-11-20 |
| b3:kerckhoffs-1883 | A. Kerckhoffs, La cryptographie militaire, Journal des sciences militaires IX 5--83, January 1883; a cryptosystem should be secure even if everything about it except the key is public; Shannon's phrasing: the enemy knows the system | January 1883 | date | wiki-kerckhoffs | 2026-11-20 |
| b3:shannon-1949 | C. E. Shannon, Communication Theory of Secrecy Systems, Bell System Technical Journal 28(4) 656--715 | October 1949 | date | crossref, wiki-kerckhoffs | 2026-11-20 |
| b3:aes-fips197 | AES: Nr = 10, 12, 14 rounds for 128-, 192-, 256-bit keys; S-box {53} -> {ed}; Appendix B cipher example: key 2b7e151628aed2a6abf7158809cf4f3c, input 3243f6a8885a308d313198a2e0370734, output 3925841d02dc09fbdc118597196a0b32; Appendix A.1 round keys w4..w7 = a0fafe17 88542cb1 23a33939 2a6c7605, w40..w43 = d014f9a8 c9ee2589 e13f0cc8 b6630ca6 | -- | -- | fips197 | 2026-11-20 |
| b3:sp800-38a | five confidentiality modes: ECB, CBC, CFB, OFB, CTR; F.2.1 CBC-AES128 (IV 000102...0f) and F.5.1 CTR-AES128 vectors | 2001 | year | sp800-38a | 2026-11-20 |
| b3:rfc8439 | ChaCha20 and Poly1305, both designed by D. J. Bernstein; ChaCha20 runs 20 rounds from the constants 0x61707865 0x3320646e 0x79622d32 0x6b206574; the nonce MUST not be repeated for the same key; operations of ChaCha20 are additions, XORs and fixed rotations, implementable in constant time, with no key-dependent table offsets; many AES implementations are vulnerable to cache-collision timing attacks; test vectors 2.3.2 (block), 2.4.2 (cipher), 2.5.2 (Poly1305 tag a8061dc1305136c6c22b8baf0c0127a9), 2.8.2 (AEAD tag 1ae10b594f09e26a7e902ecbd0600691) | June 2018 | date | rfc8439 | 2026-11-20 |
| b3:fips180-sha256 | SHA-256: message length < 2^64 bits, 512-bit blocks, 32-bit words, 256-bit digest; constants K = first 32 bits of the fractional parts of the cube roots of the first 64 primes, initial hash from the square roots of the first 8; K0 = 428a2f98, K63 = c67178f2, H0(0) = 6a09e667; a Merkle--Damgard construction; PKCS#7 padding (RFC 5652): N added bytes each of value N | -- | -- | fips180-4, wiki-sha2, wiki-padding | 2026-11-20 |
| b3:rfc2104 | HMAC(K, text) = H(K xor opad, H(K xor ipad, text)), ipad = 0x36 and opad = 0x5C repeated B times, B = 64 bytes for the hash functions considered | February 1997 | date | rfc2104 | 2026-11-20 |
| b3:vaudenay-2002 | S. Vaudenay, Security Flaws Induced by CBC Padding -- Applications to SSL, IPSEC, WTLS..., EUROCRYPT 2002, LNCS 534--545; the padding oracle attack on CBC decryption, which uses padding validation to decrypt the ciphertext | 2002 | year | crossref, wiki-padding-oracle | 2026-11-20 |
| b3:bellare-namprempre-2000 | M. Bellare and C. Namprempre, Authenticated Encryption: Relations among Notions and Analysis of the Generic Composition Paradigm, ASIACRYPT 2000, LNCS 531--545; of three compositions, encrypt-then-MAC implies security against adaptive chosen-ciphertext attack given minimal properties of both parts | 2000 | year | crossref, wiki-ae | 2026-11-20 |
| b3:py-crypto-docs | Python: secrets generates cryptographically strong random numbers and should be used in preference to random, designed for modelling and simulation; hmac.compare_digest recommended over == to reduce timing attacks; hashlib.sha256 | -- | -- | py-secrets, py-hmac, py-hashlib | 2026-11-20 |
| b3:enigma | Enigma machine invented by German engineer Arthur Scherbius at the end of World War I; an electromechanical rotor mechanism scrambles the 26 letters; photo: the military model Enigma I, used from 1930, Museo della Scienza e della Tecnologia, Milan, Alessandro Nassiri 2012, CC BY-SA 4.0 | 2012 | year | wiki-enigma, commons-enigma | 2026-11-20 |
| b3:diffie-hellman-1976 | W. Diffie and M. E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6) 644--654 | November 1976 | date | crossref | 2026-11-20 |
| b3:rsa-1978 | R. L. Rivest, A. Shamir and L. Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2) 120--126 | February 1978 | date | crossref | 2026-11-20 |
| b3:shanks-1971 | baby-step giant-step: a meet-in-the-middle algorithm for discrete logarithms in a finite abelian group, by Daniel Shanks (Proc. Symp. Pure Math. 20, 415--440, 1971); usable by an eavesdropper on Diffie--Hellman when the modulus is not too large | 1971 | year | wiki-bsgs | 2026-11-20 |
| b3:schnorr-1991 | C. P. Schnorr, Efficient signature generation by smart cards, Journal of Cryptology 4(3) 161--174; reusing the secret nonce k on two signatures of different messages lets observers recover the private key | 1991 | year | crossref, wiki-schnorr | 2026-11-20 |
| b3:oaep | PKCS#1 v1.5 padding does not give enough security for some messages; later versions include OAEP (Bellare and Rogaway), which should be used in any new application | -- | -- | wiki-rsa | 2026-11-20 |
| b3:rfc8446 | TLS 1.3: key exchange modes (EC)DHE, PSK-only, PSK with (EC)DHE; full handshake ClientHello + key_share, ServerHello + key_share, {EncryptedExtensions}, {CertificateRequest*}, {Certificate}, {CertificateVerify}, {Finished}, then client {Certificate*} {CertificateVerify*} {Finished}; CertificateVerify is a signature over the handshake, Finished a MAC over it; static RSA and Diffie--Hellman suites removed, all public-key key exchange now gives forward secrecy; key schedule from HKDF-Extract and Derive-Secret | August 2018 | date | rfc8446 | 2026-11-20 |
| b3:rfc5869 | HKDF: extract-then-expand with HMAC; test cases A.1--A.3 (SHA-256), case 1 PRK 077709362c..., OKM 3cb25f25faac... | May 2010 | date | rfc5869 | 2026-11-20 |
| b3:rfc7748 | X25519 and X448: curves for the ~128-bit and ~224-bit security levels; the prime 2^255 - 19 for ~128 bits | January 2016 | date | rfc7748 | 2026-11-20 |
| b3:sp800-57-table2 | comparable security strengths: 112 bits -- RSA k = 2048, DH group L = 2048 N = 224, ECC f = 224--255; 128 -- AES-128, k = 3072, L = 3072 N = 256, f = 256--383; 192 -- k = 7680; 256 -- k = 15360, f = 512+; estimates significantly affected when quantum computing becomes practical; Table 4: 112-bit strength acceptable for applying protection through 2030, disallowed from 2031; protection should not be applied with an algorithm whose lifetime ends before the security life of the data (example: lifetime ending 31 December 2030, data with a four-year life not encrypted after 31 December 2026) | May 2020 | date | sp800-57 | 2026-11-20 |
| b3:passwords | SP 800-63B-4: passwords SHALL be salted and hashed with a password hashing scheme taking a password, a salt and a cost factor; cost factor as high as practical and increased over time; salt at least 32 bits; RFC 7914: scrypt is memory-hard, ROMix keeps N blocks of 128 r bytes, N a power of 2, r = 8 and p = 1 yield good results; RFC 8018: PBKDF2 with an iteration count c; Python: hashlib.scrypt (RFC 7914), hashlib.pbkdf2_hmac (PKCS#5 PBKDF2 with HMAC), a good password hash is tunable, slow and salted | Aug 2025 | date | sp800-63b-4, rfc7914, rfc8018, py-hashlib | 2026-11-20 |
| b3:hasse | Hasse's theorem: N points on an elliptic curve over a field of q elements satisfy abs(N - (q + 1)) <= 2 sqrt(q); proved by Helmut Hasse in 1933, published 1936 | 1933 | year | wiki-hasse | 2026-11-20 |
| b3:rsa-signatures | Full Domain Hash: RSA signature in the hash-and-sign paradigm, hashing to the size of the modulus and raising to the secret exponent, provably secure in the random oracle model; PSS designed by Bellare and Rogaway, standardised in PKCS#1 v2.1, to replace PKCS#1 v1.5 signatures | -- | -- | wiki-fdh, wiki-pss | 2026-11-20 |
| b3:aleph-one-1996 | Elias Levy ("Aleph One"), Smashing The Stack for Fun and Profit, Phrack 7(49), article 14; the canonical stack-overflow exploit overwrites the function's return address | 8 November 1996 | date | wiki-stack-overflow | 2026-11-20 |
| b3:morris-worm-1988 | the Morris worm exploited a buffer overflow in the finger network service, a debug mode of sendmail and the trust of rsh/rexec logins without passwords | 2 November 1988 | date | wiki-morris | 2026-11-20 |
| b3:stackguard-1998 | stack-smashing protection first implemented by StackGuard in 1997 and published at the 1998 USENIX Security Symposium (Cowan et al.); terminator, random and random-XOR canaries | 1998 | year | wiki-bop | 2026-11-20 |
| b3:pax-aslr-2001 | the PaX project coined the term ASLR and published the first design and implementation, a Linux kernel patch | July 2001 | date | wiki-aslr | 2026-11-20 |
| b3:gcc-stack-protector | -fstack-protector adds a guard variable to functions with vulnerable objects (alloca, buffers of 8 bytes or more), initialised on entry and checked on exit, printing an error and exiting on failure; -fstack-protector-all protects all functions | -- | -- | gcc-instrumentation | 2026-11-20 |
| b3:asan | AddressSanitizer: compiler instrumentation and a run-time library; detects out-of-bounds accesses to heap, stack and globals, use-after-free, double free; typical slowdown 2x | -- | -- | asan-docs | 2026-11-20 |
| b3:stride | STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege; a model for threat models | -- | -- | wiki-stride | 2026-11-20 |
| b3:owasp-top10 | OWASP Top Ten, the most critical application security risks: first published 2003, editions 2004, 2007, 2010, 2013, 2017, 2021, 2025 | 2025 | year | wiki-owasp | 2026-11-20 |
| b3:saltzer-schroeder-1975 | J. H. Saltzer and M. D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9) 1278--1308; least privilege: every module accesses only what its legitimate purpose needs | 1975 | year | crossref, wiki-least-privilege | 2026-11-20 |
| b3:hardy-1988 | N. Hardy, The Confused Deputy (or why capabilities might have been invented), ACM SIGOPS Operating Systems Review 22(4) 36--38; the example: a compiler with rights to the system directory wrote its debugging output to a file named by a user, the billing file, and destroyed it | October 1988 | date | crossref, wiki-confused-deputy | 2026-11-20 |
| b3:web-defences | sqlite3: always use placeholders instead of string formatting to bind values, to avoid SQL injection; subprocess: with shell=True the application must quote whitespace and metacharacters to avoid shell injection; html.escape converts &, < and > (and quotes by default) to HTML-safe sequences; Set-Cookie: HttpOnly forbids JavaScript access (document.cookie), mitigating XSS; Secure sends only over https; SameSite=Strict sends the cookie only for requests from the site that set it; CSP: a standard to prevent XSS, clickjacking and other code injection | -- | -- | py-sqlite3, py-subprocess, py-html, mdn-set-cookie, wiki-csp | 2026-11-20 |
| b3:parnas-1972 | D. L. Parnas, On the criteria to be used in decomposing systems into modules, Communications of the ACM 15(12) 1053--1058; first description of information hiding | December 1972 | date | crossref, wiki-information-hiding | 2026-11-20 |
| b3:gof-1994 | Gamma, Helm, Johnson and Vlissides, Design Patterns: Elements of Reusable Object-Oriented Software, 1994; 23 classic patterns, examples in C++ and Smalltalk; authors called the Gang of Four | 1994 | year | wiki-design-patterns | 2026-11-20 |
| b3:solid | Robert C. Martin introduced the SOLID principles in his 2000 paper Design Principles and Design Patterns; the acronym was coined around 2004 by Michael Feathers | 2000; 2004 | year | wiki-solid | 2026-11-20 |
| b3:mvc | model-view-controller created by Trygve Reenskaug while working on Smalltalk-79 at Xerox PARC in the late 1970s | late 1970s | -- | wiki-mvc | 2026-11-20 |
| b3:uml | UML adopted as a standard by the Object Management Group in 1997, published by ISO in 2005 | 1997 | year | wiki-uml | 2026-11-20 |
| b3:mutation-1978 | R. A. DeMillo, R. J. Lipton and F. G. Sayward, Hints on Test Data Selection: Help for the Practicing Programmer, Computer 11(4) 34--41; mutation testing first proposed by Lipton in 1971; mutation score = killed / total mutants; equivalent mutants cannot be killed, and detecting them is a major obstacle | April 1978 | date | crossref, wiki-mutation-testing | 2026-11-20 |
| b3:quickcheck-2000 | K. Claessen and J. Hughes, QuickCheck: a lightweight tool for random testing of Haskell programs, ICFP 2000, 268--279 | September 2000 | date | crossref, wiki-quickcheck | 2026-11-20 |
| b3:metamorphic-1998 | metamorphic testing invented by T. Y. Chen, technical report HKUST-CS98-01 (with Cheung and Yiu) | 1998 | year | wiki-metamorphic | 2026-11-20 |
| b3:fowler-1999 | M. Fowler, Refactoring: Improving the Design of Existing Code, Addison-Wesley 1999; automatic unit tests should be set up before refactoring | 1999 | year | wiki-refactoring | 2026-11-20 |
| b3:feathers-characterization | characterization test, describing the actual behaviour of existing (legacy) code to protect it against unintended changes; term coined by Michael Feathers (Working Effectively with Legacy Code) | -- | -- | wiki-characterization-test | 2026-11-20 |
| b3:technical-debt | Ward Cunningham coined the term technical debt in 1992 | 1992 | year | wiki-technical-debt | 2026-11-20 |
| b3:ci-booch | Grady Booch first proposed the term continuous integration in 1991; CI builds and tests the system automatically, often on each commit | 1991 | year | wiki-ci | 2026-11-20 |
| b3:test-doubles | Meszaros (xUnit Test Patterns, 2007) classifies test doubles: stub (provides static input), mock, spy, fake, dummy | 2007 | year | wiki-test-double | 2026-11-20 |
| b3:tooling-docs | sys.monitoring added in Python 3.12 (LINE and BRANCH events, DISABLE); hypothesis settings.derandomize seeds the generator from a hash of the test function so every run tests the same cases; git pre-commit hook runs before a commit and a non-zero exit aborts it, bypassed with --no-verify | -- | -- | py-sys-monitoring, hypothesis-api, git-githooks | 2026-11-20 |
| b3:sketchpad-1963 | Sketchpad, the interactive drawing program written by Ivan Sutherland in 1963 | 1963 | year | wiki-sketchpad | 2026-11-20 |
| b3:zbuffer-1974 | the z-buffer was first described in 1974 by Wolfgang Strasser in his PhD thesis; its invention is most often attributed to Edwin Catmull, also 1974 | 1974 | year | wiki-zbuffer | 2026-11-20 |
| b3:gouraud-1971 | H. Gouraud, Continuous shading of curved surfaces, IEEE Transactions on Computers C-20(6) 623--629: lighting computed at the vertices and interpolated linearly across each triangle | June 1971 | date | crossref, wiki-gouraud | 2026-11-20 |
| b3:phong-1975 | Bui Tuong Phong, Illumination for computer generated pictures, Communications of the ACM 18(6) 311--317 | June 1975 | date | crossref, wiki-phong | 2026-11-20 |
| b3:whitted-1980 | T. Whitted, An improved illumination model for shaded display, Communications of the ACM 23(6) 343--349; first recursive ray tracing for mirror reflection and refraction | June 1980 | date | crossref, wiki-ray-tracing | 2026-11-20 |
| b3:pineda-1988 | J. Pineda, A parallel algorithm for polygon rasterization, SIGGRAPH 1988, 17--20 (edge functions) | 1988 | year | crossref | 2026-11-20 |
| b3:bresenham-1965 | J. E. Bresenham, Algorithm for computer control of a digital plotter, IBM Systems Journal 4(1) 25--30 | 1965 | year | crossref | 2026-11-20 |
| b3:pick-1899 | Pick's theorem: a simple polygon with integer vertices has area A = i + b/2 - 1 (i interior, b boundary lattice points); Georg Pick, 1899 | 1899 | year | wiki-pick | 2026-11-20 |
| b3:ppm-png | PPM: magic number P6, whitespace, width, height, maxval in ASCII decimal, then the pixels; PNG: 8-byte signature 89 50 4E 47 0D 0A 1A 0A, chunks of length, type, data and a CRC computed over type and data, IHDR first, IEND last | -- | -- | netpbm-ppm, w3c-png3 | 2026-11-20 |
| b3:raft-persist | Raft's persistent state (currentTerm, votedFor, log[]) is updated on stable storage before responding to RPCs | -- | rule | raft-paper | 2026-11-20 |
| b3:raft-noop | each Raft leader commits a blank no-op entry at the start of its term, to learn which entries are committed | -- | rule | raft-paper | 2026-11-20 |
| b3:raft-reads | before a read-only request a Raft leader must check it has not been deposed: it exchanges heartbeats with a majority first; a lease based on heartbeats instead relies on bounded clock skew | -- | rule | raft-paper | 2026-11-20 |
| b3:raft-timeouts | Raft's election timeouts are chosen at random from a fixed interval, e.g. 150--300 ms, so that split votes are rare | 150--300 ms | rule | raft-paper | 2026-11-20 |
| b3:rust-sync-all | File::sync_all attempts to sync all OS-internal file content and metadata to disk before returning | -- | rule | rust-file | 2026-11-20 |
