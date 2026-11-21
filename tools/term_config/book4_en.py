"""Book 4 -- en. Curation only; the rules live in tools/termlink/.

The book's writer curates this file in Phase C. Computer-science homographs to
check against each target: a table (a data table, a hash table, a truth table,
a routing table, a page table), a key (keyboard key, dictionary key, primary key,
cryptographic key), a file, a list, a set, a string, a record, a field, a tree,
a node, a root, a leaf, a stack, a queue, a heap (structure vs memory region), a
graph, a path, a word, a type, a class, an object, an instance, a value, a
call, a frame, a page, a block, a cell, a port, a bus, a register, a memory, a
link, a server, a process, a thread, a lock, a state, a token, an image, a pixel,
a sort (to sort vs a sort of), a search, a loop, a bug.
Use STOP (ordinary word outside its defining chapter), DROP (never a link),
NO_CAPITAL (skip sentence-initial matches), EXTRA (manual term -> label),
EXTRA_PROTECT (regex phrases in another sense; multi-word patterns use \\s+).
Watch the capitalised-harvest trap: a display opening its sentence is harvested
capitalised, and STOP/DROP match case-sensitively.
"""
STOP = {
    # ordinary words, or another sense elsewhere in the book: linked only inside their defining chapter
    "accessible", "accuracy", "ambiguous", "border", "bound", "box", "cache", "captures", "child", "parent",
    "class", "closure", "collision", "compact", "concept", "consistency", "consistent", "constraint",
    "cumulative", "cumulatively", "cut", "decomposition", "derivation", "drop", "enumeration", "example",
    "exhaustive", "exhaustively", "factor", "fair", "fairness", "feature", "features", "filter", "flow",
    "fork", "frame", "frames", "free", "generated", "handlers", "hit", "miss", "immediate", "implies",
    "index", "invalidates", "isolation", "label", "language", "latency", "lazy", "leftmost", "rightmost",
    "linear", "link", "linkage", "local", "locally", "lossless", "matching", "minimal", "model", "move",
    "object", "occurrence", "orphan", "pattern", "persistence", "persistent", "positions", "product",
    "reference", "regular", "resource", "scope", "sentence", "sequence", "signal", "sink", "source",
    "slice", "sound", "strategy", "streams", "structure", "substitution", "terminals", "terms",
    "throughput", "trim", "trivial", "trivially", "valid", "value", "window", "winning", "word",
    "residual", "residuals", "pure", "composition", "compositions", "Composition",
    # capitalised harvests of the same
    "Blocking", "Coherence", "Resolution",
    # loop blocking (caches) against blocking calls (sockets) and head-of-line blocking
    "blocking",
    # the MAC broadcast address (ch. 17) is not the IP one (ch. 18)
    "broadcast address",
}
NO_CAPITAL = set()
# Book 2 owns process, system call, race condition, critical section, mutual exclusion and lock
# (sources/SERIES_DEFINITIONS.md); Book 4 recalls them in remarks that keep the old labels, linked here.
EXTRA = {
    "process": "def:b2:processes-and-system-calls:process",
    "processes": "def:b2:processes-and-system-calls:process",
    "process identifier": "def:b2:processes-and-system-calls:process",
    "system call": "def:b2:processes-and-system-calls:syscall",
    "system calls": "def:b2:processes-and-system-calls:syscall",
    "race condition": "def:b2:threads-and-synchronisation:race",
    "race conditions": "def:b2:threads-and-synchronisation:race",
    "critical section": "def:b2:threads-and-synchronisation:mutex-property",
    "critical sections": "def:b2:threads-and-synchronisation:mutex-property",
    "mutual exclusion": "def:b2:threads-and-synchronisation:mutex-property",
    "Mutual exclusion": "def:b2:threads-and-synchronisation:mutex-property",
    "lock": "def:b2:threads-and-synchronisation:lock",
    "locks": "def:b2:threads-and-synchronisation:lock",
    "Lock": "def:b2:threads-and-synchronisation:lock",
}
DROP = set()
DERIVED = {}
# "sequence" is not a sequent; a Poisson process is not an operating-system process; group commit is not a
# transaction's commit; the good-suffix rule is not a word's suffix; nineteen-fold is not a fold.
# "in process" means inside one process, not a link to its definition.
EXTRA_PROTECT = [r"sequences?\b", r"Poisson\s+process", r"[Tt]he\s+process\s+(goes|starts|repeats|begins|continues)",
                 r"group\s+commit", r"good-suffix", r"\w+-fold",
                 r"[Ii]n\s+process\b", r"in-process",
                 # Reader report 2026-11-21 (R4-018 ... R4-110): the same surface word in another sense.
                 # A C++ move, a C table's move, a moved element: not Rust's move.
                 r"a\s+move\s+transfers", r"a\s+move\s+would\s+also", r"which\s+moves\s+every\s+slot",
                 r"nodes\s+do\s+not\s+move", r"is\s+moved\s+from\s+the\s+back",
                 # a file's, an address's, a position's owner; a library's or a port's borrowing
                 r"size,\s+owner", r"the\s+owner\s+and\s+group", r"chosen\s+by\s+its\s+owner",
                 r"the\s+owner\s+of\s+the\s+position", r"may\s+(not\s+)?borrow(?!\s+that\s+function)", r"allowed\s+to\s+borrow",
                 r"connections\s+borrow", r"members\s+who\s+borrow", r"borrow\s+books", r"which\s+borrows\s+them",
                 # an exception to a rule, folding a sum, cross-validation folds, an IP header field
                 r"is\s+an\s+exception\s+that", r"is\s+the\s+exception", r"tolerates\s+one\s+exception", r"never\s+folds",
                 r"five\s+folds", r"offset\s+field\s+has\s+13",
                 # constructors of an inductive set, of a list, Rust's associated functions, smart constructors
                 r"base\s+elements\s+and\s+constructors", r"each\s+constructor\s+assuming",
                 r"a\s+constructor\s+returning", r"list\s+constructor", r"smart\s+constructors",
                 r"force\s+a\s+constructor",
                 # the verb "tries", regex atomic groups, an atomic case of an induction
                 r"tries\s+(widening|to\b|the\s+subsets|again)", r"atomic\s+groups", r"atomic\s+case",
                 # an upper bound, a proof to complete, a flow's values on edges, "for example"
                 r"bounds\s+the\s+size", r"gives\s+the\s+bound", r"[Tt]he\s+bound\s+(is|gives)",
                 r"Complete\s+the\s+proof", r"whose\s+values\s+are", r"integer\s+values", r"with\s+values\s+in",
                 r"[Ff]or\s+example", r"example\s+for\b",
                 # Armstrong's decomposition rule is not a table's decomposition
                 r"decomposition\}\s+rule", r"by\s+decomposition\b", r"Decomposition:",
                 # a burst of requests, empty tokens, machine words, linear time
                 r"burst\s+of\s+requests", r"empty\s+words\s+between", r"machine\s+word", r"64-bit\s+word",
                 r"linear\s+time", r"exponential\s+to\s+linear",
                 # a DNS record's lifetime, HTTP/2 multiplexing, a compound
                 r"TTL,\s+time\s+to\s+live", r"Multiplexing\s+removes", r"two-router",
                 r"listing\s+processes", r"sequential\s+processes"]
AMBIG_POLICY = "drop"
