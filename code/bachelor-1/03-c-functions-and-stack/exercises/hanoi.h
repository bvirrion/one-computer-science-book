// hanoi.h: the towers of Hanoi (exercise 11).
#ifndef HANOI_H
#define HANOI_H

// Moves n discs from peg `from` to peg `to`; writes each move as "a->c " into
// out (if not NULL); returns the number of moves; *max_depth gets the deepest
// level of recursion reached (the first call is at depth 1).
long hanoi(int n, char from, char to, char via, char *out, int depth, int *max_depth);

#endif
