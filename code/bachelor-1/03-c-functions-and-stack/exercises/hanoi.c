// hanoi.c: move n - 1 discs aside, move the largest, move the n - 1 back on top.
#include <string.h>
#include "hanoi.h"

long hanoi(int n, char from, char to, char via, char *out, int depth, int *max_depth)
{
    if (depth > *max_depth)
        *max_depth = depth;
    if (n == 0)
        return 0;
    long moves = hanoi(n - 1, from, via, to, out, depth + 1, max_depth);
    if (out) {
        char move[6] = {from, '-', '>', to, ' ', '\0'};
        strcat(out, move);
    }
    moves += 1 + hanoi(n - 1, via, to, from, out, depth + 1, max_depth);
    return moves;
}
