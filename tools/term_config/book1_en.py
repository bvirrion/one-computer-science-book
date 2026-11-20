"""Book 1 -- en. Curation only; the rules live in tools/termlink/.

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
# Ordinary words outside their defining chapter: "type w" (verb), "update" and
# "record" (verbs), "key" (keyboard, dictionary and encryption senses all occur),
# "window" (the blur's 3 by 3 window), "class" (a class of pupils), "branch" (a
# tree's branch), "block", "core", "length" (of a message), "field", "entry",
# "formula" (mathematics), "argument" (a proof's argument), "clock" (a wall clock,
# the time of day that seeds a generator).
STOP = {"type", "update", "record", "key", "window", "class", "branch", "block",
        "core", "length", "field", "entry", "formula", "argument", "clock"}
NO_CAPITAL = set()
EXTRA = {}
# "move" and "copy" name file operations in grade 3 but are everyday words
# everywhere else (a move of the maze game, a copy of a list).
DROP = {"move", "copy"}
DERIVED = {}
# The typing appendix: \omdrill and \ompassage arguments are the lines the
# reader types (the typing test reads them, and a link would print as text to
# type); and "index finger" is a finger, not a list index.
EXTRA_PROTECT = [r"\\ompassage\{[^{}]*\}\{[^{}]*\}", r"\\omdrill\{[^{}]*\}",
                 r"index\s+fingers?",
                 # A desktop computer is not the screen's desktop; "links" and
                 # "carry" as verbs; a broken network link is not a web link.
                 r"desktop(?=\s+(?:computers?|processor))",
                 r"links(?=\s+a\s+\\emph\{key)", r"link(?=\s+breaks)",
                 r"carry(?=\s+\$)"]
AMBIG_POLICY = "nearest-preceding"
