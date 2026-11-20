/* cheney.c -- a copying collector: two semispaces; a collection copies the reachable cells
   breadth first into the empty one, with no stack: the copied cells are the queue. */
#include "heap.h"

int roots[MAX_ROOTS], nroots;
struct gc_stats gc_stats;
static struct cell space[2][MAX_CELLS / 2];
static struct cell *from, *to;  /* allocate in from-space; to-space is empty */
static int half, top;           /* semispace size, and the next free cell of from-space */

void gc_init(int cells)
{
    half = cells / 2;
    from = space[0];
    to = space[1];
    top = nroots = 0;
    gc_stats = (struct gc_stats){0};
}

struct cell *gc_cell(int c) { return &from[c]; }

static int forward(int c, int *next)  /* the cell's new index, copying it the first time */
{
    if (c == NIL) return NIL;
    if (from[c].meta == NIL) {      /* not copied yet */
        to[*next] = from[c];
        from[c].meta = (*next)++;   /* leave a forwarding pointer behind */
        gc_stats.visited++;
    }
    return from[c].meta;
}

static void collect(void)
{
    int scan = 0, next = 0;
    for (int r = 0; r < nroots; r++) roots[r] = forward(roots[r], &next);
    while (scan < next) {           /* to-space cells between scan and next are grey */
        for (int k = 0; k < 2; k++) to[scan].ref[k] = forward(to[scan].ref[k], &next);
        scan++;
    }
    struct cell *t = from;
    from = to;
    to = t;
    top = next;
    gc_stats.collections++;
}

int gc_alloc(int data, int r0, int r1)
{
    if (top == half) {
        roots[nroots++] = r0;       /* the arguments are roots, and may move */
        roots[nroots++] = r1;
        collect();
        r1 = roots[--nroots];
        r0 = roots[--nroots];
        if (top == half) return NIL;
    }
    from[top] = (struct cell){NIL, data, {r0, r1}};
    gc_stats.allocated++;
    return top++;
}
