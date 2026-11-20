# One Computer Science Book — outline of the five books

Status: **outline written 2026-11-19; nothing is scaffolded or written yet.** The
user set the frame that day (languages, no block language, the machine before
Python, the family chapter style, the share of machine learning) and approved the
chapter list in summary form. The per-chapter descriptions below are the first
full draft and await review. Provenance of every chapter is in
`sources/outline_sources.md`.

## The series

| Book | Years (parts) | Covers | Chapters |
|---|---|---|---|
| 1 | Grades 1–9 (`grade-1` … `grade-9`) | primary and middle school: the machine, typing, files, storage, binary; then Python from grade 6, the processor, the Internet, the web, logic gates | 37 |
| 2 | Grades 10–12 (`grade-10` … `grade-12`) | the grade-10 digital science course and the two-year high-school computer science speciality: data representation, architecture, operating systems, networks, proofs and costs of algorithms, data structures, SQL, computability | 35 |
| 3 | University Year 1 (`bachelor-1`) | first year of the computer science preparatory class ∪ first-year licence: C and the machine model, tools, logic, analysis of algorithms, data structures, algorithm design, digital circuits, the relational model | 30 |
| 4 | University Year 2 (`bachelor-2`) | second year of the preparatory class ∪ second-year licence: C++, Rust, architecture, systems programming, networks, automata and grammars, algorithms II, database design | 31 |
| 5 | University Year 3 (`bachelor-3`) | third-year licence in computer science: compilers and languages, operating systems, computability and complexity, database internals, distributed systems, security | 32 |
| | | | **165** |

(The column "Covers" names the source programmes for this file only. The
printed books never name a programme, a country or a university.)

Estimated sizes: about 380, 420, 430, 450 and 470 pages, 2,150 in all. Chapters
with listings and captured output run longer than the family's 10 pages.

Rules this outline already obeys:

- **The machine first, then Python, and no block language** (user, 2026-11-19).
  Grades 1–5 print no code. They teach what a computer is, its hardware, typing
  with ten fingers, files, memory and storage (RAM, hard disk, SSD), what a
  program and an operating system are, binary, and algorithms followed by hand.
  Python starts in grade 6 and is the only programming language of Books 1–2.
- **Languages by level** (user, 2026-11-19): Python at school; **Python, C, C++,
  Rust and SQL** at university. No OCaml and no Java.
  - Grades 6–12: Python. HTML and CSS appear as markup (grade 9), SQL through
    Python's built-in engine (grade 12), and assembly only for the series' toy
    machine. JavaScript is described, never taught.
  - Year 1: C for the machine model and the data structures, Python where memory
    is not the point (algorithm design).
  - Year 2: C++ and Rust. The functional-programming and typed-data content that
    the source programmes teach in another language is taught in Rust.
  - Year 3: Rust for the compiler, C for the kernel side.
- **Real code, never pseudocode.** Every listing is included from a tested file
  and every printed output is captured from a run, with the gates of the
  artificial intelligence series (see "Conventions for the writing step").
  Programming exercises have tested solutions.
- **Family chapter style** (user, 2026-11-19): definitions, methods, theorems
  with proofs (correctness, termination, cost), examples, starred exercises and a
  weekend problem, as in the mathematics and physics books.
- **Books 1 and 2 never repeat themselves.** Every notion has one owner chapter,
  the earliest grade where it fits. A later chapter that needs it opens with a
  3–5 line *You already know* recall box and adds only what is new (ownership map
  at the end). The university books may re-found a school notion rigorously, but
  never re-teach it at the school level, and no notion is owned by two university
  books.
- **Overlaps: recall, then build.** Where *One Math Book*, *One Physics Book* or
  *One Earth and Space Sciences Book* owns a notion (the cross-series table at
  the end), that series stays the owner. A chapter here opens with a `recall`
  box that names it in prose ("as the mathematics book shows"), never with a
  `\cref`, and adds the computing angle.
- **Machine learning: three algorithm chapters** (user, 2026-11-19): k nearest
  neighbours (grade 11), search and games, and decision trees with clustering
  (Year 2). They are taught as algorithms, with their costs. The rest belongs to
  the *One Artificial Intelligence Book* series, named in prose.
- **Level guard.** No chapter uses mathematics that the same year of the
  mathematics series has not reached: the cost of halving is counted in grade 11
  and called a logarithm only in grade 12; proofs by induction start in grade 12;
  expected costs wait for the probability of Year 2.
- **Free tools, offline, on any operating system.** No account, no paid product,
  no online service. Interfaces are drawn generically in TikZ; no screenshot of a
  real product is printed.
- **Data is generated.** One invented data set family, produced by a tested
  script, recurs through the series (tables, SQL, graphs, a road network).
  Nothing is downloaded.
- **Volatile facts go in `dated` boxes** with their year: typical memory and disk
  sizes, prices, product and version names. Standards and other checkable facts
  go through a source ledger.
- **Security is taught as defence.** An attack is explained on the book's own toy
  programs and servers, on the reader's machine, never against a real system.
- **Technical content only.** No chapter on digital citizenship or screen habits.
  Safe use (passwords, backups, updates) appears as short boxes inside technical
  chapters.
- **One project chapter closes each year from grade 7, and each university
  book.** A project chapter goes from a specification to a tested program.
- Printed text never names a curriculum, a country's school system or a
  university. Provenance lives in `sources/outline_sources.md` and in source
  comments only.

Chapter slugs below are the future file names (`parts/<year>/NN-<slug>.tex`)
and label stems (`ch:<g7|b1…>:<slug>`).

---

## Book 1 — Grades 1–9

### Grade 1
1. **What Is a Computer?** — `what-is-a-computer`
   Computers around us: desktop, laptop, tablet, phone, and the hidden ones in a
   washing machine, a car or a toy; a computer is a machine that follows
   instructions; what goes in and what comes out; the parts you can see and
   touch (screen, keyboard, mouse, speakers, camera).
2. **Instructions in Order** — `instructions-in-order`
   A task as a list of steps (a recipe, getting dressed, guiding a friend across
   a grid: forward, turn left, turn right); the order matters; one precise step
   at a time; finding the wrong step and fixing it.

### Grade 2
1. **The Keyboard and the Mouse** — `keyboard-and-mouse`
   Letter keys, digit keys, the space bar, Enter, Backspace, Shift and the arrow
   keys, and what each does; sitting well and where the hands rest; the pointer:
   pointing, clicking, double-clicking, dragging; the touchpad and the touch
   screen.
2. **Using a Computer** — `using-a-computer`
   Switching on and shutting down properly; the desktop, icons and windows
   (open, close, move, resize); starting a program; saving work and finding it
   again; giving a file a good name.

### Grade 3
1. **Typing with Ten Fingers** — `typing-with-ten-fingers`
   The home row and its two marked keys; which finger strikes which key; eyes on
   the screen, not on the hands; capitals with the opposite Shift; punctuation
   and digits; accuracy before speed; words per minute. Keyboard layouts differ
   between countries: drills are given per layout.
2. **Inside the Computer** — `inside-the-computer`
   The processor carries out the instructions; the memory holds what is being
   worked on; the storage keeps files when the power is off; the motherboard
   links them; power supply or battery; heat and the fan; devices plugged in
   through ports, for input, for output or for both.
3. **Files and Folders** — `files-and-folders`
   A file holds one piece of work; kinds of file and their extensions (text,
   picture, sound, video, program); folders inside folders make a tree; the path
   to a file; copying, moving, renaming, deleting, and the bin.

### Grade 4
1. **Memory and Storage** — `memory-and-storage`
   RAM is fast and is emptied when the power goes off; storage keeps everything:
   the hard disk (spinning magnetic platters and a read head), the SSD (flash
   memory, no moving part), the USB stick and the memory card; byte, kilobyte,
   megabyte, gigabyte, terabyte, with scale comparisons (a page, a photo, a
   film); why a backup copy is kept.
2. **Programs and the Operating System** — `programs-and-operating-system`
   A program is a list of instructions written by people and stored as a file;
   applications; the operating system is the program that starts first, runs the
   others, and manages files, memory, devices and users; starting up; installing
   and updating; the main families of operating systems (`dated` box).
3. **Algorithms: Repeat and Decide** — `algorithms-repeat-and-decide`
   An algorithm is a precise method that always ends with its result; repeating
   steps a number of times, or until something happens; choosing with *if … then
   … otherwise*; following an algorithm by hand on a grid and on numbers (the
   largest card of a row).

### Grade 5
1. **Bits and Bytes: Counting in Binary** — `bits-and-bytes`
   Two states are enough: the bit; counting with two digits, using cards worth
   1, 2, 4, 8 and 16; numbers up to 31 on five bits and up to 255 on a byte; each
   extra bit doubles the number of patterns.
2. **Text, Pictures and Sound as Numbers** — `text-pictures-sound-as-numbers`
   Every character has a number (a first code table); a picture is a grid of
   pixels, each one number, or three for red, green and blue; more pixels, more
   detail, a bigger file; sound as a long list of numbers (told); everything in
   a file is bits.
3. **Networks and the Internet: A First Look** — `networks-first-look`
   Computers linked by cable or by radio form a network; the Internet is a
   network of networks; a web page is a file kept on a distant computer, a
   server; the browser, the address of a page, a link; how a search engine finds
   pages (told); a password is a key: making a strong one.

### Grade 6
1. **A First Python Program** — `first-python-program`
   A programming language is precise enough for a machine; the editor, the
   interpreter, running a file; `print`; numbers and the four operations, whole
   division and remainder; a program runs from top to bottom; reading an error
   message; comments.
2. **Variables and Input** — `variables-and-input`
   A variable is a name for a value; assignment is not equality; whole numbers,
   decimal numbers and strings; `input` and conversions; following a program by
   hand with a table of values.
3. **Repeating with `for`: Turtle Drawings** — `for-loops-turtle`
   The turtle: forward, left, right, pen up, pen down; the `for` loop repeats a
   block a known number of times; indentation marks the block; regular polygons
   and their angles; the loop variable and `range`; a loop inside a loop.
4. **Decisions: `if` and `else`** — `if-else`
   Comparisons give true or false; `if`, `else`, `elif`; `and`, `or`, `not`;
   testing every branch; a program that answers differently for different
   inputs.
5. **Repeating with `while`** — `while-loops`
   Repeating as long as a condition holds; counters and running totals; the loop
   that never ends, and how to stop it; choosing between `for` and `while`; a
   number-guessing game.

### Grade 7
1. **Functions** — `functions`
   Defining and calling a function; parameters and arguments; `return` is not
   `print`; local variables; cutting a problem into functions; checking a
   function on examples.
2. **Lists** — `lists`
   A list holds many values in order; index from 0, length; walking through a
   list; appending and removing; a sum, a largest value and a count computed by
   walking; a list is changed in place.
3. **Strings** — `strings`
   A string is a sequence of characters; index, slice, length; walking through
   text; useful methods (upper, split, join, find); the code of a character;
   counting letters and words.
4. **How a Processor Runs a Program** — `how-a-processor-runs-a-program`
   Instructions are numbers in memory; the processor fetches, decodes and
   executes them one by one, at the beat of a clock; registers and the program
   counter on the series' toy machine, traced by hand; machine language; why
   Python needs an interpreter (told); several cores.
5. **Finding and Fixing Bugs** — `finding-and-fixing-bugs`
   Three kinds of error: the program does not start, it stops, or it gives a
   wrong answer; reading an error report from the bottom; tracing with a table
   and with `print`; reproducing a bug on the smallest input; changing one thing
   at a time.
6. **Project: A Quiz Game** — `project-quiz-game`
   From a one-paragraph specification to a working program: listing what it must
   do, cutting it into functions, building and testing one piece at a time, then
   improving it (scores, levels, questions kept in lists).

### Grade 8
1. **Binary and Hexadecimal** — `binary-and-hexadecimal`
   Place value in base 2 with powers of two (recalled from the mathematics
   book); converting both ways, by hand and by program; adding in binary and the
   carry; hexadecimal as shorthand for four bits; colours in hexadecimal; $n$
   bits give $2^n$ values.
2. **Dictionaries** — `dictionaries`
   Looking a value up by its key; creating, reading, changing and walking
   through a dictionary; counting with a dictionary; a record as a dictionary, a
   table as a list of records.
3. **Files and Data Tables** — `files-and-data-tables`
   Reading and writing a text file line by line; a table saved as text with
   separators; loading it as a list of records; selecting rows, counting,
   finding the largest, averaging (on the series' generated data).
4. **Searching and Sorting** — `searching-and-sorting`
   Searching item by item; searching a sorted list by halving (the
   guessing-game strategy); selection sort and insertion sort; counting
   comparisons to compare two methods.
5. **How the Internet Works** — `how-the-internet-works`
   Messages cut into packets; an address for every machine; routers pass packets
   from network to network; names turned into addresses; client and server; what
   happens between typing an address and seeing the page; speed and delay.
6. **Project: A Data Explorer** — `project-data-explorer`
   A menu-driven program that loads a data table, answers questions about it
   (filter, sort, count, top ten) and saves a report: functions, dictionaries,
   files and sorting working together.

### Grade 9
1. **Web Pages: HTML and CSS** — `html-and-css`
   A web page is a text file; elements and tags; headings, paragraphs, lists,
   links, images, tables; the page as a tree; content (HTML) kept apart from
   appearance (CSS): selectors, colours, sizes, boxes.
2. **Logic Gates and Boolean Algebra** — `logic-gates`
   True and false as 1 and 0; NOT, AND, OR, XOR and their truth tables; gates
   and circuits of gates; rules of Boolean algebra (De Morgan's laws); the half
   adder: two bits added by gates; a transistor is an electrically controlled
   switch (told; circuits and switches recalled from the physics book).
3. **Grids and Images** — `grids-and-images`
   A list of lists as a grid; rows, columns, neighbours; a grey-level image as a
   grid of numbers, a colour image as three; reading and writing a plain-text
   image file; negative, mirror, threshold, blur by averaging.
4. **Algorithms on Numbers** — `algorithms-on-numbers`
   Divisors and primality by trial division; stopping at the square root; the
   sieve for all primes below $n$; Euclid's algorithm programmed (recalled from
   the mathematics book), and why it is fast; counting steps.
5. **Randomness and Simulation** — `randomness-and-simulation`
   Pseudo-random numbers and the seed; simulating dice, coins and draws;
   frequencies settle near the probability (recalled from the mathematics
   book); a random walk; estimating an answer by simulation.
6. **Secret Codes: A First Look at Cryptography** — `first-cryptography`
   Encrypting and decrypting with a key; the shift cipher and its 25 keys;
   substitution ciphers broken by letter frequencies; a cipher with a keyword;
   why a long random key resists; what the padlock in a browser promises (told).
7. **Project: A Game on a Grid** — `project-grid-game`
   A complete game on a grid (a maze, or a cellular automaton) from
   specification to tests: representing the state, the rules as functions, the
   display as text, playing a turn.

## Book 2 — Grades 10–12

### Grade 10
1. **Specifications, Assertions and Tests** — `specifications-and-tests`
   What a function promises: precondition and postcondition; documentation
   strings; `assert`; choosing test cases (ordinary, boundary, invalid); a test
   file run automatically; a failing test as a bug report.
2. **Tuples, Sets and Comprehensions** — `tuples-sets-comprehensions`
   Tuples and unpacking; sets and membership; mutable and immutable values; two
   names for one list, and copying; lists, sets and dictionaries built by
   comprehension.
3. **Integers in the Machine** — `machine-integers`
   Unsigned integers on a fixed number of bits, and overflow; signed integers in
   two's complement, and why one adder serves both; shifts, bitwise operations
   and masks; why Python's integers never overflow and most languages' do.
4. **Floating-Point Numbers** — `floating-point`
   Binary fractions; why 0.1 has no exact representation; sign, exponent and
   significand; the gaps between neighbouring values; rounding error and how it
   builds up; comparing two floating-point numbers; special values.
5. **Text Encodings: From ASCII to UTF-8** — `text-encodings`
   Code point versus bytes; ASCII on 7 bits; the one-byte extensions and their
   conflicts; Unicode; UTF-8's variable length decoded by hand; garbled text
   explained; bytes and strings in Python.
6. **Digital Images, Sound and Compression** — `images-sound-compression`
   Sampling and quantising a signal (signals recalled from the physics book);
   sampling rate, bit depth and file size; colour depth and resolution;
   compression without loss (run-length coding; a dictionary method, told) and
   with loss (what is thrown away, told); the metadata in a file.
7. **Processing Data Tables** — `data-tables`
   A table as records under a header; selection, projection, sorting on a key,
   grouping and aggregating (statistics recalled from the mathematics book);
   joining two tables on a shared column; missing and inconsistent data; a text
   format with nesting.
8. **The Web: Clients, Servers and HTTP** — `http-clients-servers`
   The parts of an address; a request and its response read line by line;
   methods, status codes, headers; a form and its parameters; a small server
   written in Python; cookies and sessions; what runs in the browser and what on
   the server.
9. **Graphs: Networks of Roads and People** — `graphs-first-look`
   Vertices and edges; directed and weighted graphs; degree, path, distance,
   connected graph; a road map and a network of friends as graphs; a graph
   stored as a dictionary of neighbours; the shortest route found by hand; where
   a receiver gets its position (recalled from the Earth and space sciences
   book).
10. **Sensors, Actuators and Control Programs** — `sensors-actuators-control`
    A computer inside an object: sensors in, actuators out, a loop that never
    ends; measured values turned into numbers; a controller as a state machine
    (states, events, transitions); a thermostat, a traffic light and a lift
    simulated in Python.
11. **Project: A Small Web Application** — `project-web-application`
    A data table served over HTTP on the reader's own machine: routes, forms,
    pages generated from data, a test for every route. Nothing leaves the
    machine.

### Grade 11
1. **From Gates to an Arithmetic Unit** — `gates-to-arithmetic-unit`
   The full adder; chaining adders for $n$ bits; subtraction through two's
   complement; the multiplexer and the decoder; an arithmetic and logic unit
   made of these blocks; a circuit that remembers: the latch and the flip-flop.
2. **The von Neumann Machine and Assembly Language** — `von-neumann-machine`
   Processor, memory, buses, input and output; program and data in the same
   memory; registers, program counter, flags; the full instruction set of the
   toy machine; assembly programs with jumps: a condition, a loop, a sum over an
   array; from a line of Python to machine instructions.
3. **Operating Systems and the Command Line** — `os-and-command-line`
   What the kernel does: processes, memory, files, devices, users and rights;
   the file-system tree, absolute and relative paths; the shell: moving,
   listing, copying, permissions, redirection and pipes; free and proprietary
   systems.
4. **Network Layers and Protocols** — `network-protocols`
   A protocol is an agreed format and an agreed dialogue; layers and
   encapsulation; addresses and the network mask; a routing table read by hand;
   reliable delivery over an unreliable network: acknowledgements, timeouts, the
   alternating-bit protocol; ports.
5. **Proving Algorithms Correct** — `proving-algorithms-correct`
   Does it stop? A quantity that strictly decreases. Is the answer right? The
   loop invariant: true at the start, kept by each turn, useful at the end.
   Proofs for the largest element, selection sort, insertion sort and binary
   search.
6. **The Cost of an Algorithm** — `cost-of-an-algorithm`
   Counting elementary operations as a function of the input size; best and
   worst case; constant, linear and quadratic cost; the cost of halving, as the
   number of times $n$ can be halved; measured running times set against the
   counts.
7. **Greedy Algorithms** — `greedy-algorithms`
   Optimisation problems; the greedy choice; giving change, choosing
   activities, filling a knapsack; cases where the greedy answer is optimal,
   with proof, and counter-examples where it is not.
8. **Classifying by Neighbours: the k-NN Algorithm** — `k-nearest-neighbours`
   Learning from labelled examples; a distance between examples; the $k$ nearest
   neighbours vote; choosing $k$; measuring the error on examples kept aside;
   what the method cannot do, and its cost.
9. **Modules, Interfaces and Libraries** — `modules-and-interfaces`
   Splitting a program into modules; the interface of a module and its hidden
   implementation; importing; the standard library and how to read its
   documentation; documenting one's own module; changing an implementation
   without touching its users.
10. **Project: An Assembler and Simulator for the Toy Machine** — `project-toy-machine`
    The reader's own version of the series' simulator: reading assembly text,
    encoding instructions, running the fetch–execute cycle, with the chapter's
    programs as tests.

### Grade 12
1. **Recursion** — `recursion`
   A function that calls itself; base case and recursive case; the call stack;
   a recursive function proved by induction (recalled from the mathematics
   book); recursion and loops; the towers of Hanoi, recursive drawings, the cost
   of the naive Fibonacci.
2. **Classes and Objects** — `classes-and-objects`
   Grouping data with the functions that act on it; class, instance,
   attributes, methods, constructor; encapsulation and the interface of a class;
   special methods; inheritance (first look).
3. **Linked Lists, Stacks and Queues** — `lists-stacks-queues`
   An abstract data type is defined by its operations; the linked list of
   cells; the stack (last in, first out) and the queue (first in, first out),
   each implemented two ways; the cost of each operation; checking brackets,
   evaluating a postfix expression.
4. **Trees and Binary Search Trees** — `trees`
   Root, node, leaf, depth, height, size; the recursive definition of a binary
   tree; preorder, inorder, postorder and breadth-first traversals; the binary
   search tree: search and insertion, cost bounded by the height; balanced and
   degenerate trees.
5. **Graph Traversals and Shortest Paths** — `graph-algorithms`
   Adjacency lists and the adjacency matrix (recalled from the mathematics
   book); depth-first search with a stack, breadth-first search with a queue;
   reachability, cycles, shortest paths counted in edges; Dijkstra's algorithm
   on weighted graphs, with its invariant.
6. **Divide and Conquer** — `divide-and-conquer`
   Split, solve, combine; merge sort and its $n \log_2 n$ cost (logarithms
   recalled from the mathematics book); binary search read again; fast
   exponentiation; rotating an image by quarters.
7. **Dynamic Programming** — `dynamic-programming`
   Overlapping subproblems; memoisation and the bottom-up table; change with
   the fewest coins; the longest common subsequence and the alignment of two
   texts; the 0/1 knapsack; rebuilding the solution from the table.
8. **Searching in Text** — `text-search`
   The naive search and its worst case; preprocessing the pattern: the
   Boyer–Moore–Horspool shift table; cost in practice; searching for several
   patterns at once (told).
9. **Relational Databases and SQL** — `relational-databases-sql`
   Why flat files fail: redundancy and anomalies; relations, attributes,
   domains; primary and foreign keys; the schema; `SELECT` with conditions,
   ordering, aggregates and joins; inserting, updating, deleting; what a
   database system guarantees. Run through Python's built-in engine.
10. **Processes and Scheduling** — `processes-and-scheduling`
    Program and process; the states of a process; the scheduler and round
    robin; the context switch; two processes and one resource: race conditions,
    mutual exclusion, deadlock and its four conditions.
11. **Routing** — `routing`
    A network as a weighted graph; distance-vector routing by exchanged tables,
    and its slow convergence; link-state routing with Dijkstra's algorithm and
    costs from link speeds; a route recomputed after a failure.
12. **Cryptography and Secure Communication** — `secure-communication`
    Symmetric encryption and the problem of sharing the key; agreeing on a key
    in public; a key pair for encryption and for signatures, on the arithmetic
    of the mathematics book (modular powers and the miniature RSA recalled);
    hash functions; certificates; the steps of a secure web connection.
13. **What Programs Cannot Do: The Halting Problem** — `halting-problem`
    A program is data: interpreters, compilers, programs that read programs;
    decidable problems; the halting problem, and the proof by contradiction
    that no program decides it; other undecidable questions (told); computable
    does not mean feasible.
14. **Project: A Route Planner** — `project-route-planner`
    The series' generated region as a database of places and roads: queried in
    SQL, loaded into a graph, searched with Dijkstra's algorithm, behind a class
    interface, with tests.

## Book 3 — University Year 1 (`bachelor-1`)

C is the language of Parts I, IV and VI; Parts III and V write their algorithms
in Python, where memory is not the point.

### Part I — C and the machine model
1. **From Source Code to a Running Program** — `compilation-pipeline`
   Preprocessing, compiling, assembling, linking; object files and the
   executable; compiler warnings as a tool; the memory of a running process:
   code, static data, stack, heap; an interpreted and a compiled language
   compared on the same program.
2. **C: Types, Operators and Control Flow** — `c-types-and-control`
   Integer types and their widths, floating types, characters; conversions and
   their traps; operators and order of evaluation; `if`, `switch`, loops;
   undefined behaviour: what the standard does not promise.
3. **Functions and the Call Stack** — `c-functions-and-stack`
   Declaration and definition; passing by value; the stack frame: parameters,
   local variables, return address; recursion on the stack, and its overflow;
   scope and lifetime; static and global variables.
4. **Pointers and Arrays** — `pointers-and-arrays`
   Addresses; pointer types and dereferencing; a pointer passed to change the
   caller's data; arrays and pointer arithmetic; arrays as parameters; access
   out of bounds; pointers to functions.
5. **Dynamic Memory** — `dynamic-memory`
   `malloc` and `free`; a lifetime chosen by the programmer; leaks, double free
   and use after free, and the tools that find them; conventions of ownership;
   a growable array written by hand.
6. **Strings, Structures and Files** — `c-strings-structs-files`
   Null-terminated strings and their dangers; `struct`, `union`, `enum`; layout
   and alignment; text files and binary files; reading input robustly.
7. **Modular Programs, Makefiles and Tests** — `c-modules-make-tests`
   Header and implementation files; opaque types; separate compilation and the
   dependency graph of a Makefile; unit tests in C; a session with a debugger;
   assertions and defensive programming.

### Part II — Tools
8. **The Shell** — `the-shell`
   Processes, arguments, environment, exit status; redirection and pipes; text
   tools and regular expressions in practice; shell scripts; permissions.
9. **Version Control with Git** — `version-control`
   Snapshots, commits and the commit graph; the staging area; branches and
   merges; resolving a conflict; remote repositories; searching history for the
   commit that broke a test; what a good commit is.

### Part III — Reasoning about programs
10. **Propositional Logic** — `propositional-logic`
    Formulas as trees; valuations and truth (truth tables recalled from the
    mathematics book); equivalence and normal forms; satisfiability and a
    backtracking solver; a puzzle modelled as a formula.
11. **Induction, Recursion and Termination** — `induction-and-termination`
    Inductively defined sets (lists, trees, formulas); structural induction;
    well-founded orders; termination by a variant; recursive functions proved
    correct.
12. **Program Correctness** — `program-correctness`
    Specifications as preconditions and postconditions; partial and total
    correctness; loop invariants found systematically; proofs for array
    algorithms (partition, binary search with every boundary case, the
    three-colour flag).
13. **Asymptotic Analysis and Recurrences** — `asymptotic-analysis`
    $O$, $\Omega$ and $\Theta$ defined and handled (comparison of sequences
    recalled from the mathematics book); worst, best and average case; sums;
    recurrences solved by unrolling and by the master theorem; cost in space;
    what the model of computation counts.

### Part IV — Data structures
14. **Dynamic Arrays and Amortised Analysis** — `dynamic-arrays`
    Abstract type versus implementation; the doubling array; amortised cost by
    the aggregate, accounting and potential methods; the circular buffer.
15. **Linked Structures: Lists, Stacks and Queues** — `linked-structures`
    Singly and doubly linked lists in C; sentinels; stacks, queues and deques
    on arrays and on links; iterators; costs compared, by proof and by
    measurement.
16. **Hash Tables** — `hash-tables`
    Hash functions; chaining and open addressing; load factor and resizing;
    expected cost under uniform hashing (stated; proved in the Year 2 volume);
    sets and dictionaries; inputs that defeat a hash function.
17. **Binary Search Trees and Balanced Trees** — `balanced-trees`
    Search, insertion, deletion; bounds on the height; rotations; AVL trees
    with the proof of their height bound; red-black trees (told); ordered
    dictionaries.
18. **Heaps and Priority Queues** — `heaps`
    The priority-queue type; the binary heap in an array; sifting up and down;
    building a heap in linear time; heapsort.
19. **Sorting** — `sorting`
    Quicksort and its partition, worst case and average case by counting; merge
    sort; the $n \log n$ lower bound for sorting by comparisons; counting sort
    and radix sort; stability; how library sorts are built.

### Part V — Algorithm design
20. **Exhaustive Search and Backtracking** — `backtracking`
    Enumerating subsets, permutations and combinations (counting recalled from
    the mathematics book); the search tree; pruning; n queens, sudoku, subset
    sum; branch and bound (first look).
21. **Divide and Conquer** — `divide-and-conquer`
    The paradigm and its recurrences; Karatsuba's multiplication; the closest
    pair of points; selection in linear time; fast matrix multiplication
    (told).
22. **Greedy Algorithms and Their Proofs** — `greedy-proofs`
    The exchange argument; interval scheduling; Huffman codes and their
    optimality; a greedy answer as an approximation.
23. **Dynamic Programming** — `dynamic-programming`
    Optimal substructure stated and proved; the recurrence first, the table
    second; edit distance, matrix-chain order, knapsack, longest increasing
    subsequence; saving space; rebuilding the solution.
24. **Graphs and Traversals** — `graph-traversals`
    Definitions, representations and their costs; depth-first search with
    discovery times and edge classes; breadth-first search; connected
    components, bipartite graphs, topological order, strongly connected
    components.
25. **Shortest Paths** — `shortest-paths`
    Dijkstra's algorithm with a heap, proved; negative weights and
    Bellman–Ford; all pairs with Floyd–Warshall; shortest paths in an acyclic
    graph.
26. **Minimum Spanning Trees and Union–Find** — `spanning-trees`
    The cut property; Kruskal's and Prim's algorithms, proved; disjoint sets
    with union by rank and path compression (bound stated).

### Part VI — Machine and data
27. **Boolean Algebra and Combinational Circuits** — `combinational-circuits`
    Boolean functions and their canonical forms; simplification by algebra and
    by Karnaugh maps; NAND alone is enough; adders with carry look-ahead,
    multiplexers, decoders, the arithmetic and logic unit; propagation delay.
28. **Sequential Circuits and Finite-State Machines** — `sequential-circuits`
    Latches, flip-flops and the clock; registers, counters, memory cells; Moore
    and Mealy machines; from a state diagram to a circuit; the control of a
    small processor as a state machine.
29. **The Relational Model, Relational Algebra and SQL** — `relational-model`
    Relations, keys and integrity constraints (relations recalled from the
    mathematics book); the operators of relational algebra and their laws; SQL
    read as algebra: joins, grouping, nested queries, views;
    entity–relationship modelling and its translation into tables.
30. **Project: A Search Engine for a Folder of Texts** — `project-text-search-engine`
    In C: splitting files into words, an inverted index in a hash table, ranked
    answers with a heap, a test suite, a Makefile, a Git history; measured
    against the naive scan.

## Book 4 — University Year 2 (`bachelor-2`)

### Part I — C++
1. **From C to C++: Classes and Resource Management** — `cpp-classes-raii`
   References; classes, constructors and destructors; a resource acquired in a
   constructor and released in the destructor; `const`; namespaces; exceptions
   and what they cost.
2. **Copying, Moving and Smart Pointers** — `cpp-copy-move`
   Copy construction and assignment; value semantics; moves; the rule of zero
   and the rule of five; unique and shared ownership through smart pointers.
3. **Inheritance and Polymorphism** — `cpp-polymorphism`
   Derived classes; virtual functions and the dispatch table; abstract classes
   as interfaces; composition against inheritance; the substitution principle;
   the object-oriented design of a small system.
4. **Templates and Generic Programming** — `cpp-templates`
   Function and class templates; instantiation at compile time; requirements
   on a type parameter; static against dynamic polymorphism; one generic
   container written once.
5. **The Standard Library: Containers, Iterators and Algorithms** — `cpp-standard-library`
   Sequence and associative containers and the structures behind them (recalled
   from the Year 1 volume); iterator categories; algorithms and anonymous
   functions; cost guarantees; a container chosen by measurement.

### Part II — Rust and functional programming
6. **Rust: Ownership and Borrowing** — `rust-ownership`
   One owner per value; moves; shared and exclusive borrows; lifetimes; the
   errors C allows and this compiler refuses (use after free, data race);
   slices and strings.
7. **Enums, Pattern Matching and Error Handling** — `rust-enums-and-errors`
   Sum types and product types; `match` and exhaustiveness; `Option` and
   `Result` in place of null and exceptions; recursive types: lists and trees.
8. **Traits and Generics** — `rust-traits-and-generics`
   Traits as interfaces; generic functions compiled once per type; trait
   objects and dynamic dispatch; the standard traits; compared with C++
   templates and virtual functions.
9. **Functional Programming** — `functional-programming`
   Functions as values; closures; map, filter, fold; iterators and laziness;
   immutable data and persistent structures; recursion and tail calls;
   reasoning by equations.

### Part III — Architecture
10. **Assembly Language and the Calling Convention** — `assembly-and-calling-convention`
    An instruction set (a RISC-V subset): registers, arithmetic, loads and
    stores, branches; how an instruction is encoded; the calling convention and
    the stack frame; C constructs compiled by hand, and the compiler's output
    read.
11. **The Processor: Datapath, Control and Pipelining** — `processor-and-pipelining`
    A single-cycle datapath built from the Year 1 blocks; control signals; the
    five-stage pipeline; hazards, forwarding, stalls; branch prediction; the
    performance equation.
12. **Caches and the Memory Hierarchy** — `caches`
    Locality; direct-mapped and associative caches; misses classified and
    measured; code that respects the cache (traversal order, layout); the
    hierarchy from registers to disks.

### Part IV — Systems programming
13. **Processes and System Calls** — `processes-and-system-calls`
    User mode and kernel mode; the system call; creating a process, executing a
    program, waiting for a child; the process tree; a minimal shell.
14. **Files, Pipes and Signals** — `files-pipes-signals`
    File descriptors; reading, writing and buffering; the interface of the file
    system: inodes, links, directories; pipes and redirection implemented;
    signals and handlers.
15. **Threads and Synchronisation** — `threads-and-synchronisation`
    Threads and processes; data races; mutual exclusion: Peterson's algorithm,
    locks; condition variables and semaphores; producer–consumer and
    readers–writers; the same programs in C, C++ and Rust.
16. **Sockets** — `sockets`
    The socket interface; a TCP client and server; UDP; serving several clients
    (processes, threads, an event loop); framing the messages of a protocol;
    byte order.

### Part V — Networks
17. **The Link Layer** — `link-layer`
    Frames; error detection (parity, checksums, cyclic redundancy codes);
    sharing a medium; Ethernet and switches; address resolution; wireless links
    (signals recalled from the physics book).
18. **The Network Layer: IP and Routing** — `network-layer`
    Addresses, prefixes and the longest-prefix match; forwarding and routing;
    address translation; fragmentation; IPv6; distance-vector and link-state
    algorithms analysed; routing between operators (told).
19. **The Transport Layer: UDP and TCP** — `transport-layer`
    Multiplexing by ports; reliable transfer: sliding windows and
    retransmission; TCP's connection, flow control and congestion control;
    fairness; newer transports (`dated` box).
20. **The Application Layer: DNS, HTTP and TLS** — `application-layer`
    The hierarchy and caching of the name system; the versions of HTTP;
    electronic mail (told); TLS as a layer: handshake, certificates, what is
    protected and what is not.

### Part VI — Languages and logic
21. **Finite Automata** — `finite-automata`
    Alphabets, words, languages; deterministic and nondeterministic automata;
    the subset construction; empty transitions; closure properties; an
    automaton as a program.
22. **Regular Expressions and the Limits of Regular Languages** — `regular-languages`
    Regular expressions; Kleene's theorem in both directions; minimisation and
    the Myhill–Nerode theorem; the pumping lemma and languages that are not
    regular; decision problems.
23. **Context-Free Grammars and Pushdown Automata** — `context-free-languages`
    Grammars, derivations, parse trees; ambiguity; normal forms; the CYK
    algorithm; pushdown automata, equivalent to grammars (one direction
    admitted); the limits of context-free languages.
24. **Predicate Logic and Formal Proofs** — `predicate-logic`
    Terms, formulas, free and bound variables; structures and truth; natural
    deduction for propositional and predicate logic; soundness proved,
    completeness stated; what a proof assistant checks.

### Part VII — Algorithms II and data
25. **Text Algorithms and Compression** — `text-algorithms`
    The Knuth–Morris–Pratt algorithm and its automaton; Rabin–Karp; tries;
    Lempel–Ziv–Welch compression.
26. **Flows and Matchings** — `flows-and-matchings`
    Flow networks; augmenting paths; the max-flow min-cut theorem; the
    Edmonds–Karp algorithm; matchings in bipartite graphs; problems modelled as
    flows.
27. **Randomised Algorithms** — `randomised-algorithms`
    Algorithms that are always right and sometimes slow, or always fast and
    sometimes wrong; expected running time (probability recalled from the
    mathematics book); randomised quicksort and selection; universal hashing
    proved; Bloom filters; testing primality.
28. **Search and Games** — `search-and-games`
    State spaces; uniform-cost search and A* with an admissible heuristic,
    proved; two-player games: minimax, alpha–beta pruning, evaluation
    functions; positions solved backwards from the end.
29. **Learning from Examples: Decision Trees and Clustering** — `trees-and-clustering`
    Supervised and unsupervised learning as algorithmic problems; decision
    trees grown by information gain; k-means and why it stops; hierarchical
    clustering; k-d trees for nearest neighbours; overfitting measured.
30. **Database Design: Dependencies, Normal Forms and Transactions** — `database-design`
    Functional dependencies and closures; keys computed; the third and
    Boyce–Codd normal forms, and decomposition; transactions and their four
    guarantees; isolation anomalies seen in a live session; using an index.
31. **Project: A Key-Value Server** — `project-key-value-server`
    In Rust or C++: a text protocol over TCP, a concurrent hash map behind
    locks, persistence in an append-only file, a load test and its
    measurements.

## Book 5 — University Year 3 (`bachelor-3`)

### Part I — Compilers and programming languages
One small language is compiled across the part, in Rust.

1. **Lexical Analysis** — `lexical-analysis`
   The phases of a compiler; tokens; from regular expressions to a scanner
   (automata recalled from the Year 2 volume); the longest match; error
   positions.
2. **Top-Down Parsing** — `top-down-parsing`
   A grammar for a programming language; first and follow sets; LL(1)
   grammars; recursive descent; operator precedence; recovering from an error.
3. **Bottom-Up Parsing** — `bottom-up-parsing`
   Shift and reduce; LR(0) items and their automaton; SLR tables; LALR (told);
   conflicts and how to resolve them; parser generators.
4. **Abstract Syntax and Semantic Analysis** — `semantic-analysis`
   Abstract syntax trees; scopes and symbol tables; resolving names; checking
   the types of a simple typed language; useful error messages.
5. **The Lambda Calculus and Operational Semantics** — `lambda-calculus`
   Terms, substitution, reduction; evaluation strategies; data encoded as
   functions; fixed points; small-step and big-step semantics; an interpreter
   derived from the rules.
6. **Type Systems and Type Inference** — `type-systems`
   Typing rules and derivations; type safety as progress and preservation,
   proved for a small language; polymorphism; unification and inference; what
   an ownership type system checks.
7. **Intermediate Code and Code Generation** — `code-generation`
   Three-address code and control-flow graphs; translating expressions,
   control flow and calls; activation records; selecting instructions for the
   Year 2 instruction set.
8. **Program Analysis and Optimisation** — `program-optimisation`
   Dataflow analysis as a fixed point: liveness, reaching definitions; static
   single assignment; the classic optimisations; register allocation by graph
   colouring.
9. **Memory Management and Garbage Collection** — `garbage-collection`
   Allocators: free lists and fragmentation; reference counting; mark and
   sweep, copying and generational collection; memory safety without a
   collector.

### Part II — Operating systems
10. **The Kernel and CPU Scheduling** — `kernel-and-scheduling`
    The structure of a kernel; interrupts and traps; the context switch in
    detail; scheduling policies analysed (first come, shortest job, round
    robin, multilevel feedback, fair share); real-time constraints (told).
11. **Virtual Memory** — `virtual-memory`
    Address spaces; paging and multi-level page tables; the translation cache;
    demand paging; replacement policies analysed; copy on write; files mapped
    into memory.
12. **Storage Devices and File Systems** — `file-systems`
    Hard disks and flash at the level of blocks, seeks and wear; the layout of
    a file system: inodes, directories, free space; journaling and consistency
    after a crash; log-structured designs; redundancy across disks.
13. **Concurrency: Deadlock, Monitors and Lock-Free Structures** — `concurrency`
    Safety and liveness; deadlock characterised, prevented, detected; monitors;
    memory models and atomic operations; a lock-free stack and queue, and the
    ABA problem; linearisability.
14. **Virtual Machines and Containers** — `virtualisation`
    Trap and emulate; hardware support; hypervisors; containers as isolated
    processes (namespaces, resource limits); what each one isolates.

### Part III — Theory of computation
15. **Turing Machines and Computability** — `computability`
    Turing machines; the Church–Turing thesis; a universal machine; decidable
    and semi-decidable languages; undecidability by diagonalisation and by
    reduction; Rice's theorem.
16. **Time and Space Complexity** — `complexity-classes`
    Classes of time and space; P, and NP by verifiers; the hierarchy theorems
    (stated); polynomial space and Savitch's theorem; logarithmic space.
17. **NP-Completeness** — `np-completeness`
    Polynomial reductions; the Cook–Levin theorem proved; a chain of reductions
    (3-SAT, clique, vertex cover, Hamiltonian cycle, subset sum); co-NP; what
    an NP-completeness proof tells an engineer.
18. **Approximation and Exact Methods for Hard Problems** — `hard-problems`
    Approximation ratios: vertex cover, set cover, the travelling salesman
    under the triangle inequality; limits of approximation (told); branch and
    bound; satisfiability solvers that learn clauses; local search.
19. **Information, Entropy and Error-Correcting Codes** — `information-and-codes`
    Entropy; the source-coding theorem and the optimality of Huffman codes;
    channel capacity (stated); Hamming distance, linear codes, Hamming codes;
    cyclic redundancy codes read again; Reed–Solomon codes (told).
20. **Program Verification: Hoare Logic and Model Checking** — `program-verification`
    Hoare triples and their proof rules; weakest preconditions; verification
    conditions handed to a solver; temporal properties and the model checking
    of finite-state systems.

### Part IV — Data and distributed systems
21. **Database Storage and Indexes** — `database-storage`
    Pages, records and the buffer pool; B+ trees: search, insertion, deletion,
    height; hash indexes; log-structured merge trees.
22. **Query Processing and Optimisation** — `query-optimisation`
    Algorithms for selection, sorting and joins; algebraic rewriting; cost
    estimates and statistics; the search for a plan; reading a query plan.
23. **Concurrency Control and Recovery** — `transactions-and-recovery`
    Serialisability; two-phase locking; multiversion concurrency; isolation
    levels; write-ahead logging and recovery after a crash.
24. **Parallel Programming** — `parallel-programming`
    Speed-up and the laws of Amdahl and Gustafson; task and data parallelism;
    work and span; parallel loops, reductions, divide and conquer; vector
    instructions and accelerators (told).
25. **Distributed Systems: Time, Failures and Remote Calls** — `distributed-systems`
    No shared clock and no shared memory; failure models; remote procedure
    calls and what they can promise; logical and vector clocks; consistent
    snapshots.
26. **Replication and Consensus** — `replication-and-consensus`
    Replication and consistency models; the impossibility of consensus in an
    asynchronous system (stated); the Raft protocol step by step; quorums; the
    trade-off between consistency and availability.

### Part V — Security
27. **Symmetric Cryptography and Hash Functions** — `symmetric-cryptography`
    What "secure" means; the one-time pad; block ciphers and their modes;
    stream ciphers; hash functions and their properties; message
    authentication; authenticated encryption.
28. **Public-Key Cryptography and Secure Protocols** — `public-key-cryptography`
    Key exchange; RSA and its correct use (arithmetic recalled from the
    mathematics book); elliptic curves (told); signatures; certificates and
    trust; the TLS handshake analysed; storing passwords.
29. **Software Security** — `software-security`
    Threat models; memory-safety errors and their defences, on the book's own
    toy programs; injection and the validation of input; web vulnerabilities
    and their fixes; authentication and access control; least privilege.

### Part VI — Building software
30. **Software Engineering: Design, Testing and Maintenance** — `software-engineering`
    From requirements to design; modularity, coupling, interfaces; a few design
    patterns and when they pay; unit, integration and property-based tests;
    coverage; continuous integration; code review; refactoring under tests.
31. **Computer Graphics: From Triangles to Pixels** — `computer-graphics`
    Coordinates and transformations as matrices (recalled from the mathematics
    book); projection; rasterising a triangle; visibility with a depth buffer;
    shading; a simple scene traced ray by ray.
32. **Project: A Replicated Key-Value Store** — `project-replicated-store`
    The Year 2 server made fault-tolerant: a write-ahead log, three replicas,
    leader election and log replication, tests that kill a node, a consistency
    check.

---

## Notion-ownership map

The **owner** teaches the notion; the chapters listed under *recalled in* open
with a short *You already know* box and build on it. Notions owned in Books 1–2
and re-derived rigorously in a university book are listed with both owners: the
university chapter re-founds the notion and does not repeat the school level.

### Books 1–2 (one owner each; a later chapter recalls and adds)

| Notion | Owner | Recalled in |
|---|---|---|
| computer, input and output | g1 `what-is-a-computer` | g3 `inside-the-computer` |
| instructions in sequence | g1 `instructions-in-order` | g4 `algorithms-repeat-and-decide` |
| the keys, the pointer | g2 `keyboard-and-mouse` | g3 `typing-with-ten-fingers` |
| window, saving a file | g2 `using-a-computer` | g3 `files-and-folders` |
| touch typing | g3 `typing-with-ten-fingers` | — (practised from then on) |
| processor, memory, storage, ports | g3 `inside-the-computer` | g4 `memory-and-storage`, g7 `how-a-processor-runs-a-program` |
| file, folder, path | g3 `files-and-folders` | g8 `files-and-data-tables`, g11 `os-and-command-line` |
| RAM, hard disk, SSD, byte units | g4 `memory-and-storage` | g5 `bits-and-bytes`, g10 `images-sound-compression` |
| program, operating system | g4 `programs-and-operating-system` | g6 `first-python-program`, g11 `os-and-command-line` |
| algorithm, repetition, condition (by hand) | g4 `algorithms-repeat-and-decide` | g6 `for-loops-turtle`, `if-else`, `while-loops` |
| bit, byte, counting in binary | g5 `bits-and-bytes` | g8 `binary-and-hexadecimal` |
| character code | g5 `text-pictures-sound-as-numbers` | g7 `strings`, g10 `text-encodings` |
| pixel, red–green–blue | g5 `text-pictures-sound-as-numbers` | g9 `grids-and-images`, g10 `images-sound-compression` |
| network, Internet, server, browser | g5 `networks-first-look` | g8 `how-the-internet-works` |
| variable, assignment, type | g6 `variables-and-input` | every later chapter |
| `for` loop | g6 `for-loops-turtle` | every later chapter |
| condition, Boolean value in a program | g6 `if-else` | g9 `logic-gates` |
| `while` loop | g6 `while-loops` | g11 `proving-algorithms-correct` |
| function | g7 `functions` | g10 `specifications-and-tests`, g12 `recursion` |
| list | g7 `lists` | g9 `grids-and-images`, g10 `tuples-sets-comprehensions` |
| string | g7 `strings` | g10 `text-encodings`, g12 `text-search` |
| fetch–execute cycle, machine language | g7 `how-a-processor-runs-a-program` | g11 `von-neumann-machine` |
| kinds of error, tracing | g7 `finding-and-fixing-bugs` | g10 `specifications-and-tests` |
| base conversion, hexadecimal, binary addition | g8 `binary-and-hexadecimal` | g9 `logic-gates`, g10 `machine-integers` |
| dictionary | g8 `dictionaries` | g10 `data-tables`, `graphs-first-look` |
| text file, table of records | g8 `files-and-data-tables` | g10 `data-tables`, g12 `relational-databases-sql` |
| linear and binary search, selection and insertion sort | g8 `searching-and-sorting` | g11 `proving-algorithms-correct`, `cost-of-an-algorithm`, g12 `divide-and-conquer` |
| packet, address, router, name system, client and server | g8 `how-the-internet-works` | g10 `http-clients-servers`, g11 `network-protocols` |
| HTML, CSS | g9 `html-and-css` | g10 `http-clients-servers` |
| Boolean operations, gates, half adder | g9 `logic-gates` | g11 `gates-to-arithmetic-unit` |
| grid as a list of lists | g9 `grids-and-images` | g12 `dynamic-programming` |
| pseudo-random numbers, simulation | g9 `randomness-and-simulation` | g11 `k-nearest-neighbours` |
| cipher, key, frequency analysis | g9 `first-cryptography` | g12 `secure-communication` |
| specification, assertion, test | g10 `specifications-and-tests` | every later chapter |
| mutability, tuple, set | g10 `tuples-sets-comprehensions` | g12 `classes-and-objects` |
| two's complement, bitwise operations | g10 `machine-integers` | g11 `gates-to-arithmetic-unit` |
| floating-point representation | g10 `floating-point` | g11 `k-nearest-neighbours` |
| sampling and quantising as data, compression | g10 `images-sound-compression` | g10 `sensors-actuators-control` |
| join of two tables | g10 `data-tables` | g12 `relational-databases-sql` |
| HTTP, request and response | g10 `http-clients-servers` | g12 `secure-communication` |
| graph, path, distance | g10 `graphs-first-look` | g12 `graph-algorithms`, `routing` |
| state machine | g10 `sensors-actuators-control` | g12 `processes-and-scheduling` |
| adder, multiplexer, flip-flop | g11 `gates-to-arithmetic-unit` | g11 `von-neumann-machine` |
| von Neumann model, assembly | g11 `von-neumann-machine` | g12 `halting-problem` |
| kernel, shell, permissions | g11 `os-and-command-line` | g12 `processes-and-scheduling` |
| protocol, layer, routing table | g11 `network-protocols` | g12 `routing` |
| invariant, termination | g11 `proving-algorithms-correct` | every algorithm chapter of g12 |
| cost of an algorithm | g11 `cost-of-an-algorithm` | every algorithm chapter of g12 |
| greedy method | g11 `greedy-algorithms` | g12 `dynamic-programming` |
| module, interface | g11 `modules-and-interfaces` | g12 `classes-and-objects`, `lists-stacks-queues` |
| recursion | g12 `recursion` | g12 `trees`, `divide-and-conquer`, `dynamic-programming` |
| stack, queue | g12 `lists-stacks-queues` | g12 `graph-algorithms` |
| Dijkstra's algorithm | g12 `graph-algorithms` | g12 `routing` |

### Years 1–3 (one owner each across the three books)

| Notion | Owner | Re-founds (Books 1–2) | Recalled in |
|---|---|---|---|
| compilation, memory of a process | Y1 `compilation-pipeline` | — | Y2 `assembly-and-calling-convention`, Y3 `code-generation` |
| call stack, stack frame | Y1 `c-functions-and-stack` | g12 `recursion` | Y2 `assembly-and-calling-convention` |
| pointer, heap allocation | Y1 `pointers-and-arrays`, `dynamic-memory` | — | Y2 `cpp-classes-raii`, `rust-ownership`, Y3 `garbage-collection` |
| shell | Y1 `the-shell` | g11 `os-and-command-line` | Y2 `processes-and-system-calls` |
| propositional logic, satisfiability | Y1 `propositional-logic` | g9 `logic-gates` | Y2 `predicate-logic`, Y3 `np-completeness`, `hard-problems` |
| structural induction, termination | Y1 `induction-and-termination` | g11 `proving-algorithms-correct`, g12 `recursion` | every later proof |
| invariants, total correctness | Y1 `program-correctness` | g11 `proving-algorithms-correct` | Y3 `program-verification` |
| asymptotic notation, recurrences | Y1 `asymptotic-analysis` | g11 `cost-of-an-algorithm` | every later analysis |
| amortised cost | Y1 `dynamic-arrays` | — | Y1 `spanning-trees` |
| linked list, stack, queue | Y1 `linked-structures` | g12 `lists-stacks-queues` | Y2 `cpp-standard-library` |
| hash table | Y1 `hash-tables` | g8 `dictionaries` (use only) | Y2 `randomised-algorithms`, Y3 `database-storage` |
| search trees, balancing | Y1 `balanced-trees` | g12 `trees` | Y2 `cpp-standard-library`, Y3 `database-storage` |
| heap, priority queue | Y1 `heaps` | — | Y1 `shortest-paths`, Y2 `search-and-games` |
| quicksort, sorting lower bound | Y1 `sorting` | g8 `searching-and-sorting`, g12 `divide-and-conquer` | Y2 `randomised-algorithms` |
| backtracking | Y1 `backtracking` | — | Y3 `hard-problems` |
| divide and conquer | Y1 `divide-and-conquer` | g12 `divide-and-conquer` | Y3 `parallel-programming` |
| greedy proofs, Huffman codes | Y1 `greedy-proofs` | g11 `greedy-algorithms` | Y3 `information-and-codes` |
| dynamic programming | Y1 `dynamic-programming` | g12 `dynamic-programming` | Y2 `context-free-languages` |
| traversals, topological order, strong components | Y1 `graph-traversals` | g10 `graphs-first-look`, g12 `graph-algorithms` | Y3 `program-optimisation` |
| shortest paths | Y1 `shortest-paths` | g12 `graph-algorithms` | Y2 `network-layer`, `search-and-games` |
| spanning tree, union–find | Y1 `spanning-trees` | — | — |
| combinational circuits | Y1 `combinational-circuits` | g9 `logic-gates`, g11 `gates-to-arithmetic-unit` | Y2 `processor-and-pipelining` |
| sequential circuits, finite-state machine | Y1 `sequential-circuits` | g10 `sensors-actuators-control` | Y2 `finite-automata`, `processor-and-pipelining` |
| relational model, relational algebra, SQL | Y1 `relational-model` | g12 `relational-databases-sql` | Y2 `database-design`, Y3 `query-optimisation` |
| class, inheritance, polymorphism | Y2 `cpp-classes-raii`, `cpp-polymorphism` | g12 `classes-and-objects` | Y3 `software-engineering` |
| generic programming | Y2 `cpp-templates` | — | Y2 `rust-traits-and-generics` |
| ownership and borrowing | Y2 `rust-ownership` | — | Y3 `type-systems`, `garbage-collection` |
| sum types, pattern matching | Y2 `rust-enums-and-errors` | — | Y3 `semantic-analysis` |
| closure, higher-order function | Y2 `functional-programming` | — | Y3 `lambda-calculus` |
| instruction set, calling convention | Y2 `assembly-and-calling-convention` | g11 `von-neumann-machine` | Y3 `code-generation` |
| datapath, pipeline | Y2 `processor-and-pipelining` | g7 `how-a-processor-runs-a-program` | Y3 `parallel-programming` |
| cache, locality | Y2 `caches` | — | Y3 `virtual-memory`, `database-storage` |
| system call, process creation | Y2 `processes-and-system-calls` | g12 `processes-and-scheduling` | Y3 `kernel-and-scheduling` |
| file descriptor, inode (interface) | Y2 `files-pipes-signals` | g3 `files-and-folders` | Y3 `file-systems` |
| thread, lock, semaphore | Y2 `threads-and-synchronisation` | g12 `processes-and-scheduling` | Y3 `concurrency` |
| socket | Y2 `sockets` | — | Y3 `distributed-systems` |
| error-detecting code, cyclic redundancy code | Y2 `link-layer` | — | Y3 `information-and-codes` |
| IP addressing, routing algorithms | Y2 `network-layer` | g11 `network-protocols`, g12 `routing` | Y3 `distributed-systems` |
| reliable transport, congestion control | Y2 `transport-layer` | g11 `network-protocols` | Y3 `distributed-systems` |
| finite automaton, regular language | Y2 `finite-automata`, `regular-languages` | — | Y3 `lexical-analysis` |
| context-free grammar | Y2 `context-free-languages` | — | Y3 `top-down-parsing`, `bottom-up-parsing` |
| predicate logic, natural deduction | Y2 `predicate-logic` | — | Y3 `type-systems`, `program-verification` |
| string matching | Y2 `text-algorithms` | g12 `text-search` | — |
| flow, matching | Y2 `flows-and-matchings` | — | — |
| randomised algorithm, universal hashing | Y2 `randomised-algorithms` | g9 `randomness-and-simulation` | Y3 `hard-problems` |
| A*, minimax | Y2 `search-and-games` | — | Y3 `hard-problems` |
| decision tree, clustering | Y2 `trees-and-clustering` | g11 `k-nearest-neighbours` | — |
| functional dependency, normal form, transaction | Y2 `database-design` | — | Y3 `transactions-and-recovery` |
| type system, type inference | Y3 `type-systems` | — | — |
| garbage collection | Y3 `garbage-collection` | — | — |
| scheduling policies | Y3 `kernel-and-scheduling` | g12 `processes-and-scheduling` | — |
| virtual memory, paging | Y3 `virtual-memory` | — | Y3 `virtualisation` |
| disk and flash internals, file-system layout | Y3 `file-systems` | g4 `memory-and-storage` | Y3 `database-storage` |
| deadlock theory, lock-free structures | Y3 `concurrency` | g12 `processes-and-scheduling` | Y3 `transactions-and-recovery` |
| Turing machine, undecidability | Y3 `computability` | g12 `halting-problem` | Y3 `complexity-classes` |
| P, NP, NP-completeness | Y3 `complexity-classes`, `np-completeness` | — | Y3 `hard-problems` |
| entropy, error-correcting codes | Y3 `information-and-codes` | g10 `images-sound-compression` | — |
| Hoare logic, model checking | Y3 `program-verification` | — | — |
| B+ tree, buffer pool | Y3 `database-storage` | — | Y3 `query-optimisation` |
| serialisability, write-ahead log | Y3 `transactions-and-recovery` | — | Y3 `replication-and-consensus` |
| logical clock, consensus | Y3 `distributed-systems`, `replication-and-consensus` | — | — |
| block cipher, hash function | Y3 `symmetric-cryptography` | g9 `first-cryptography`, g12 `secure-communication` | Y3 `public-key-cryptography` |
| public-key encryption, signature, certificate | Y3 `public-key-cryptography` | g12 `secure-communication` | Y3 `software-security` |

### Owned by another series (recall, then build)

| Notion | Owner (series, year, file) | Recalled here in | What this series adds |
|---|---|---|---|
| powers of two | mathematics g8 `powers` | g8 `binary-and-hexadecimal` (g5 `bits-and-bytes` precedes it and uses doubling only) | bases 2 and 16, conversion algorithms |
| divisors, primes, Euclid's algorithm | mathematics g9 `arithmetic-gcd` | g9 `algorithms-on-numbers` | the programs, the sieve, step counts |
| probability and frequencies | mathematics g9 `statistics-and-probability` | g9 `randomness-and-simulation` | pseudo-random generation, simulation |
| mean, median, spread | mathematics g10 `statistics` | g10 `data-tables` | computing them over tables |
| proof by induction | mathematics g12 `sequences` | g12 `recursion`, Y1 `induction-and-termination` | structural induction, termination |
| logarithm | mathematics g12 `exponential-logarithm` | g12 `divide-and-conquer` (g11 `cost-of-an-algorithm` precedes it and counts halvings only) | logarithmic and $n \log n$ costs |
| counting | mathematics g12 `combinatorics`, b1 `counting` | Y1 `backtracking`, `sorting` | enumeration algorithms, the sorting lower bound |
| modular arithmetic, fast powers, miniature RSA | mathematics g12 `arithmetic`, b1 `integer-arithmetic` | g12 `secure-communication`, Y3 `public-key-cryptography` | protocols, key sizes, correct use |
| matrices, adjacency matrix, counting walks | mathematics g12 `matrices-graphs` | g12 `graph-algorithms`, Y3 `computer-graphics` | traversals and shortest paths (graph vocabulary comes first here, g10) |
| truth tables, sets, maps, relations | mathematics b1 `logic-sets-maps` | Y1 `propositional-logic`, `relational-model` | formulas as syntax, satisfiability; relations as tables |
| comparison of sequences | mathematics b1 `sequences`, `taylor-asymptotics` | Y1 `asymptotic-analysis` | $O$, $\Omega$, $\Theta$ for costs; recurrences |
| Gaussian elimination | mathematics b1 `matrices` | — (not re-taught) | — |
| discrete probability, expectation | mathematics b2 `countable-probability`, `discrete-random-variables` | Y2 `randomised-algorithms`, Y3 `information-and-codes` | expected cost, entropy |
| groups, rings, finite fields | mathematics b3 `group-theory`, `rings-arithmetic` | Y3 `public-key-cryptography`, `information-and-codes` | cryptographic and coding constructions |
| electric circuit, switch | physics g3–g8 (the circuit chapters) | g9 `logic-gates` | the switch as a logic element |
| signals | physics g10 `signals-and-waves` | g10 `images-sound-compression`, Y2 `link-layer` | sampled data and file formats (sampling is used as told) |
| optical fibre | physics g10 `refraction` | g8 `how-the-internet-works` (told) | — |
| sampling theorem, analog-to-digital conversion | physics b2 `feedback-oscillators` | — (not re-taught) | — |
| semiconductors, the transistor | physics b3 `electrons-in-solids` | g9 `logic-gates`, Y1 `combinational-circuits` (the transistor is told as a switch) | gates built from switches |
| satellite positioning | Earth and space g9 `maps-of-the-earth` | g10 `graphs-first-look` | map data as a graph, routes |

Two extra-shelf series overlap and are named in prose only, as further reading:

- **One Artificial Intelligence Book** owns machine learning. This series keeps
  three algorithm chapters (g11 `k-nearest-neighbours`, Y2 `search-and-games`,
  Y2 `trees-and-clustering`) and stays self-contained on them. That series
  assumes general algorithms and data structures, which this one teaches.
- **One Quant Book** (Books 13–15: low-latency software, networks and hardware,
  data platforms) is specialist depth on caches, lock-free programming,
  networking and databases. Nothing here depends on it.

## Conventions for the writing step (proposed, to confirm at the scaffold)

- **Exercise calibration**, as in chemistry and Earth:
  - grades 1–5: 10–11 exercises, mostly ★, no weekend problem;
  - grades 6–9: 12 exercises and a weekend problem of 10–14 questions (Parts I–III);
  - grades 10–12: exactly 15 exercises (5★/6★★/4★★★) and a problem of 18–22
    questions (Parts I–IV) ending on a named result;
  - university years: exactly 12 exercises (4★/5★★/3★★★) and one problem of
    22–28 questions.

  A project chapter replaces the weekend problem with the project's milestones.
- **Kinds of exercise.** From grade 6, each chapter mixes four kinds: predict
  what a program prints, find and fix the bug, write a function to a
  specification, and prove or count. A written program's solution is a tested
  file; a proof's solution is prose.
- **Typing.** Grade 3 owns the technique. Drill lines for later practice are an
  appendix of Book 1, one set per keyboard layout; a language edition prints the
  layouts of its countries.
- **Code mechanics**, ported from the artificial intelligence series: listings
  with `\omcode` and `\omcodes` (line ranges of a tested file, at most 40
  lines), captured output with `\omoutput`, and the gates
  `tools/check_omcode.py`, `tools/capture_output.py`, `tools/check_outputs.py`
  and `tools/test_code.sh`. Code lives in `code/<year>/NN-<slug>/` with its
  tests. Listings stay in English in every language edition except comments and
  printed strings (to settle before the first translation).
- **The toy machine.** One small instruction set serves g7, g11 and the g11
  project; its simulator is a tested Python module of the repo. The university
  books move to a RISC-V subset.
- **The data set family.** One invented town with its library loans, weather
  readings, road network and a small network of friends, generated by a seeded,
  tested script. It could reuse the invented region of the Earth and space
  series.
- **Visuals.** TikZ for circuits, memory diagrams, trees, graphs, automata,
  packet layouts and generic windows; photographs (public domain or CC, credited
  per file) of real hardware and historic machines; AI illustrations for
  everyday scenes in grades 1–6. Every figure is checked one page at a time.
- **Boxes.** `recall`, `history[title]` (the people and machines behind a
  notion), `dated{<year>}`, `safety` (passwords, backups, updates) and
  `inpractice[title]` (how professionals do it).
- **Source ledger** for checkable external facts (standards, protocol numbers,
  dates, capacities), one file per book, as in chemistry and Earth.

## Open points

- **When Python starts.** This outline starts it in grade 6, when the reader
  types fluently and the mathematics has angles and decimals. It could start one
  year earlier, as a last chapter of grade 5.
- **Assembly at university.** A RISC-V subset on a tested simulator of the repo
  is proposed, with x86-64 shown only through the compiler's output. No RISC-V
  toolchain is installed on the writing machine.
- **Toolchain.** Python 3.12, gcc 11 and Rust 1.97 are installed. The C++
  compiler, the pinned versions and the CI image are scaffold decisions.
- **SQL in grade 12.** The user's list places SQL at university. Grade 12 keeps
  a first chapter on it, run through Python, because the high-school source
  programme has one and the grade-12 project uses it. It can move to Year 1.
- **Photographs and AI illustrations.** `book_style.md` scopes them per series;
  this outline proposes both for this series.
- **Listings in language editions.** Whether identifiers stay English and only
  comments and strings are translated.
- **Size.** 165 chapters is 14 more than the Earth series. Grade 12 (14
  chapters) and Year 3 (32) are the first places to cut: `text-search`,
  `routing`, `virtualisation` and `computer-graphics` can go without breaking a
  later chapter.
- **Pilots.** Three pilot chapters before the batch, as in chemistry and Earth:
  proposed g3 `typing-with-ten-fingers`, g8 `searching-and-sorting` and b1
  `pointers-and-arrays`.

