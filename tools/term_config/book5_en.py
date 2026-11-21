"""Book 5 -- en. Curation only; the rules live in tools/termlink/.

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
    "abstraction", "affine", "application", "asset", "capability", "checkpoint", "clustered", "configuration",
    "container", "correct", "covering", "cut", "deadline", "definition", "dominates", "efficiency",
    "encoding", "frame", "garbage", "guest", "host", "handle", "kernel", "leader", "linear", "live",
    "liveness", "Liveness", "monitor", "order", "padding", "Padding", "page", "pages", "parallelism",
    "preservation", "Preservation", "progress", "Progress", "safe", "quadruple", "temporary", "tile",
    "semantic", "serial", "serially", "shadows", "shrinking", "Shrinking", "stub", "token", "trap", "trigger",
    "verifier", "work", "requirement", "reachable", "reachability", "non-trivial",
}
NO_CAPITAL = set()
EXTRA = {}
DROP = set()
DERIVED = {}
# "order" in another sense than a B+ tree's order (sorted, key, round-robin order); "to handle" the verb;
# conjunctive normal form is not a lambda-calculus normal form; a bar-code scanner is not a lexical scanner.
EXTRA_PROTECT = [r"sorted\s+order", r"key\s+order", r"round-robin\s+order", r"increasing\s+order",
                 r"another\s+order", r"the\s+order\s+of\s+its\s+key", r"to\s+handle\b",
                 r"(conjunctive|disjunctive)\s+normal\s+form", r"let\s+a\s+scanner\b",
                 # reader report R5-011, -015, -027, -041, -053, -058: ordinary words, or another sense
                 r"is\s+correct\s+by\s+hypothesis", r"definition\s+of\s+interference",
                 r"transition\s+function\s+gives\s+the\s+next\s+state", r"level\s+above\s+spills",
                 r"recognisable\s+bytes", r"revocation\s+is\s+one\s+deletion"]
AMBIG_POLICY = "drop"
