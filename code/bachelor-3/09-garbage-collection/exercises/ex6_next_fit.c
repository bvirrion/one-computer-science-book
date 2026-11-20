/* ex6_next_fit.c -- next fit: each search starts at the block where the last one stopped.
   It includes arena.c to reach its static helpers. */
#include "../listings/arena.c"

static size_t rover = 1;  /* always the start of a block */

size_t next_fit(size_t bytes)
{
    size_t i = rover;
    do {
        if (!used(i) && size(i) >= bytes) return rover = i;
        i = next(i);
        if (size(i) == 0) i = 1;  /* past the last block: wrap round to the first */
    } while (i != rover);
    return 0;
}

void next_fit_init(void)
{
    rover = 1;
    arena_init(next_fit);
}

void next_fit_free(void *p)  /* arena_free, keeping the rover on the start of a block */
{
    size_t i = (size_t)((size_t *)p - heap) - 1, n = next(i);
    size_t start = used(i - 1) ? i : i - size(i - 1) / W;  /* where the merged block starts */
    if (rover == i || (rover == n && !used(n))) rover = start;
    arena_free(p);
}
