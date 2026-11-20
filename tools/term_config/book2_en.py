"""Book 2 -- en. Curation only; the rules live in tools/termlink/.

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
# defining chapter: a cost (of a road, of an algorithm), a path (file, graph), a
# set (Python type, everyday), a state (machine, process, toy machine), a route
# (web dispatcher vs road route vs network route), a class (Python vs k-NN label),
# a method (HTTP vs class), a header (table vs packet), a frame (call stack vs link
# layer), a node/root/parent/child (tree vs file system vs network), a stack/queue
# (structure vs call stack, print queue), a shift (bit shift vs Horspool shift), a
# sign (of a number vs a signature), a salt/digest/flag/pipe/shell/form/session in
# their everyday senses, a process (OS vs any process), a module (Python vs course).
STOP = {
    "cost", "correct", "path", "set", "state", "states", "command", "option", "parameter",
    "route", "sign", "size", "depth", "constant", "character", "encoding", "domain",
    "edge", "edges", "event", "events", "frame", "node", "nodes", "root", "parent",
    "child", "merge", "pattern", "query", "request", "response", "session", "shift",
    "selection", "projection", "stable", "stably", "objective", "occurrence",
    "alignment", "balanced", "canonical", "connected", "converged", "convergence",
    "degenerate", "descriptor", "distance", "methods", "method", "attribute",
    "attributes", "rows", "process", "cycle", "push", "pop", "queue", "stack",
    "module", "flag", "centre", "radius", "diameter", "degree", "neighbour",
    "neighbours", "feature", "features", "scheme", "fragment", "form", "quantum",
    "salt", "digest", "exponent", "prefix", "overflow", "redundancy", "cells", "alias",
    "aliases", "metadata", "pipe", "shell", "protocol", "compression", "simulator",
    "scaling", "decoder", "bus", "relation", "tree", "successor", "successors",
    "transition", "transitions", "termination", "timeout", "user", "variant", "class",
    "header", "subtree", "subproblem", "best case", "worst case", "compiler", "anomalies",
    "Compression", "Scaling", "Grouping", "Unpacking", "Recursion", "recursion",
    "predecessor", "predecessors", "aggregate", "tuple", "certificate", "assertion",
    "specification", "vertex", "vertices", "test case",
    # a road's or a string's length (not a path's), a Horspool jump, a k-NN label vs an
    # assembly label, "joins" as a verb, a user group vs GROUP BY, the town's Library,
    # a BFS layer vs a network layer, the menu as a text interface, a problem instance
    "length", "lengths", "Lengths", "jump", "jumps", "label", "labels", "join", "joins",
    "group", "groups", "library", "Library", "layer", "Layer", "layers", "interface",
    "interfaces", "instance",
}
NO_CAPITAL = set()
EXTRA = {}
DROP = set()
DERIVED = {}
EXTRA_PROTECT = []
AMBIG_POLICY = "nearest-preceding"
