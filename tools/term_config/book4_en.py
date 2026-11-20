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
}
NO_CAPITAL = set()
EXTRA = {}
DROP = set()
DERIVED = {}
# "sequence" is not a sequent; a Poisson process is not an operating-system process; group commit is not a
# transaction's commit; the good-suffix rule is not a word's suffix; nineteen-fold is not a fold.
# "in process" means inside one process, not a link to its definition.
EXTRA_PROTECT = [r"sequences?\b", r"Poisson\s+process", r"the\s+process\s+(goes|starts|repeats|begins|continues)",
                 r"group\s+commit", r"good-suffix", r"\w+-fold",
                 r"[Ii]n\s+process\b", r"in-process"]
AMBIG_POLICY = "drop"
