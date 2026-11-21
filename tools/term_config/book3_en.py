"""Book 3 -- en. Curation only; the rules live in tools/termlink/.

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
# Ordinary words, or words with several senses in this book, linked only in their
# defining chapter: an index (staging area vs inverted index vs array index), a heap
# (memory region vs structure), a stack/queue (call stack vs structure), a register
# (processor vs circuit), a loop (program vs graph), a literal (C vs logic), a union
# (C vs set vs relational), a branch (Git vs if vs branch and bound), a path, a root,
# a cut, a capacity (array vs knapsack), a pipeline (shell vs compilation), a
# selection/projection/division/relation (relational vs everyday), an enumeration (C
# enum vs listing solutions), feasible (path vs solution), an ancestor (tree vs
# commit), a bisection (history vs search), a variant (loop variant vs a version).
STOP = {
    "index", "heap", "stack", "queue", "register", "loop", "literal", "literally", "union",
    "branch", "path", "root", "children", "cut", "crosses", "capacity", "pipeline",
    "selection", "projection", "division", "relation", "relationship", "renaming",
    "enumeration", "feasible", "feasibility", "ancestor", "bisection", "variant",
    "termination", "terminates", "domain", "edges", "entity", "essential", "fields",
    "filter", "full", "keys", "minimal", "model", "monotone", "prime", "rank", "relax",
    "simple", "specification", "stable", "stably", "stability", "states", "structure",
    "symbol", "target", "transition", "tuple", "view", "width", "cells", "complete",
    "connected", "constraints", "counter", "cycle", "degree", "depth", "diameter",
    "centre", "distance", "implementation", "interface", "inversion", "clause",
    "successor", "multiplicity", "prerequisite", "prerequisites", "recipe",
    "representative", "shadows", "attributes", "address", "scope",
    # a data stream (not a C stream), NULL padding of an outer join, metric pivots
    "stream", "streams", "padding", "Padding", "pivot", "pivots", "Pivot",
}
NO_CAPITAL = set()
EXTRA = {}
DROP = set()
DERIVED = {}
# "in place of" (instead of), and a cost that is an algorithm's, not a code's.
# Reader R3-037/R3-041: the size of an element (not a dynamic array's size), the
# memory cells of a dynamic array (not list cells), the rotations of a board (not
# tree rotations), knapsack items ranked by value per unit of weight (not passing by
# value), and an explicit loop (not a graph's loop).
EXTRA_PROTECT = [r"in\s+place\s+of", r"cost\s+of\s+the\s+algorithm", r"Sorting\s+costs",
                 r"size\s+of\s+an\s+element", r"1\s+to\s+4\s+cells",
                 r"rotations\s+(?:or|and)\s+reflections", r"four\s+rotations",
                 r"by\s+value\s+per\s+unit", r"work\s+in\s+a\s+loop"]
AMBIG_POLICY = "drop"
