# Data ledger --- Book 4

Book 4's own rows. Shared rows and the rules are in `sources/data_ledger.md`.
Owned by the Book 4 writer; other books may cite these rows read-only.

## Sources

| key | source | URL |
|---|---|---|
| RISCV-OPCODES | RISC-V International, riscv-opcodes: machine-readable encoding tables (extensions/rv_i, rv32_i, rv_m) | https://github.com/riscv/riscv-opcodes |
| RISCV-ISA-SRC | The RISC-V Instruction Set Manual, Volume I, source of the RV32I and M chapters (src/unpriv/rv32.adoc, m-st-ext.adoc) and its tags | https://github.com/riscv/riscv-isa-manual |
| RISCV-PSABI | RISC-V ELF psABI, calling convention (riscv-cc.adoc) | https://github.com/riscv-non-isa/riscv-elf-psabi-doc |
| RISCV-ASM | RISC-V Assembly Programmer's Manual (src/asm-manual.adoc) | https://github.com/riscv-non-isa/riscv-asm-manual |
| RARS | RARS, the RISC-V Assembler and Runtime Simulator: system-call numbers (src/Syscall.properties) | https://github.com/TheThirdOne/rars |
| LINUX-UNISTD | Linux kernel, include/uapi/asm-generic/unistd.h (system-call numbers of the generic table, used by RISC-V) | https://github.com/torvalds/linux |
| STROUSTRUP-FAQ | B. Stroustrup, Bjarne Stroustrup's FAQ (``When was C++ invented?'') | https://www.stroustrup.com/bs_faq.html |
| CROSSREF | Crossref REST API, bibliographic metadata registered for a DOI (title, authors, venue, date) | https://api.crossref.org/works/ |
| NASA-MCO | NASA, Mars Climate Orbiter Mishap Investigation Board, Phase I Report, November 10, 1999 (NASA Lessons Learned library) | https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf |
| X86-64-PSABI | System V Application Binary Interface, AMD64 Architecture Processor Supplement (x86-64 psABI), low-level system information (low-level-sys-info.tex) | https://gitlab.com/x86-psABIs/x86-64-ABI |
| RISCV-ABOUT | RISC-V International, About RISC-V (history) | https://riscv.org/about/ |
| WILKES-1965 | M. V. Wilkes, Slave Memories and Dynamic Storage Allocation, IEEE Transactions on Electronic Computers EC-14(2), April 1965, pp. 270-271 | https://doi.org/10.1109/PGEC.1965.264263 |
| LIPTAY-1968 | J. S. Liptay, Structural aspects of the System/360 Model 85, II: The cache, IBM Systems Journal 7(1), 1968, pp. 15-21 | https://doi.org/10.1147/sj.71.0015 |
| POSIX-FORK | The Open Group Base Specifications Issue 8 (POSIX.1-2024), fork | https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html |
| POSIX-WAIT | The Open Group Base Specifications Issue 8 (POSIX.1-2024), wait, waitpid | https://pubs.opengroup.org/onlinepubs/9799919799/functions/waitpid.html |
| POSIX-EXEC | The Open Group Base Specifications Issue 8 (POSIX.1-2024), exec | https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html |
| MAN-PROC-STATUS | Linux man-pages, proc_pid_status(5) | https://man7.org/linux/man-pages/man5/proc_pid_status.5.html |
| MAN-SIGNAL | Linux man-pages, signal(7) | https://man7.org/linux/man-pages/man7/signal.7.html |
| MAN-PIPE | Linux man-pages, pipe(7) | https://man7.org/linux/man-pages/man7/pipe.7.html |
| MAN-SIGNAL-SAFETY | Linux man-pages, signal-safety(7) | https://man7.org/linux/man-pages/man7/signal-safety.7.html |
| CROSSREF-PETERSON | Crossref metadata of G. L. Peterson, Myths about the mutual exclusion problem, Information Processing Letters 12(3), 1981, pp. 115-116, doi 10.1016/0020-0190(81)90106-X | https://api.crossref.org/works/10.1016/0020-0190(81)90106-X |
| CROSSREF-LAMPORT-BAKERY | Crossref metadata of L. Lamport, A new solution of Dijkstra's concurrent programming problem, Communications of the ACM 17(8), 1974, pp. 453-455, doi 10.1145/361082.361093 | https://api.crossref.org/works/10.1145/361082.361093 |
| EWD123-B4 | E. W. Dijkstra Archive, transcription of EWD 123, Cooperating sequential processes | https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html |
| EWD-INDEX-01 | E. W. Dijkstra Archive, index of EWD 100-199 (heading: 1964-67) | https://www.cs.utexas.edu/~EWD/index01xx.html |
| EWD310-B4 | E. W. Dijkstra Archive, transcription of EWD 310, Hierarchical ordering of sequential processes | https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD310.html |
| EWD-INDEX-03 | E. W. Dijkstra Archive, index of EWD 300-399 (heading: 1971-73) | https://www.cs.utexas.edu/~EWD/index03xx.html |
| CPPREF-SEMAPHORE | cppreference, std::counting_semaphore, std::binary_semaphore | https://en.cppreference.com/w/cpp/thread/counting_semaphore |
| RFC6890 | RFC 6890 (BCP 153), Special-Purpose IP Address Registries, April 2013 | https://www.rfc-editor.org/rfc/rfc6890.html |
| RFC791 | RFC 791, Internet Protocol, September 1981 | https://www.rfc-editor.org/rfc/rfc791.html |
| KERNEL-IP-SYSCTL | Linux kernel documentation, IP Sysctl | https://docs.kernel.org/networking/ip-sysctl.html |
| MAN-SOCKET | Linux man-pages, socket(7) | https://man7.org/linux/man-pages/man7/socket.7.html |
| RFC1662 | RFC 1662, PPP in HDLC-like Framing, July 1994 | https://www.rfc-editor.org/rfc/rfc1662.html |
| RFC1071 | RFC 1071, Computing the Internet Checksum, September 1988 | https://www.rfc-editor.org/rfc/rfc1071.html |
| RFC826 | RFC 826, An Ethernet Address Resolution Protocol, November 1982 | https://www.rfc-editor.org/rfc/rfc826.html |
| RFC7042 | RFC 7042 (BCP 141), IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters, October 2013 | https://www.rfc-editor.org/rfc/rfc7042.html |
| RFC894 | RFC 894, A Standard for the Transmission of IP Datagrams over Ethernet Networks, April 1984 | https://www.rfc-editor.org/rfc/rfc894.html |
| RFC1952 | RFC 1952, GZIP file format specification version 4.3, May 1996 | https://www.rfc-editor.org/rfc/rfc1952.html |
| RFC3385 | RFC 3385, iSCSI CRC/Checksum Considerations, September 2002 | https://www.rfc-editor.org/rfc/rfc3385.html |
| LINUX-IF-ETHER | Linux kernel, include/uapi/linux/if_ether.h (read in the installed copy, /usr/include/linux/if_ether.h) | https://github.com/torvalds/linux/blob/master/include/uapi/linux/if_ether.h |
| CROSSREF-ABRAMSON | Crossref record of N. Abramson, The ALOHA System: another alternative for computer communications, AFIPS Fall Joint Computer Conference 1970, p. 281 | https://api.crossref.org/works/10.1145/1478462.1478502 |
| RFC1918 | RFC 1918 (BCP 5), Address Allocation for Private Internets, February 1996 | https://www.rfc-editor.org/rfc/rfc1918.html |
| RFC5737 | RFC 5737, IPv4 Address Blocks Reserved for Documentation, January 2010 | https://www.rfc-editor.org/rfc/rfc5737.html |
| RFC3849 | RFC 3849, IPv6 Address Prefix Reserved for Documentation, July 2004 | https://www.rfc-editor.org/rfc/rfc3849.html |
| RFC4632 | RFC 4632, Classless Inter-domain Routing (CIDR), August 2006 | https://www.rfc-editor.org/rfc/rfc4632.html |
| RFC8200 | RFC 8200, Internet Protocol, Version 6 (IPv6) Specification, July 2017 | https://www.rfc-editor.org/rfc/rfc8200.html |
| RFC5952 | RFC 5952, A Recommendation for IPv6 Address Text Representation, August 2010 | https://www.rfc-editor.org/rfc/rfc5952.html |
| RFC3022 | RFC 3022, Traditional IP Network Address Translator (Traditional NAT), January 2001 | https://www.rfc-editor.org/rfc/rfc3022.html |
| RFC2453 | RFC 2453, RIP Version 2, November 1998 | https://www.rfc-editor.org/rfc/rfc2453.html |
| RFC2328 | RFC 2328, OSPF Version 2, April 1998 | https://www.rfc-editor.org/rfc/rfc2328.html |
| RFC4271 | RFC 4271, A Border Gateway Protocol 4 (BGP-4), January 2006 | https://www.rfc-editor.org/rfc/rfc4271.html |
| NRO-2011 | Number Resource Organization, Free Pool of IPv4 Address Space Depleted, 3 February 2011 | https://www.nro.net/ipv4-free-pool-depleted/ |
| RFC768 | RFC 768, User Datagram Protocol, 28 August 1980 | https://www.rfc-editor.org/rfc/rfc768.html |
| RFC9293 | RFC 9293, Transmission Control Protocol (TCP), August 2022 | https://www.rfc-editor.org/rfc/rfc9293.html |
| RFC6298 | RFC 6298, Computing TCP's Retransmission Timer, June 2011 | https://www.rfc-editor.org/rfc/rfc6298.html |
| RFC5681 | RFC 5681, TCP Congestion Control, September 2009 | https://www.rfc-editor.org/rfc/rfc5681.html |
| RFC6335 | RFC 6335 (BCP 165), IANA Procedures for the Management of the Service Name and Transport Protocol Port Number Registry, August 2011 | https://www.rfc-editor.org/rfc/rfc6335.html |
| RFC9000 | RFC 9000, QUIC: A UDP-Based Multiplexed and Secure Transport, May 2021 | https://www.rfc-editor.org/rfc/rfc9000.html |
| CROSSREF-MATHIS | Crossref record of M. Mathis, J. Semke, J. Mahdavi, T. Ott, The macroscopic behavior of the TCP congestion avoidance algorithm, ACM SIGCOMM Computer Communication Review 27(3), 67-82, July 1997 | https://api.crossref.org/works/10.1145/263932.264023 |
| ARXIV-JAIN | R. Jain, D. Chiu, W. Hawe, A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems, DEC Research Report TR-301, September 1984 (arXiv cs/9809099) | https://arxiv.org/abs/cs/9809099 |
| RFC1034 | RFC 1034, Domain Names - Concepts and Facilities, November 1987 | https://www.rfc-editor.org/rfc/rfc1034.html |
| RFC1035 | RFC 1035, Domain Names - Implementation and Specification, November 1987 | https://www.rfc-editor.org/rfc/rfc1035.html |
| RFC3596 | RFC 3596, DNS Extensions to Support IP Version 6, October 2003 | https://www.rfc-editor.org/rfc/rfc3596.html |
| RFC2606 | RFC 2606 (BCP 32), Reserved Top Level DNS Names, June 1999 | https://www.rfc-editor.org/rfc/rfc2606.html |
| RFC9110 | RFC 9110, HTTP Semantics, June 2022 | https://www.rfc-editor.org/rfc/rfc9110.html |
| RFC9112 | RFC 9112, HTTP/1.1, June 2022 | https://www.rfc-editor.org/rfc/rfc9112.html |
| RFC9113 | RFC 9113, HTTP/2, June 2022 | https://www.rfc-editor.org/rfc/rfc9113.html |
| RFC9114 | RFC 9114, HTTP/3, June 2022 | https://www.rfc-editor.org/rfc/rfc9114.html |
| RFC8446 | RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, August 2018 | https://www.rfc-editor.org/rfc/rfc8446.html |
| RFC5321 | RFC 5321, Simple Mail Transfer Protocol, October 2008 | https://www.rfc-editor.org/rfc/rfc5321.html |
| CROSSREF-KLEENE | Crossref record of S. C. Kleene, Representation of Events in Nerve Nets and Finite Automata, in Automata Studies (AM-34), Princeton University Press, 1956, pp. 3-42 | https://api.crossref.org/works/10.1515/9781400882618-002 |
| CROSSREF-RABIN-SCOTT | Crossref record of M. O. Rabin and D. Scott, Finite Automata and Their Decision Problems, IBM Journal of Research and Development 3(2), 114-125, April 1959 | https://api.crossref.org/works/10.1147/rd.32.0114 |
| CROSSREF-THOMPSON | Crossref record of K. Thompson, Programming Techniques: Regular expression search algorithm, Communications of the ACM 11(6), 419-422, June 1968 | https://api.crossref.org/works/10.1145/363347.363387 |
| CROSSREF-GLUSHKOV | Crossref record of V. M. Glushkov, The abstract theory of automata, Russian Mathematical Surveys 16(5), 1-53, 1961 | https://api.crossref.org/works/10.1070/RM1961v016n05ABEH004112 |
| CROSSREF-BERRY-SETHI | Crossref record of G. Berry and R. Sethi, From regular expressions to deterministic automata, Theoretical Computer Science 48, 117-126, 1986 | https://api.crossref.org/works/10.1016/0304-3975(86)90088-5 |
| CROSSREF-NERODE | Crossref record of A. Nerode, Linear automaton transformations, Proceedings of the American Mathematical Society 9(4), 541-544, August 1958 | https://api.crossref.org/works/10.1090/S0002-9939-1958-0135681-9 |
| PYTHON-RE | Python documentation, re - Regular expression operations (3.15), possessive quantifiers and atomic groups | https://docs.python.org/3/library/re.html |
| POSIX-REGEX | The Open Group Base Specifications Issue 8 (IEEE Std 1003.1-2024), Chapter 9, Regular Expressions | https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html |
| CROSSREF-CHOMSKY | Crossref record of N. Chomsky, Three models for the description of language, IRE (IEEE) Transactions on Information Theory 2(3), 113-124, September 1956 | https://api.crossref.org/works/10.1109/TIT.1956.1056813 |
| CROSSREF-ALGOL60 | Crossref record of J. W. Backus et al., ed. P. Naur, Report on the algorithmic language ALGOL 60, Communications of the ACM 3(5), 299-311, May 1960 | https://api.crossref.org/works/10.1145/367236.367262 |
| CROSSREF-YOUNGER | Crossref record of D. H. Younger, Recognition and parsing of context-free languages in time n^3, Information and Control 10(2), 189-208, February 1967 | https://api.crossref.org/works/10.1016/S0019-9958(67)80007-X |
| SEP-FREGE | Stanford Encyclopedia of Philosophy, Gottlob Frege: the Begriffsschrift (1879), his first book, a formula language of pure thought modelled upon that of arithmetic | https://plato.stanford.edu/entries/frege/ |
| CROSSREF-GENTZEN | Crossref record of G. Gentzen, Untersuchungen über das logische Schließen I, Mathematische Zeitschrift 39(1), 176-210, December 1935 | https://api.crossref.org/works/10.1007/BF01201353 |
| CROSSREF-GODEL-1930 | Crossref record of K. Gödel, Die Vollständigkeit der Axiome des logischen Funktionenkalküls, Monatshefte für Mathematik und Physik 37(1), 349-360, December 1930 | https://api.crossref.org/works/10.1007/BF01696781 |
| CROSSREF-ROBINSON | Crossref record of J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 23-41, 1965 | https://api.crossref.org/works/10.1145/321250.321253 |
| CROSSREF-APT | Crossref record of B. Aspvall, M. F. Plass, R. E. Tarjan, A linear-time algorithm for testing the truth of certain quantified boolean formulas, Information Processing Letters 8(3), 121-123, March 1979 | https://api.crossref.org/works/10.1016/0020-0190(79)90002-4 |
| LEAN-HOME | Lean home page: an open-source programming language and proof assistant; Mathlib, its community library of formalised mathematics | https://lean-lang.org/ |
| ROCQ-ABOUT | Rocq Prover, about page: formerly known as the Coq Proof Assistant | https://rocq-prover.org/about |
| CROSSREF-KMP | Crossref record of D. E. Knuth, J. H. Morris, V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 323-350, 1977 | https://api.crossref.org/works/10.1137/0206024 |
| CROSSREF-BOYER-MOORE | Crossref record of R. S. Boyer, J. S. Moore, A fast string searching algorithm, Communications of the ACM 20(10), 762-772, October 1977 | https://api.crossref.org/works/10.1145/359842.359859 |
| CROSSREF-KARP-RABIN | Crossref record of R. M. Karp, M. O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2), 249-260, March 1987 | https://api.crossref.org/works/10.1147/rd.312.0249 |
| CROSSREF-WELCH | Crossref record of T. A. Welch, A technique for high-performance data compression, Computer 17(6), 8-19, June 1984 | https://api.crossref.org/works/10.1109/MC.1984.1659158 |
| CROSSREF-ZIV-LEMPEL | Crossref record of J. Ziv, A. Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 530-536, September 1978 | https://api.crossref.org/works/10.1109/TIT.1978.1055934 |
| CROSSREF-AHO-CORASICK | Crossref record of A. V. Aho, M. J. Corasick, Efficient string matching: an aid to bibliographic search, Communications of the ACM 18(6), 333-340, June 1975 | https://api.crossref.org/works/10.1145/360825.360855 |
| RFC-1951 | RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, May 1996: compresses data using a combination of the LZ77 algorithm and Huffman coding | https://www.rfc-editor.org/rfc/rfc1951 |
| CROSSREF-FORD-FULKERSON | Crossref record of L. R. Ford Jr., D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399-404, 1956 | https://api.crossref.org/works/10.4153/CJM-1956-045-5 |
| CROSSREF-EDMONDS-KARP | Crossref record of J. Edmonds, R. M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248-264, April 1972 | https://api.crossref.org/works/10.1145/321694.321699 |
| CROSSREF-HALL | Crossref record of P. Hall, On representatives of subsets, Journal of the London Mathematical Society s1-10, 26-30, 1935 | https://api.crossref.org/works/10.1112/jlms/s1-10.37.26 |
| CROSSREF-MENGER | Crossref record of K. Menger, Zur allgemeinen Kurventheorie, Fundamenta Mathematicae 10, 96-115, 1927 | https://api.crossref.org/works/10.4064/fm-10-1-96-115 |
| WIKI-KONIG | Wikipedia, Kőnig's theorem (graph theory): proved by Dénes Kőnig (1931); discovered independently, also in 1931, by Jenő Egerváry for weighted graphs | https://en.wikipedia.org/wiki/K%C5%91nig%27s_theorem_(graph_theory) |
| CROSSREF-HOARE-1961 | Crossref record of C. A. R. Hoare, Algorithm 64: Quicksort, Communications of the ACM 4(7), 321, July 1961 | https://api.crossref.org/works/10.1145/366622.366644 |
| CROSSREF-CARTER-WEGMAN | Crossref record of J. L. Carter, M. N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 143-154, April 1979 | https://api.crossref.org/works/10.1016/0022-0000(79)90044-8 |
| CROSSREF-BLOOM | Crossref record of B. H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 422-426, July 1970 | https://api.crossref.org/works/10.1145/362686.362692 |
| CROSSREF-MILLER-1976 | Crossref record of G. L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13(3), 300-317, December 1976 | https://api.crossref.org/works/10.1016/S0022-0000(76)80043-8 |
| CROSSREF-RABIN-1980 | Crossref record of M. O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12(1), 128-138, February 1980 | https://api.crossref.org/works/10.1016/0022-314X(80)90084-0 |
| WIKI-KARGER | Wikipedia, Karger's algorithm: invented by David Karger and first published in 1993 (Global min-cuts in RNC and other ramifications of a simple mincut algorithm, Proc. 4th ACM-SIAM SODA) | https://en.wikipedia.org/wiki/Karger%27s_algorithm |
| CROSSREF-HNR-1968 | Crossref record of P. Hart, N. Nilsson, B. Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2), 100-107, 1968 | https://api.crossref.org/works/10.1109/TSSC.1968.300136 |
| CROSSREF-VON-NEUMANN-1928 | Crossref record of J. v. Neumann, Zur Theorie der Gesellschaftsspiele, Mathematische Annalen 100, 295-320, December 1928 | https://api.crossref.org/works/10.1007/BF01448847 |
| CROSSREF-KNUTH-MOORE | Crossref record of D. E. Knuth, R. W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4), 293-326, 1975 | https://api.crossref.org/works/10.1016/0004-3702(75)90019-3 |
| CROSSREF-QUINLAN-1986 | Crossref record of J. R. Quinlan, Induction of decision trees, Machine Learning 1(1), 81-106, March 1986 | https://api.crossref.org/works/10.1007/BF00116251 |
| CROSSREF-LLOYD-1982 | Crossref record of S. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 129-137, March 1982 | https://api.crossref.org/works/10.1109/TIT.1982.1056489 |
| WIKI-LLOYD | Wikipedia, Lloyd's algorithm: first proposed by Stuart P. Lloyd of Bell Labs in 1957 for pulse-code modulation; unpublished until 1982 | https://en.wikipedia.org/wiki/Lloyd%27s_algorithm |
| CROSSREF-BENTLEY-1975 | Crossref record of J. L. Bentley, Multidimensional binary search trees used for associative searching, Communications of the ACM 18(9), 509-517, September 1975 | https://api.crossref.org/works/10.1145/361002.361007 |
| SQLITE-ISOLATION | SQLite documentation, Isolation in SQLite: transactions are serializable except with shared cache and read_uncommitted, which is the only way to see another connection's uncommitted changes; a single writer at a time | https://www.sqlite.org/isolation.html |
| SQLITE-TRANSACTION | SQLite documentation, BEGIN TRANSACTION: DEFERRED, IMMEDIATE (starts a write at once; may fail with SQLITE_BUSY if another write transaction is active), EXCLUSIVE | https://www.sqlite.org/lang_transaction.html |
| SQLITE-EQP | SQLite documentation, EXPLAIN QUERY PLAN: SCAN is a full-table scan, SEARCH visits a subset of rows; output format may change between releases | https://www.sqlite.org/eqp.html |
| PG-ISOLATION | PostgreSQL documentation, Transaction Isolation: the four standard levels and the phenomena each allows (Table 13.1); PostgreSQL Read Uncommitted behaves like Read Committed, its Repeatable Read allows no phantoms | https://www.postgresql.org/docs/current/transaction-iso.html |
| CROSSREF-CODD-1970 | Crossref record of E. F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377-387, June 1970 | https://api.crossref.org/works/10.1145/362384.362685 |
| WIKI-3NF | Wikipedia, Third normal form: defined in Codd's paper Further Normalization of the Data Base Relational Model, 1971 | https://en.wikipedia.org/wiki/Third_normal_form |
| WIKI-BCNF | Wikipedia, Boyce-Codd normal form: formally developed in 1974 by Raymond F. Boyce and Edgar F. Codd; first described by Ian Heath in 1971 | https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form |
| CROSSREF-HAERDER-REUTER | Crossref record of T. Haerder, A. Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 287-317, December 1983 | https://api.crossref.org/works/10.1145/289.291 |
| WIKI-ACID | Wikipedia, ACID: in 1983 Andreas Reuter and Theo Haerder coined the acronym ACID | https://en.wikipedia.org/wiki/ACID |

## Rows

| id | quantity | value | unit | source | accessed |
|---|---|---|---|---|---|
| b2:rv-encodings | opcode, funct3 and funct7 of every RV32I and RV32M instruction used by rv | as in `code/shared/rv/rv/isa.py` (SPEC table) | --- | RISCV-OPCODES | 2026-11-20 |
| b2:rv-formats | base instruction formats | R, I, S, U, with B and J as variants of S and U (immediate bits rearranged) | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-x0 | register x0 | hardwired to 0 | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-div | division rules (M) | div/rem round toward zero; by zero: quotient all bits set (divu 2^32-1, div -1), remainder = dividend; -2^31 / -1: quotient -2^31, remainder 0; no trap | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-misaligned-jump | misaligned branch or jump target | instruction-address-misaligned exception on a taken branch or jump, reported on that instruction; none when not taken | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-misaligned-ldst | misaligned loads and stores | execution-environment dependent: handled invisibly, or an address-misaligned or access-fault exception | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-endian | byte order of memory | defined by the execution environment (little-endian or big-endian) | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-lui | lui | load upper immediate, U-type, builds 32-bit constants with an addi | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-isa-tags | dated releases of the unprivileged manual | tags 20240411 and 20250508 (latest dated tag on the access date; draft builds continue) | --- | RISCV-ISA-SRC | 2026-11-20 |
| b2:rv-abi-names | ABI register names | x0 zero, x1 ra (return address), x2 sp (stack pointer), x3 gp, x4 tp, x5-7 t0-2, x8 s0/fp, x9 s1, x10-17 a0-7, x18-27 s2-11, x28-31 t3-6 | --- | RISCV-PSABI | 2026-11-20 |
| b2:rv-sp-align | stack | grows downwards; sp aligned to 128 bits (16 bytes) on procedure entry | --- | RISCV-PSABI | 2026-11-20 |
| b2:rv-call-tail | call and tail pseudo-instructions | expand to auipc + jalr (call saves the return address in ra; tail uses t1, or t2 with Zicfilp, as scratch) | --- | RISCV-ASM | 2026-11-20 |
| b2:rv-ecalls | RARS system-call numbers | PrintInt 1, PrintString 4, ReadInt 5, Sbrk 9, Exit 10, PrintChar 11, Exit2 93 | --- | RARS | 2026-11-20 |
| b2:linux-exit-93 | Linux system-call number of exit (generic table) | 93 | --- | LINUX-UNISTD | 2026-11-20 |
| b2:cwc-1979 | start of the work that became C++ | 1979, first called ``C with Classes''; first used inside AT&T in August 1983; the name C++ late 1983 | --- | STROUSTRUP-FAQ | 2026-11-20 |
| b2:cpp20-published | the C++20 standard (page cpp/language/history and cpp/20) | published December 2020; final draft N4860 of 2020-03-31 | --- | CPPREF | 2026-11-20 |
| b2:cpp-dtor-order | destruction of members and bases (page cpp/language/destructor) | members in reverse order of declaration, then bases in reverse order of construction | --- | CPPREF | 2026-11-20 |
| b2:cpp-noexcept-terminate | an exception leaving a non-throwing function (page cpp/language/noexcept_spec) | std::terminate is called; destructors are non-throwing unless a member's or base's destructor may throw | --- | CPPREF | 2026-11-20 |
| b2:cpp-logic-error | standard exception categories (page cpp/error/logic_error) | logic_error: invalid_argument, domain_error, length_error, out_of_range; runtime_error: range_error, overflow_error, underflow_error | --- | CPPREF | 2026-11-20 |
| b2:cpp11-move | language and library features of C++11 (page cpp/11) | rvalue references, move constructors and move assignment operators, defaulted and deleted functions; std::unique_ptr | --- | CPPREF | 2026-11-20 |
| b2:cpp17-elision | copy elision (page cpp/language/copy_elision) | since C++17 a prvalue is constructed directly in the storage of its final destination (guaranteed copy elision); the elision of a named local in a return statement (NRVO) stays permitted, not required | --- | CPPREF | 2026-11-20 |
| b2:vector-nothrow-move | std::vector::push_back (page cpp/container/vector/push_back) | amortised constant; strong guarantee if an exception is thrown; if the move constructor of T is not noexcept and T is copy-insertable, the vector copies when it grows; otherwise the guarantee is waived | --- | CPPREF | 2026-11-20 |
| b2:simula-oop | origin of object-oriented programming (FAQ ``What is object-oriented programming?'' and ``Why did you invent C++?'') | a style originating with Simula, relying on encapsulation, inheritance and polymorphism; C++ was made to write systems programs in the styles encouraged by Simula67 | --- | STROUSTRUP-FAQ | 2026-11-20 |
| b2:simula-hopl | history of Simula by its designers (DOI 10.1145/800025.808391) | Kristen Nygaard and Ole-Johan Dahl, ``The development of the SIMULA languages'', first History of Programming Languages conference, 1978 | --- | CROSSREF | 2026-11-20 |
| b2:lsp-1987 | the substitution principle's first statement (DOI 10.1145/62138.62141) | Barbara Liskov, keynote address ``Data abstraction and hierarchy'', OOPSLA '87 (addendum to the proceedings), 1987 | --- | CROSSREF | 2026-11-20 |
| b2:lsp-1994 | the principle as a definition of subtyping (DOI 10.1145/197320.197383) | Barbara Liskov and Jeannette Wing, ``A behavioral notion of subtyping'', ACM Transactions on Programming Languages and Systems 16(6), November 1994 | --- | CROSSREF | 2026-11-20 |
| b2:cpp20-concepts | constraints and concepts (page cpp/language/constraints) | concepts and requires-clauses are a C++20 feature | --- | CPPREF | 2026-11-20 |
| b2:qsort-c89 | the C qsort function (page c/algorithm/qsort) | in the C standard since C89/C90 (section 4.10.5.2), now 7.22.5.2; neither C nor POSIX requires quicksort, a complexity or stability | --- | CPPREF | 2026-11-20 |
| b2:std-sort-complexity | std::sort (page cpp/algorithm/sort) | O(N log N) comparisons; required in the worst case since C++11 (LWG 713; before, on average only); usually introsort | --- | CPPREF | 2026-11-20 |
| b2:lower-bound-comparisons | std::lower_bound (page cpp/algorithm/lower_bound) | at most log2(N) + O(1) comparisons, N = distance(first, last); std::ranges::lower_bound is C++20 | --- | CPPREF | 2026-11-20 |
| b2:map-complexity | std::map (page cpp/container/map) | search, removal and insertion have logarithmic complexity; maps are usually implemented as red-black trees | --- | CPPREF | 2026-11-20 |
| b2:unordered-complexity | std::unordered_map (page cpp/container/unordered_map) and the container library overview (page cpp/container) | search, insertion and removal average constant time, O(n) worst case; elements organised into buckets by the hash of the key; insertion invalidates iterators only if it causes a rehash; references and pointers to elements are invalidated only by erasing the element | --- | CPPREF | 2026-11-20 |
| b2:unordered-max-load | unordered_map::max_load_factor (page cpp/container/unordered_map/max_load_factor) | the container automatically increases the number of buckets when the load factor exceeds the maximum load factor | --- | CPPREF | 2026-11-20 |
| b2:vector-insert | std::vector::insert (page cpp/container/vector/insert) | constant plus linear in the distance between pos and the end; if the new size exceeds the old capacity, all iterators and references are invalidated, otherwise only those before the insertion point remain valid | --- | CPPREF | 2026-11-20 |
| b2:rust-2021 | the Rust 2021 edition (page edition-guide/rust-2021) | released with Rust 1.56.0, announced 2021-10-21 | --- | RUST-REF | 2026-11-20 |
| b2:rustbelt-2018 | DOI 10.1145/3158154 | R. Jung, J.-H. Jourdan, R. Krebbers, D. Dreyer, RustBelt: securing the foundations of the Rust programming language, Proceedings of the ACM on Programming Languages 2 (POPL), January 2018, pp. 1-34; abstract: the first formal and machine-checked safety proof for a language representing a realistic subset of Rust, extensible to libraries that use unsafe features, applied to several widely used ones | --- | CROSSREF | 2026-11-20 |
| b2:option-npo | module std::option, section Representation (page std/option) | Rust guarantees that Option<T> has the same size, alignment and call ABI as T for T = Box<U>, &U, &mut U (U: Sized), fn pointers, NonZero integers, NonNull<U> and repr(transparent) wrappers of these; None is then the all-zero bit pattern; called the null pointer optimization | --- | RUST-REF | 2026-11-20 |
| b2:mco-units | Mars Climate Orbiter root cause: the ground file of thruster impulse data (SM_FORCES output, AMD file) was in pound-force seconds where the interface specification required newton-seconds, so the small-forces velocity changes were low by a factor 4.45 | 4.45 | lbf to N | NASA-MCO | 2026-11-20 |
| b2:mco-loss | Mars Climate Orbiter: signal last seen 09:04:52 UTC on 23 September 1999, during Mars orbit insertion; reconstructed periapsis 57 km, judged too low for survival | 57 | km | NASA-MCO | 2026-11-20 |
| b2:rv-cc-saved | integer registers preserved across calls (callee-saved) and not (caller-saved) | preserved: sp, s0-s11; not preserved: ra, t0-t6, a0-a7; zero immutable; gp, tp unallocatable | --- | RISCV-PSABI | 2026-11-20 |
| b2:rv-cc-args | integer argument and return registers | eight argument registers a0-a7, the first two (a0, a1) also return values | --- | RISCV-PSABI | 2026-11-20 |
| b2:x86-64-args | x86-64 System V integer argument and return registers | arguments in rdi, rsi, rdx, rcx, r8, r9 (in this order); return in rax (then rdx); callee-saved rbx, rbp, r12-r15 | --- | X86-64-PSABI | 2026-11-20 |
| b2:rv-origin | RISC-V began as an instruction-set research project in May 2010; foundation 2015; RISC-V International incorporated March 2020 | 2010 | year | RISCV-ABOUT | 2026-11-20 |
| b2:cache-wilkes | a small fast "slave memory" holding copies of words of the main memory proposed in a two-page paper, April 1965 | 1965 | year | WILKES-1965 | 2026-11-20 |
| b2:cache-360-85 | the buffer memory of the IBM System/360 Model 85 described under the name "cache" | 1968 | year | LIPTAY-1968 | 2026-11-20 |
| b2:fork-returns | fork returns 0 to the child and the child's process ID to the parent; both continue from fork; the child is a copy of the parent except as listed (unique process ID, ...) ; -1 and no child on failure | 0 / pid / -1 | --- | POSIX-FORK | 2026-11-20 |
| b2:waitpid-macros | WIFEXITED non-zero for a child that terminated normally, WEXITSTATUS its low 8 bits of the exit status; WIFSIGNALED for a child terminated by an uncaught signal, WTERMSIG the signal number | --- | --- | POSIX-WAIT | 2026-11-20 |
| b2:exec-no-return | an exec function replaces the current process image with a new one; if it returns, an error occurred, it returns -1 and sets errno; argv and envp end with a null pointer | -1 | --- | POSIX-EXEC | 2026-11-20 |
| b2:proc-state-z | /proc/<pid>/status State field: the process's state, among them Z (zombie) | Z | --- | MAN-PROC-STATUS | 2026-11-20 |
| b2:signal-numbers | Linux x86 signal numbers and default actions: SIGHUP 1 Term, SIGINT 2 Term, SIGKILL 9 Term, SIGSEGV 11 Core, SIGPIPE 13 Term, SIGALRM 14 Term, SIGTERM 15 Term, SIGCHLD 17 Ign | --- | --- | MAN-SIGNAL | 2026-11-20 |
| b2:sigkill-sigstop | SIGKILL and SIGSTOP cannot be caught, blocked or ignored | --- | --- | MAN-SIGNAL | 2026-11-20 |
| b2:pipe-capacity | Linux pipe capacity since 2.6.11: 16 pages, 65 536 bytes with 4096-byte pages | 65536 | byte | MAN-PIPE | 2026-11-20 |
| b2:pipe-buf | writes of less than PIPE_BUF bytes are atomic (POSIX); PIPE_BUF is 4096 on Linux | 4096 | byte | MAN-PIPE | 2026-11-20 |
| b2:pipe-eof-sigpipe | read on a pipe whose write ends are all closed returns 0 (end of file); write to a pipe whose read ends are all closed raises SIGPIPE, or fails with EPIPE if it is ignored | --- | --- | MAN-PIPE | 2026-11-20 |
| b2:async-signal-safe | an async-signal-safe function is one that can be safely called from within a signal handler | --- | --- | MAN-SIGNAL-SAFETY | 2026-11-20 |
| b2:peterson-1981 | G. L. Peterson, Myths about the mutual exclusion problem, Information Processing Letters 12(3), pp. 115-116, June 1981 | 1981 | year | CROSSREF-PETERSON | 2026-11-20 |
| b2:lamport-bakery-1974 | L. Lamport, A new solution of Dijkstra's concurrent programming problem, Communications of the ACM 17(8), pp. 453-455, August 1974 | 1974 | year | CROSSREF-LAMPORT-BAKERY | 2026-11-20 |
| b2:ewd123-semaphores | EWD 123 section 3.2 introduces semaphores with the operations P (decrease by 1 as soon as the result would be non-negative) and V (increase by 1, indivisibly); section 2.1 gives Dekker's solution for two processes, the first correct one | P, V | rule | EWD123-B4 | 2026-11-20 |
| b2:ewd123-period | EWD 123 belongs to the archive's EWD 100-199 range, headed 1964-67 | 1964-67 | year | EWD-INDEX-01 | 2026-11-20 |
| b2:ewd310-philosophers | EWD 310 poses the five dining philosophers (forks between plates, two forks to eat); the naive solution, left fork then right, is rejected: if all five take their left fork, the group is stuck | 5 | philosophers | EWD310-B4 | 2026-11-20 |
| b2:ewd310-period | EWD 310 belongs to the archive's EWD 300-399 range, headed 1971-73 | 1971-73 | year | EWD-INDEX-03 | 2026-11-20 |
| b2:cpp-counting-semaphore | std::counting_semaphore and std::binary_semaphore (= counting_semaphore<1>) exist since C++20; acquire decrements or blocks, release increments and unblocks | C++20 | standard | CPPREF-SEMAPHORE | 2026-11-20 |
| b2:loopback-block | 127.0.0.0/8 is the special-purpose block named Loopback (RFC 1122 section 3.2.1.3); not valid as a destination or forwardable address on a network | 127.0.0.0/8 | block | RFC6890 | 2026-11-20 |
| b2:network-byte-order | when a multi-octet quantity is transmitted, the most significant octet is transmitted first (network byte order is big-endian) | --- | --- | RFC791 | 2026-11-20 |
| b2:ephemeral-range | Linux ip_local_port_range, the local ports TCP and UDP choose from, defaults to 32768 to 60999 | 32768-60999 | port | KERNEL-IP-SYSCTL | 2026-11-20 |
| b2:so-reuseaddr | with SO_REUSEADDR an AF_INET socket may bind a local address unless an active listening socket is bound to it | --- | --- | MAN-SOCKET | 2026-11-20 |
| b2:ppp-flag | PPP frames are delimited by the flag byte 0x7e; a 0x7e or 0x7d inside is sent as the escape 0x7d followed by the byte XOR 0x20 | 0x7e, 0x7d, 0x20 | byte | RFC1662 | 2026-11-20 |
| b2:crc16-ccitt | the 16-bit frame check sequence of PPP uses the generator x^16 + x^12 + x^5 + 1 | 0x1021 | polynomial | RFC1662 | 2026-11-20 |
| b2:inet-checksum | the Internet checksum is the one's complement of the one's complement sum of the 16-bit words, carries added back at the low end | --- | --- | RFC1071 | 2026-11-20 |
| b2:arp-fields | ARP packet: hardware type (Ethernet 1), protocol type, address lengths 6 and 4 for Ethernet and IPv4, opcode request 1 and reply 2, sender and target addresses | 1, 2 | opcode | RFC826 | 2026-11-20 |
| b2:ethertypes | EtherType values: IPv4 0x0800, ARP 0x0806, IPv6 0x86DD; an EtherType is 2 octets after the destination and source addresses | 0x0800, 0x0806, 0x86DD | --- | RFC7042 | 2026-11-20 |
| b2:mac-bits | a MAC address is 6 octets (3-octet OUI plus 3); in its first octet, bit 0x01 marks a group address and bit 0x02 a locally administered one | 6 | octet | RFC7042 | 2026-11-20 |
| b2:ethernet-payload | the data field of an Ethernet frame carrying IP is at least 46 and at most 1500 octets | 46-1500 | octet | RFC894 | 2026-11-20 |
| b2:ethernet-header | Ethernet header 14 octets (addresses 6 + 6, type 2), frame check sequence 4 octets, minimum frame without FCS 60 octets | 14, 4, 60 | octet | LINUX-IF-ETHER | 2026-11-20 |
| b2:crc32-gzip | the CRC-32 of gzip follows ISO 3309 and ITU-T V.42; its sample code uses the reflected constant 0xedb88320 with pre- and post-complement | 0xedb88320 | --- | RFC1952 | 2026-11-20 |
| b2:crc32-ieee | the IEEE 802 CRC-32 generator is 0x104C11DB7 as a bit vector, x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1 | 0x104C11DB7 | polynomial | RFC3385 | 2026-11-20 |
| b2:aloha-1970 | N. Abramson's paper on the ALOHA System appeared in the proceedings of the 1970 Fall Joint Computer Conference | 1970 | year | CROSSREF-ABRAMSON | 2026-11-20 |
| b2:ipv4-header | IPv4 header fields and widths: version 4, IHL 4, type of service 8, total length 16, identification 16, flags 3, fragment offset 13, time to live 8, protocol 8, header checksum 16, source 32, destination 32 bits, then options | 20 | octet | RFC791 | 2026-11-20 |
| b2:ipv4-frag-offset | the fragment offset is measured in units of 8 octets; flag DF 1 = don't fragment, MF 1 = more fragments | 8 | octet | RFC791 | 2026-11-20 |
| b2:ipv4-checksum | the header checksum is the one's complement of the one's complement sum of the header's 16-bit words, the field taken as zero; recomputed wherever the header is processed | --- | --- | RFC791 | 2026-11-20 |
| b2:ipv4-ttl-zero | a datagram whose time to live reaches zero must be destroyed | 0 | --- | RFC791 | 2026-11-20 |
| b2:ipv4-576 | every host must accept datagrams of up to 576 octets, whole or in fragments | 576 | octet | RFC791 | 2026-11-20 |
| b2:private-blocks | private address blocks 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 | 3 | block | RFC1918 | 2026-11-20 |
| b2:doc-ipv4 | IPv4 documentation blocks 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 | 3 | block | RFC5737 | 2026-11-20 |
| b2:doc-ipv6 | IPv6 documentation prefix 2001:db8::/32 | 32 | bit | RFC3849 | 2026-11-20 |
| b2:cidr-longest-match | CIDR prefixes are written address/length with a length from 0 to 32; forwarding in the Internet is done on a longest-match basis; providers advertise one aggregate route | --- | --- | RFC4632 | 2026-11-20 |
| b2:ipv6-header | IPv6 header: version 4, traffic class 8, flow label 20, payload length 16, next header 8, hop limit 8, source 128, destination 128 bits (40 octets); minimum link MTU 1280; only sources fragment | 40 | octet | RFC8200 | 2026-11-20 |
| b2:ipv6-text | IPv6 text form: leading zeros suppressed, :: used to the maximum on the longest run of at least two zero groups (the first on a tie), lowercase hexadecimal | --- | --- | RFC5952 | 2026-11-20 |
| b2:napt | NAPT translates many addresses and their TCP/UDP ports into one address and its ports; sessions are outbound from the private network unless statically mapped | --- | --- | RFC3022 | 2026-11-20 |
| b2:rip-infinity | RIP uses 16 as infinity; updates every 30 seconds; split horizon with poisoned reverse advertises routes back with an infinite metric; split horizon cannot stop loops of three or more routers | 16 | hop | RFC2453 | 2026-11-20 |
| b2:ospf-link-state | OSPF is a link-state protocol: each router keeps an identical database of the topology and builds a tree of shortest paths with itself as root | --- | --- | RFC2328 | 2026-11-20 |
| b2:bgp-as | BGP is an inter-autonomous-system routing protocol; an autonomous system is a set of routers under a single technical administration; AS_PATH lists the systems an update passed through, letting loops be pruned | --- | --- | RFC4271 | 2026-11-20 |
| b2:ipv4-exhaustion | on 3 February 2011 IANA allocated its last five /8 IPv4 blocks, one to each regional registry, emptying its free pool | 2011 | year | NRO-2011 | 2026-11-20 |
| b2:udp-header | UDP header: source port, destination port, length, checksum, 2 octets each (8 octets); the length counts header and data | 8 | octet | RFC768 | 2026-11-20 |
| b2:tcp-header | TCP header: ports 16 + 16, sequence number 32, acknowledgment number 32, data offset 4, reserved 4, 8 control bits (including SYN, ACK, FIN, RST), window 16, checksum 16, urgent pointer 16, options; at least 20 octets | 20 | octet | RFC9293 | 2026-11-20 |
| b2:tcp-states | TCP connection states: LISTEN, SYN-SENT, SYN-RECEIVED, ESTABLISHED, FIN-WAIT-1, FIN-WAIT-2, CLOSE-WAIT, CLOSING, LAST-ACK, TIME-WAIT, CLOSED | 11 | state | RFC9293 | 2026-11-20 |
| b2:tcp-time-wait | an actively closed connection lingers in TIME-WAIT for 2 MSL; the specification takes MSL as 2 minutes | 2 | minute | RFC9293 | 2026-11-20 |
| b2:rto-rules | RTO: initial 1 s; first sample R gives SRTT = R, RTTVAR = R/2; then RTTVAR = (1 - 1/4) RTTVAR + 1/4 abs(SRTT - R) and SRTT = (1 - 1/8) SRTT + R/8; RTO = SRTT + max(G, 4 RTTVAR), at least 1 s; doubled on each expiry | 1 | s | RFC6298 | 2026-11-20 |
| b2:congestion-control | slow start: cwnd grows by at most one segment per new ACK; congestion avoidance: about one segment per RTT; on loss ssthresh = max(FlightSize/2, 2 segments); on timeout cwnd = 1 segment; fast retransmit at 3 duplicate ACKs, then fast recovery | 3 | duplicate ACK | RFC5681 | 2026-11-20 |
| b2:port-ranges | port ranges: system ports 0-1023, user ports 1024-49151, dynamic (ephemeral) ports 49152-65535 | 49152 | port | RFC6335 | 2026-11-20 |
| b2:quic | QUIC is a secure general-purpose transport protocol with streams, low-latency connection setup and path migration; its packets are carried in UDP datagrams; standardised May 2021 | 2021 | year | RFC9000 | 2026-11-20 |
| b2:mathis-1997 | the macroscopic model of TCP congestion avoidance (throughput against loss rate) published by Mathis, Semke, Mahdavi and Ott in July 1997 | 1997 | year | CROSSREF-MATHIS | 2026-11-20 |
| b2:jain-index | Jain, Chiu and Hawe's fairness index (DEC report, September 1984) lies between 0 and 1 and does not depend on the amount of the resource | 1984 | year | ARXIV-JAIN | 2026-11-20 |
| b2:dns-zone | authoritative information is organised in zones; a resolver may work iteratively (a server refers it to another server) or ask for recursion; a record's TTL says how long it may be cached | 1987 | year | RFC1034 | 2026-11-20 |
| b2:dns-limits | a label has at most 63 octets, a name at most 255, a UDP message at most 512 | 63 | octet | RFC1035 | 2026-11-20 |
| b2:dns-header | the header has six 16-bit fields (ID; QR, Opcode, AA, TC, RD, RA, Z, RCODE; QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT) | 12 | octet | RFC1035 | 2026-11-20 |
| b2:dns-types | record types A 1, NS 2, CNAME 5, MX 15, TXT 16 | 15 | MX type | RFC1035 | 2026-11-20 |
| b2:dns-compression | a compression pointer is two octets whose first two bits are ones; the other 14 bits are an offset from the start of the message | 14 | bit | RFC1035 | 2026-11-20 |
| b2:dns-port | DNS servers use port 53 over UDP and TCP | 53 | port | RFC1035 | 2026-11-20 |
| b2:dns-aaaa | the AAAA record (type 28) holds a 128-bit IPv6 address | 28 | type | RFC3596 | 2026-11-20 |
| b2:test-tld | .test is reserved for testing DNS-related code | 1999 | year | RFC2606 | 2026-11-20 |
| b2:http-ports | default TCP port 80 for http and 443 for https | 443 | port | RFC9110 | 2026-11-20 |
| b2:http-persistent | HTTP/1.1 uses persistent connections by default; Connection: close announces a close after the response; body length from Content-Length, chunked coding (hex sizes, a last chunk of size 0) or the close of the connection | 0 | last chunk size | RFC9112 | 2026-11-20 |
| b2:http2-frame | every HTTP/2 frame starts with a 9-octet header: length 24 bits, type 8, flags 8, reserved 1, stream identifier 31; initial maximum frame size 2^14; TCP head-of-line blocking is not addressed | 9 | octet | RFC9113 | 2026-11-20 |
| b2:http3 | HTTP/3 maps HTTP over QUIC; a stream that is blocked or suffers loss does not prevent progress on other streams; June 2022 | 2022 | year | RFC9114 | 2026-11-20 |
| b2:tls13-handshake | TLS 1.3 full handshake: ClientHello; ServerHello, EncryptedExtensions, Certificate, CertificateVerify, Finished; client Finished; one round trip, with optional 0-RTT early data | 1 | round trip | RFC8446 | 2026-11-20 |
| b2:tls13-record | a record: content type 1 byte, legacy version 2, length 2 (5-byte header); at most 2^14 bytes of plaintext; the real content type is inside the encryption | 16384 | byte | RFC8446 | 2026-11-20 |
| b2:smtp | SMTP: a server listens on port 25; EHLO, MAIL FROM, RCPT TO, DATA, QUIT; replies 220, 250, 354, 221; data ends with a line holding a single period; lower MX preference values are tried first | 25 | port | RFC5321 | 2026-11-20 |
| b2:kleene-1956 | Kleene's paper on events in nerve nets and finite automata, in the collection Automata Studies | 1956 | year | CROSSREF-KLEENE | 2026-11-20 |
| b2:rabin-scott-1959 | Rabin and Scott's paper on finite automata and their decision problems (nondeterministic automata, the subset construction) | 1959 | year | CROSSREF-RABIN-SCOTT | 2026-11-20 |
| b2:thompson-1968 | Thompson's regular expression search algorithm (an expression compiled to a nondeterministic machine, simulated on all states at once) | 1968 | year | CROSSREF-THOMPSON | 2026-11-20 |
| b2:glushkov-1961 | Glushkov's survey of the abstract theory of automata, source of the position automaton | 1961 | year | CROSSREF-GLUSHKOV | 2026-11-20 |
| b2:berry-sethi-1986 | Berry and Sethi, from regular expressions to deterministic automata (first, last and follow computed on the expression) | 1986 | year | CROSSREF-BERRY-SETHI | 2026-11-20 |
| b2:nerode-1958 | Nerode's paper on linear automaton transformations, one of the two sources of the Myhill-Nerode theorem | 1958 | year | CROSSREF-NERODE | 2026-11-20 |
| b2:python-re-backtracking | Python's re engine establishes backtracking points; possessive quantifiers and atomic groups (added in 3.11) throw them away | 3.11 | version | PYTHON-RE | 2026-11-20 |
| b2:posix-ere | POSIX defines basic and extended regular expressions; when several matches start at the same point, the longest is matched | 2024 | year | POSIX-REGEX | 2026-11-20 |
| b2:chomsky-1956 | Chomsky's three models for the description of language, where phrase-structure grammars appear | 1956 | year | CROSSREF-CHOMSKY | 2026-11-20 |
| b2:algol60-report | The ALGOL 60 report, edited by Peter Naur, gives the language's syntax in the notation later called Backus-Naur form | 1960 | year | CROSSREF-ALGOL60 | 2026-11-20 |
| b2:younger-1967 | Younger, recognition and parsing of context-free languages in time n^3 (one of the sources of the CYK algorithm) | 1967 | year | CROSSREF-YOUNGER | 2026-11-20 |
| b2:frege-1879 | Frege's Begriffsschrift, a formula language for logic modelled on that of arithmetic | 1879 | year | SEP-FREGE | 2026-11-20 |
| b2:gentzen-1935 | Gentzen's investigations into logical deduction, where natural deduction and the sequent calculus appear | 1935 | year | CROSSREF-GENTZEN | 2026-11-20 |
| b2:godel-1930 | Gödel's paper on the completeness of the axioms of first-order logic | 1930 | year | CROSSREF-GODEL-1930 | 2026-11-20 |
| b2:robinson-1965 | Robinson's resolution principle, with unification, for machine-oriented logic | 1965 | year | CROSSREF-ROBINSON | 2026-11-20 |
| b2:aspvall-1979 | Aspvall, Plass and Tarjan's linear-time test of 2-CNF formulas | 1979 | year | CROSSREF-APT | 2026-11-20 |
| b2:lean | Lean, an open-source programming language and proof assistant, with the Mathlib library of formalised mathematics | 2026 | year | LEAN-HOME | 2026-11-20 |
| b2:rocq | the Rocq Prover, formerly the Coq Proof Assistant | 2026 | year | ROCQ-ABOUT | 2026-11-20 |
| b2:kmp-1977 | Knuth, Morris and Pratt, fast pattern matching in strings | 1977 | year | CROSSREF-KMP | 2026-11-20 |
| b2:boyer-moore-1977 | Boyer and Moore, a fast string searching algorithm | 1977 | year | CROSSREF-BOYER-MOORE | 2026-11-20 |
| b2:karp-rabin-1987 | Karp and Rabin, efficient randomized pattern-matching algorithms | 1987 | year | CROSSREF-KARP-RABIN | 2026-11-20 |
| b2:welch-1984 | Welch, a technique for high-performance data compression (LZW) | 1984 | year | CROSSREF-WELCH | 2026-11-20 |
| b2:ziv-lempel-1978 | Ziv and Lempel, compression of individual sequences via variable-rate coding | 1978 | year | CROSSREF-ZIV-LEMPEL | 2026-11-20 |
| b2:aho-corasick-1975 | Aho and Corasick, efficient string matching for bibliographic search (several patterns at once) | 1975 | year | CROSSREF-AHO-CORASICK | 2026-11-20 |
| b2:deflate | DEFLATE, the format zlib writes, combines LZ77 and Huffman coding | 1996 | year | RFC-1951 | 2026-11-20 |
| b2:ford-fulkerson-1956 | Ford and Fulkerson, maximal flow through a network | 1956 | year | CROSSREF-FORD-FULKERSON | 2026-11-20 |
| b2:edmonds-karp-1972 | Edmonds and Karp, shortest augmenting paths and the polynomial bound for network flow | 1972 | year | CROSSREF-EDMONDS-KARP | 2026-11-20 |
| b2:hall-1935 | Hall, on representatives of subsets (the marriage condition) | 1935 | year | CROSSREF-HALL | 2026-11-20 |
| b2:menger-1927 | Menger, the theorem on disjoint paths, in a paper on curve theory | 1927 | year | CROSSREF-MENGER | 2026-11-20 |
| b2:konig-1931 | Kőnig, maximum matching equals minimum vertex cover in bipartite graphs; Egerváry independently, weighted, the same year | 1931 | year | WIKI-KONIG | 2026-11-20 |
| b2:hoare-1961 | Hoare, Algorithm 64: Quicksort | 1961 | year | CROSSREF-HOARE-1961 | 2026-11-20 |
| b2:carter-wegman-1979 | Carter and Wegman, universal classes of hash functions | 1979 | year | CROSSREF-CARTER-WEGMAN | 2026-11-20 |
| b2:bloom-1970 | Bloom, hash coding with allowable errors (the Bloom filter) | 1970 | year | CROSSREF-BLOOM | 2026-11-20 |
| b2:miller-1976 | Miller, Riemann's hypothesis and tests for primality (the test later made probabilistic by Rabin) | 1976 | year | CROSSREF-MILLER-1976 | 2026-11-20 |
| b2:rabin-1980 | Rabin, the probabilistic primality test | 1980 | year | CROSSREF-RABIN-1980 | 2026-11-20 |
| b2:karger-1993 | Karger, the random contraction algorithm for minimum cuts | 1993 | year | WIKI-KARGER | 2026-11-20 |
| b2:hnr-1968 | Hart, Nilsson and Raphael, the heuristic determination of minimum cost paths (A*) | 1968 | year | CROSSREF-HNR-1968 | 2026-11-20 |
| b2:von-neumann-1928 | von Neumann, on the theory of games of strategy (the minimax theorem) | 1928 | year | CROSSREF-VON-NEUMANN-1928 | 2026-11-20 |
| b2:knuth-moore-1975 | Knuth and Moore, an analysis of alpha-beta pruning | 1975 | year | CROSSREF-KNUTH-MOORE | 2026-11-20 |
| b2:quinlan-1986 | Quinlan, induction of decision trees (ID3) | 1986 | year | CROSSREF-QUINLAN-1986 | 2026-11-20 |
| b2:lloyd-1957 | Lloyd first proposed the algorithm at Bell Labs, for pulse-code modulation | 1957 | year | WIKI-LLOYD | 2026-11-20 |
| b2:lloyd-1982 | Lloyd, least squares quantization in PCM, published | 1982 | year | CROSSREF-LLOYD-1982 | 2026-11-20 |
| b2:bentley-1975 | Bentley, multidimensional binary search trees (k-d trees) | 1975 | year | CROSSREF-BENTLEY-1975 | 2026-11-20 |
| b2:sqlite-serializable | SQLite transactions are serializable, except shared cache with read_uncommitted | - | text | SQLITE-ISOLATION | 2026-11-20 |
| b2:sqlite-one-writer | SQLite allows a single writer at a time | - | text | SQLITE-ISOLATION | 2026-11-20 |
| b2:sqlite-begin-immediate | BEGIN IMMEDIATE starts a write transaction at once and may fail with SQLITE_BUSY | - | text | SQLITE-TRANSACTION | 2026-11-20 |
| b2:sqlite-eqp | EXPLAIN QUERY PLAN: SCAN is a full scan, SEARCH a subset; format may change between releases | - | text | SQLITE-EQP | 2026-11-20 |
| b2:sql-isolation-levels | the standard isolation levels and the phenomena each allows | - | table | PG-ISOLATION | 2026-11-20 |
| b2:codd-1970 | Codd, a relational model of data for large shared data banks | 1970 | year | CROSSREF-CODD-1970 | 2026-11-20 |
| b2:codd-3nf-1971 | Codd defines third normal form | 1971 | year | WIKI-3NF | 2026-11-20 |
| b2:bcnf-1974 | Boyce and Codd formally develop BCNF (first described by Heath in 1971) | 1974 | year | WIKI-BCNF | 2026-11-20 |
| b2:haerder-reuter-1983 | Haerder and Reuter coin ACID in a survey of transaction recovery | 1983 | year | WIKI-ACID | 2026-11-20 |
