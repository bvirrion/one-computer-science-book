/* ex5_sweep_bug.c -- marksweep.c with one line left out of sweep. Find the effect, then the line. */
#include "../listings/heap.h"

int roots[MAX_ROOTS], nroots;
struct gc_stats gc_stats;
enum { WHITE = 0, MARKED = 1, FREE = 2 };  /* meta of a cell */
static struct cell heap[MAX_CELLS];
static int size, free_list, stack[MAX_CELLS];

void gc_init(int cells)
{
    size = cells;
    free_list = NIL;
    for (int c = cells - 1; c >= 0; c--) {  /* the free list is linked through ref[0] */
        heap[c] = (struct cell){FREE, 0, {free_list, NIL}};
        free_list = c;
    }
    nroots = 0;
    gc_stats = (struct gc_stats){0};
}

struct cell *gc_cell(int c) { return &heap[c]; }

static void mark(void)
{
    int top = 0;
    for (int r = 0; r < nroots; r++)
        if (roots[r] != NIL && heap[roots[r]].meta == WHITE) {
            heap[roots[r]].meta = MARKED;  /* grey: marked, on the stack */
            stack[top++] = roots[r];
        }
    while (top > 0) {
        int c = stack[--top];             /* black once its references are pushed */
        gc_stats.visited++;
        for (int k = 0; k < 2; k++) {
            int d = heap[c].ref[k];
            if (d != NIL && heap[d].meta == WHITE) {
                heap[d].meta = MARKED;
                stack[top++] = d;
            }
        }
    }
}

static void sweep(void)
{
    for (int c = 0; c < size; c++) {
        if (heap[c].meta == MARKED) {
        } else if (heap[c].meta == WHITE) {  /* unreachable: garbage */
            heap[c] = (struct cell){FREE, 0, {free_list, NIL}};
            free_list = c;
            gc_stats.swept++;
        }
    }
}

int gc_alloc(int data, int r0, int r1)
{
    if (free_list == NIL) {
        roots[nroots++] = r0;  /* the arguments are roots while we collect */
        roots[nroots++] = r1;
        mark();
        sweep();
        nroots -= 2;
        gc_stats.collections++;
        if (free_list == NIL) return NIL;
    }
    int c = free_list;
    free_list = heap[c].ref[0];
    heap[c] = (struct cell){WHITE, data, {r0, r1}};
    gc_stats.allocated++;
    return c;
}
