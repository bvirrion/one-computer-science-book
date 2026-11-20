# Book 1 (grades 1–9 and typing appendix): every term the book will define

Phase A, 2026-11-20; brought in line with the sync rulings of `SERIES_DEFINITIONS.md` the same day. Frozen at the sync (run file, "Dependencies"): Book 2 recalls these notions in
prose with this wording and no definition pair. Each row is one `definition` environment; the **term(s)**
column lists the `\emph{…}\index{…}` pairs it carries (emphasis text first, index key after `→` when it
differs). Labels follow `def:<prefix>:<chapter-slug>:<leaf>`. Named methods and propositions that carry
an `\index` are listed at the end of their chapter's block.

Sense notes (rule 6 of `SERIES_DEFINITIONS.md`) are in the last column; the Phase C curation they imply is
collected in §3. **(p)** marked a row that depended on a proposal of the Phase A report; the sync accepted every one of
them (spreadsheet in g8/03, text editor vs word processor in g2/02, square root by halving in g9/04), so the
rows stand.

## 1. Terms by chapter

### Grade 1

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g1/01 what-is-a-computer | `def:g1:what-is-a-computer:computer` | computer | "desktop computer" in prose must not link *desktop* (g2) |
| | `def:g1:what-is-a-computer:input` | input; output | noun senses; Python's `input` is `\code` (masked) |
| | `def:g1:what-is-a-computer:device` | input device; output device | |
| g1/02 instructions-in-order | `def:g1:instructions-in-order:instruction` | instruction | g7/04 qualifies *machine instruction* |
| | `def:g1:instructions-in-order:sequence` | sequence of instructions → sequence of instructions | not bare *sequence* (the mathematics books own sequences) |

### Grade 2

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g2/01 keyboard-and-mouse | `def:g2:keyboard-and-mouse:key` | key → key (keyboard) | sense 1 of 3 (see §2) |
| | `def:g2:keyboard-and-mouse:cursor` | cursor | |
| | `def:g2:keyboard-and-mouse:pointer` | pointer | only sense in Book 1 (C pointers are Year 1's) |
| | `def:g2:keyboard-and-mouse:click` | click; double-click; drag | verbs everywhere: STOP outside g2 |
| | `def:g2:keyboard-and-mouse:touchpad` | touchpad; touch screen | |
| g2/02 using-a-computer | `def:g2:using-a-computer:desktop` | desktop | protect "desktop computer" |
| | `def:g2:using-a-computer:icon` | icon | |
| | `def:g2:using-a-computer:window` | window | |
| | `def:g2:using-a-computer:menu` | menu | g8/06's program menu is the same sense |
| | `def:g2:using-a-computer:save` | saving → saving (a file) | |
| | (p) `def:g2:using-a-computer:word-processor` | text editor; word processor | only if the proposed section is accepted |

### Grade 3

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g3/01 typing-with-ten-fingers | `def:g3:typing-with-ten-fingers:touch-typing` | touch typing | |
| | `def:g3:typing-with-ten-fingers:home-row` | home row | must win over g9's *grid* wording; *row* is never defined |
| | `def:g3:typing-with-ten-fingers:layout` | keyboard layout | |
| | `def:g3:typing-with-ten-fingers:wpm` | words per minute | the five-character word is part of this definition |
| g3/02 inside-the-computer | `def:g3:inside-the-computer:processor` | processor | |
| | `def:g3:inside-the-computer:memory` | memory → memory (of a computer) | working memory; *RAM* is g4/01 |
| | `def:g3:inside-the-computer:storage` | storage | |
| | `def:g3:inside-the-computer:motherboard` | motherboard | |
| | `def:g3:inside-the-computer:device` | device → peripheral device | protect generic "device" if over-linked |
| g3/03 files-and-folders | `def:g3:files-and-folders:file` | file; file name | |
| | `def:g3:files-and-folders:extension` | extension → file extension | |
| | `def:g3:files-and-folders:folder` | folder | |
| | `def:g3:files-and-folders:folder-tree` | folder tree | bare *tree* is Book 2 g12's |
| | `def:g3:files-and-folders:path` | file path | bare *path* never defined (packet paths, maze paths) |
| | `def:g3:files-and-folders:copy-move` | copying → copying a file; moving → moving a file | STOP *copy*, *move* outside g3/03 |
| | `def:g3:files-and-folders:bin` | bin → recycle bin | |

### Grade 4

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g4/01 memory-and-storage | `def:g4:memory-and-storage:ram` | RAM | |
| | `def:g4:memory-and-storage:hard-disk` | hard disk | |
| | `def:g4:memory-and-storage:flash` | flash memory | |
| | `def:g4:memory-and-storage:ssd` | SSD → solid-state drive (SSD) | |
| | (p) `def:g4:memory-and-storage:byte` | byte | **intra-book ownership**: outline g4 text vs map's g5 "bit, byte"; proposal: the byte as a unit here, "eight bits" added in g5/01 without a new pair |
| | `def:g4:memory-and-storage:multiples` | kilobyte; megabyte; gigabyte; terabyte | powers of 1,000 (SI); 1,024 told in a remark |
| | `def:g4:memory-and-storage:backup` | backup | |
| g4/02 programs-and-operating-system | `def:g4:programs-and-operating-system:program` | program | |
| | `def:g4:programs-and-operating-system:application` | application | |
| | `def:g4:programs-and-operating-system:os` | operating system | |
| | `def:g4:programs-and-operating-system:start-up` | start-up | |
| | `def:g4:programs-and-operating-system:update` | installation; update | |
| | `def:g4:programs-and-operating-system:account` | user account | |
| g4/03 algorithms-repeat-and-decide | `def:g4:algorithms-repeat-and-decide:algorithm` | algorithm | |
| | `def:g4:algorithms-repeat-and-decide:loop` | loop → loop (repetition) | g6 adds *for loop*, *while loop* |
| | `def:g4:algorithms-repeat-and-decide:condition` | condition | g6/04 adds *compound condition* |

### Grade 5

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g5/01 bits-and-bytes | `def:g5:bits-and-bytes:bit` | bit | |
| | `def:g5:bits-and-bytes:binary` | binary number → binary | |
| g5/02 text-pictures-sound-as-numbers | `def:g5:text-pictures-sound-as-numbers:character-code` | character code; code table | *ASCII* is named in a history box only (Book 2 g10 owns it) |
| | `def:g5:text-pictures-sound-as-numbers:pixel` | pixel | |
| | `def:g5:text-pictures-sound-as-numbers:grey-level` | grey level | |
| | `def:g5:text-pictures-sound-as-numbers:rgb` | red–green–blue colour → RGB colour | |
| | `def:g5:text-pictures-sound-as-numbers:resolution` | resolution → resolution (of a picture) | |
| g5/03 networks-first-look | `def:g5:networks-first-look:network` | network | |
| | `def:g5:networks-first-look:internet` | Internet | |
| | `def:g5:networks-first-look:server` | server | |
| | `def:g5:networks-first-look:web` | web page; World Wide Web | |
| | `def:g5:networks-first-look:browser` | browser | |
| | `def:g5:networks-first-look:web-address` | web address | bare *address* never defined |
| | `def:g5:networks-first-look:link` | link → link (on a web page) | protect the verb *link(s)* |
| | `def:g5:networks-first-look:password` | password | Book 2 g12 and Book 5 recall |
| | `def:g5:networks-first-look:authentication` | authentication | sync ruling: Book 1 owns it; Book 2 recalls, Book 5 may re-found it |

### Grade 6

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g6/01 first-python-program | `def:g6:first-python-program:language` | programming language | |
| | `def:g6:first-python-program:interpreter` | interpreter | Book 2 g12 recalls; *compiler* is not defined in Book 1 |
| | `def:g6:first-python-program:source-file` | source file | |
| | `def:g6:first-python-program:comment` | comment | |
| | `def:g6:first-python-program:error-message` | error message | g7/05 adds the kinds of error |
| g6/02 variables-and-input | `def:g6:variables-and-input:variable` | variable | |
| | `def:g6:variables-and-input:assignment` | assignment | |
| | `def:g6:variables-and-input:value` | value | STOP outside g6/02 if it over-links |
| | `def:g6:variables-and-input:type` | type → type (of a value) | protect the verb *type/typed/typing* |
| | `def:g6:variables-and-input:conversion` | type conversion | |
| | (p) `def:g6:variables-and-input:trace-table` | trace table | **intra-book ownership**: map gives "tracing" to g7/05; proposal: the table here (first use), tracing with `print` and the kinds of error in g7/05 |
| g6/03 for-loops-turtle | `def:g6:for-loops-turtle:turtle` | turtle graphics | |
| | `def:g6:for-loops-turtle:for-loop` | for loop | named in words beside `\code{for}` |
| | `def:g6:for-loops-turtle:block` | block → indented block | |
| | `def:g6:for-loops-turtle:loop-variable` | loop variable | |
| | `def:g6:for-loops-turtle:nested-loop` | nested loop | |
| g6/04 if-else | `def:g6:if-else:comparison` | comparison | |
| | `def:g6:if-else:boolean` | Boolean value | |
| | `def:g6:if-else:conditional` | conditional statement; if statement | |
| | `def:g6:if-else:branch` | branch | |
| | `def:g6:if-else:compound-condition` | compound condition | the operators *and*, *or*, *not* are named in `\code` |
| g6/05 while-loops | `def:g6:while-loops:while-loop` | while loop | |
| | `def:g6:while-loops:counter` | counter | |
| | `def:g6:while-loops:running-total` | running total | |
| | `def:g6:while-loops:infinite-loop` | infinite loop | |

### Grade 7

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g7/01 functions | `def:g7:functions:function` | function | the mathematics books define a mathematical *function* (other series; linking is per book) |
| | `def:g7:functions:call` | function call | |
| | `def:g7:functions:parameter` | parameter; argument | |
| | `def:g7:functions:return-value` | return value | |
| | `def:g7:functions:local-variable` | local variable | |
| g7/02 lists | `def:g7:lists:list` | list | |
| | `def:g7:lists:item` | item → item (of a list) | *element* is kept for HTML (g9/01) |
| | `def:g7:lists:index` | index | |
| | `def:g7:lists:length` | length → length (of a list) | STOP outside g7 (side lengths in turtle and grids) |
| | `def:g7:lists:traversal` | list traversal | |
| g7/03 strings | `def:g7:strings:string` | string | Book 2 recalls |
| | `def:g7:strings:character` | character | protect "a character in the game/story" |
| | `def:g7:strings:slice` | slice | |
| | `def:g7:strings:string-method` | string method | contested: bare *method* (class sense) is Book 2 g12's |
| g7/04 how-a-processor-runs-a-program | `def:g7:how-a-processor-runs-a-program:cell` | memory cell | |
| | `def:g7:how-a-processor-runs-a-program:address` | memory address | |
| | `def:g7:how-a-processor-runs-a-program:machine-instruction` | machine instruction; machine language | *assembly language* is Book 2 g11's |
| | `def:g7:how-a-processor-runs-a-program:register` | register | |
| | `def:g7:how-a-processor-runs-a-program:pc` | program counter | |
| | `def:g7:how-a-processor-runs-a-program:cycle` | fetch–decode–execute cycle | |
| | `def:g7:how-a-processor-runs-a-program:clock` | clock → clock (of a processor) | protect everyday clocks |
| | `def:g7:how-a-processor-runs-a-program:core` | core → core (of a processor) | |
| g7/05 finding-and-fixing-bugs | `def:g7:finding-and-fixing-bugs:bug` | bug | |
| | `def:g7:finding-and-fixing-bugs:kinds` | syntax error; runtime error; logic error | |
| | `def:g7:finding-and-fixing-bugs:traceback` | traceback | |
| | `def:g7:finding-and-fixing-bugs:debugging` | debugging | |
| g7/06 project-quiz-game | — | — | project: no new term (*specification* is Book 2 g10's) |

### Grade 8

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g8/01 binary-and-hexadecimal | `def:g8:binary-and-hexadecimal:base` | base → number base | protect "base of a rectangle", Book 2's "base case" is another book |
| | `def:g8:binary-and-hexadecimal:hexadecimal` | hexadecimal; hexadecimal digit | |
| | `def:g8:binary-and-hexadecimal:carry` | carry → carry (in binary addition) | protect the verb *carry/carries* (packets carry data) |
| | `prop:g8:binary-and-hexadecimal:patterns` | (proposition) patterns of n bits | no `\index` |
| g8/02 dictionaries | `def:g8:dictionaries:dictionary` | dictionary | protect "a paper dictionary" (g8/04 hook) |
| | `def:g8:dictionaries:key` | key → dictionary key | sense 2 of 3 |
| | `def:g8:dictionaries:entry` | entry | |
| | `def:g8:dictionaries:record` | record | Book 2 recalls (g10 data tables) |
| | `def:g8:dictionaries:field` | field | |
| g8/03 files-and-data-tables | `def:g8:files-and-data-tables:text-file` | text file | |
| | `def:g8:files-and-data-tables:newline` | newline character → end of line | |
| | `def:g8:files-and-data-tables:csv` | CSV file | |
| | `def:g8:files-and-data-tables:table` | data table | bare *table* never defined (code table, truth table) |
| | `def:g8:files-and-data-tables:header-row` | header row | not bare *header* (packet header, g8/05) |
| | (p) `def:g8:files-and-data-tables:spreadsheet` | spreadsheet; formula → formula (of a spreadsheet) | only if the proposed section is accepted |
| g8/04 searching-and-sorting | `def:g8:searching-and-sorting:linear-search` | linear search | |
| | `def:g8:searching-and-sorting:binary-search` | binary search | |
| | `def:g8:searching-and-sorting:sorted` | sorted list | |
| | `def:g8:searching-and-sorting:selection-sort` | selection sort | |
| | `def:g8:searching-and-sorting:insertion-sort` | insertion sort | |
| g8/05 how-the-internet-works | `def:g8:how-the-internet-works:packet` | packet; packet header | |
| | `def:g8:how-the-internet-works:ip-address` | IP address | Book 2 g11 adds the mask |
| | `def:g8:how-the-internet-works:interface` | network interface | bare *interface* is Book 2 g11's (module interface) |
| | `def:g8:how-the-internet-works:switch` | network switch | bare *switch* is the physics books' electric switch |
| | `def:g8:how-the-internet-works:router` | router | *routing table* is Book 2 g11's |
| | `def:g8:how-the-internet-works:domain-name` | domain name; name system → domain name system (DNS) | |
| | `def:g8:how-the-internet-works:client` | client | |
| | `def:g8:how-the-internet-works:bit-rate` | bit rate | |
| | `def:g8:how-the-internet-works:latency` | latency | |
| g8/06 project-data-explorer | — | — | project: no new term |

### Grade 9

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| g9/01 html-and-css | `def:g9:html-and-css:html` | HTML | |
| | `def:g9:html-and-css:element` | element → HTML element; tag; start tag; end tag | |
| | `def:g9:html-and-css:attribute` | attribute | Book 2 g12 *attribute* (of an object) is another book |
| | `def:g9:html-and-css:document-tree` | document tree | |
| | `def:g9:html-and-css:css` | CSS; CSS rule; selector | |
| | `def:g9:html-and-css:class` | class → class (of an HTML element) | only sense in Book 1 |
| | `def:g9:html-and-css:box-model` | box model | |
| g9/02 logic-gates | `def:g9:logic-gates:gate` | logic gate | |
| | `def:g9:logic-gates:truth-table` | truth table | as `SERIES_DEFINITIONS.md` says: the truth table of a gate or circuit |
| | `def:g9:logic-gates:gates` | NOT gate; AND gate; OR gate; XOR gate | |
| | `def:g9:logic-gates:circuit` | logic circuit | bare *circuit* is the physics books' |
| | `def:g9:logic-gates:half-adder` | half adder | *full adder* is Book 2 g11's |
| | `prop:g9:logic-gates:de-morgan` | (proposition) De Morgan's laws → De Morgan's laws for gates | indexed in the proposition, owner chapter only |
| g9/03 grids-and-images | `def:g9:grids-and-images:grid` | grid | rows and columns described, never defined |
| | `def:g9:grids-and-images:cell` | cell → grid cell | g7/04 has *memory cell* |
| | `def:g9:grids-and-images:neighbour` | neighbour → neighbour (of a cell) | |
| | `def:g9:grids-and-images:pgm` | plain image file → PGM file | |
| | `met:g9:grids-and-images:blur` | (method) blur by averaging | no `\index` |
| g9/04 algorithms-on-numbers | `def:g9:algorithms-on-numbers:primality-test` | primality test | *prime number*, *divisor*, *gcd* are the mathematics books' |
| | `met:g9:algorithms-on-numbers:trial-division` | (method) trial division | `\index{trial division}` in the method |
| | `met:g9:algorithms-on-numbers:sieve` | (method) sieve of Eratosthenes | `\index` in the method |
| | (p) `met:g9:algorithms-on-numbers:sqrt-halving` | (method) square root by halving | no `\index` |
| | `prop:g9:algorithms-on-numbers:sqrt-bound` | (proposition) a divisor below the square root | no `\index` |
| | `prop:g9:algorithms-on-numbers:euclid-halves` | (proposition) Euclid's remainders halve in two steps | no `\index` (Euclid's algorithm is the mathematics books') |
| g9/05 randomness-and-simulation | `def:g9:randomness-and-simulation:prng` | pseudo-random number generator | |
| | `def:g9:randomness-and-simulation:seed` | seed | |
| | `def:g9:randomness-and-simulation:simulation` | simulation | |
| | `met:g9:randomness-and-simulation:estimate` | (method) estimation by simulation | `\index` in the method; *random walk* in prose only (mathematics Year 2) |
| g9/06 first-cryptography | `def:g9:first-cryptography:cipher` | cipher; plaintext; ciphertext | |
| | `def:g9:first-cryptography:encryption` | encryption; decryption | |
| | `def:g9:first-cryptography:key` | key → encryption key | sense 3 of 3 |
| | `def:g9:first-cryptography:shift-cipher` | shift cipher | |
| | `def:g9:first-cryptography:substitution-cipher` | substitution cipher | |
| | `def:g9:first-cryptography:frequency-analysis` | frequency analysis | *frequency* itself is the mathematics books' |
| | `def:g9:first-cryptography:brute-force` | brute-force search | |
| | `def:g9:first-cryptography:keyword-cipher` | keyword cipher | |
| g9/07 project-grid-game | — | — | project: no new term (the maze has gems and a gate, not keys and doors, to keep *key* out) |

### Typing appendix

| Chapter | Label | Term(s) | Notes |
|---|---|---|---|
| typ/01 typing-drills | — | — | no definition (g3/01 owns the technique); see §3 for its links |

**Count:** about 206 defined terms in 172 definitions (the (p) rows included), plus 9 methods and
propositions.

## 2. Words with more than one sense in Book 1

| Word | Senses and owners | Plan |
|---|---|---|
| key | keyboard key (g2/01), dictionary key (g8/02), encryption key (g9/06) | three definitions carry `\emph{key}` with distinct index keys; with `AMBIG_POLICY = "nearest-preceding"` each chapter links its own sense; the appendix (after grade 9 in reading order) must not link *key* to the cipher sense: `EXTRA_PROTECT` there |
| table | code table (g5/02), data table (g8/03), truth table (g9/02) | bare *table* never defined; STOP *table* |
| address | web address (g5/03), memory address (g7/04), IP address (g8/05) | bare *address* never defined |
| cell | memory cell (g7/04), grid cell (g9/03), spreadsheet cell (prose, g8/03) | emphasis on the qualified forms where possible; protect "cell" in g8/03 |
| header | header row (g8/03), packet header (g8/05) | qualified forms only |
| tree | folder tree (g3/03), document tree (g9/01) | bare *tree* never defined (Book 2 g12) |
| path | file path (g3/03); a packet's and a maze's path in prose | bare *path* never defined |
| row | home row (g3/01); grid rows (prose) | bare *row* never defined |
| type | type of a value (g6/02); the verb *to type* (g3/01 onwards) | protect the verb forms |
| link | link on a web page (g5/03); the verb *to link* | protect the verb forms |
| carry | carry in addition (g8/01); the verb *to carry* | protect the verb forms |
| character | character of a string (g7/03); a story's character | protect |
| clock, core, base, length, value, copy, move, click | the defined sense and the everyday one | STOP outside the defining chapter where prose shows over-linking |
| switch | network switch (g8/05); electric switch (physics books, g9/02 prose) | qualified form only |
| element / item | HTML element (g9/01); list item (g7/02) | separate words on purpose |

## 3. Phase C curation already foreseen (`tools/term_config/book1_en.py`)

- `STOP`: table, value, length, copy, move, click, drag (and *menu* if it over-links).
- `EXTRA_PROTECT`: the verbs `type[sd]?|typing` (outside g6/02's definition), `link(s|ed|ing)` as verbs,
  `carr(y|ies|ied|ying)` as verbs, "desktop computer", "paper dictionary", "a character in", "the base of",
  the keyboard senses of *key* and *row* in `parts/typing/` and in any later keyboard figure caption.
- `NO_CAPITAL`: Click, Drag, Save, Type (imperatives in exercises).
- The capitalised-harvest trap: *Internet*, *HTML*, *CSS*, *RAM*, *SSD*, *IP address*, *World Wide Web*
  are capitalised in their definitions on purpose; check that sentence-initial *Key*, *Type* and *Link*
  are not harvested as separate terms.

## 4. Notions this book recalls and never defines

- From the mathematics books: place value, powers, square root, divisor, prime number, greatest common
  divisor and Euclid's algorithm, probability, frequency, mean, angle, regular polygon, the area of a disc,
  negative numbers (named in prose, `recall` boxes, no `\cref`).
- From the physics books: electric circuit, switch, the speed of light in glass (told), the transistor
  (told as a switch).
- From Book 2 (named in prose as "a later year" only, never defined here): specification, assertion,
  test file, ASCII and Unicode by name, overflow, mutability and aliasing, join, event, state machine,
  sensor, actuator, permissions, routing table, cost of an algorithm, full adder, assembly language, the
  von Neumann model, class and method (programming), tree, stack, queue, compiler.

## 5. Sync rulings applied (2026-11-20)

- byte g4/01, bit and "8 bits" g5/01; trace table g6/02; interpreter g6/01 (no *compiler*); character code and
  code table g5/02 (ASCII in a history box); resolution g5; authentication g5/03; string method g7/03; folder
  tree g3, document tree g9; class of an HTML element g9/01; machine language and machine instruction g7/04;
  network switch, network interface, bit rate g8/05: **as this file already had them**.
- **port**: no definition (Book 2 g10-08 owns *port number*); g3/02 says "port" for a connector in prose. The
  row was removed.
- Never defined in Book 1, told in prose at most: assembly language, assembler, label, specification, full
  adder, routing table, network mask, event, permissions, sensor, actuator, protocol, port number, sampling
  rate, bit depth (g5/02 tells sound in prose only), side effect, paradigm, pure function, interrupt, compiler,
  tree, method, class (programming), random walk.
- Figures are uncounted: `fig:` labels allowed, never `\cref{fig:...}`.
