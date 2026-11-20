/* gen.c -- two generations. New cells go to a small nursery; a minor collection copies the
   nursery's reachable cells into the old generation (promotion). When the old generation
   is too full to take a whole nursery, a major collection copies everything reachable into
   its other half. An old cell that points into the nursery must be in the remembered set;
   the server never writes into a cell after creating it, so its set stays empty. */
#include "heap.h"

int roots[MAX_ROOTS], nroots;
struct gc_stats gc_stats;
long minors, majors, promoted, copied_major;
int remembered[MAX_CELLS], nremembered;  /* old cells that may point into the nursery */
static struct cell mem[MAX_CELLS];
static int old, nursery;         /* sizes: old is [0, old) or [old, 2 old), then the nursery */
static int base, top, young_top; /* the old half in use, its next free cell, the nursery's */

void gc_init_gen(int nursery_cells, int cells)
{
    nursery = nursery_cells;
    old = (cells - nursery) / 2;
    base = top = nroots = nremembered = 0;
    young_top = 2 * old;
    minors = majors = promoted = copied_major = 0;
    gc_stats = (struct gc_stats){0};
}

void gc_init(int cells) { gc_init_gen(cells / 10, cells); }  /* a tenth for the nursery */
struct cell *gc_cell(int c) { return &mem[c]; }
static int young(int c) { return c >= 2 * old; }

static int copy(int c, int *next, int all)  /* forward c to *next if it must move */
{
    if (c == NIL || !(all || young(c))) return c;
    if (mem[c].meta == NIL) {
        mem[*next] = mem[c];
        mem[c].meta = (*next)++;
    }
    return mem[c].meta;
}

static void scan_from(int scan, int *next, int all)  /* Cheney's loop */
{
    for (int r = 0; r < nroots; r++) roots[r] = copy(roots[r], next, all);
    for (; scan < *next; scan++)
        for (int k = 0; k < 2; k++) mem[scan].ref[k] = copy(mem[scan].ref[k], next, all);
}

static void minor(void)  /* nursery -> old */
{
    int start = top;
    for (int i = 0; i < nremembered; i++)  /* the remembered cells are roots too */
        for (int k = 0; k < 2; k++)
            mem[remembered[i]].ref[k] = copy(mem[remembered[i]].ref[k], &top, 0);
    nremembered = 0;
    scan_from(start, &top, 0);
    promoted += top - start;
    young_top = 2 * old;
    minors++;
}

static void major(void)  /* old and nursery -> the other old half */
{
    int other = base == 0 ? old : 0, next = other;
    scan_from(other, &next, 1);
    copied_major += next - other;
    nremembered = 0;
    base = other;
    top = next;
    young_top = 2 * old;
    majors++;
}

int gc_alloc(int data, int r0, int r1)
{
    if (young_top == 2 * old + nursery) {
        roots[nroots++] = r0;
        roots[nroots++] = r1;
        int full = base + old - top < nursery;  /* could the old generation take the nursery? */
        if (full) major(); else minor();
        r1 = roots[--nroots];
        r0 = roots[--nroots];
        gc_stats.collections++;
        if (full && base + old - top < nursery) return NIL;  /* live data fill the heap */
    }
    mem[young_top] = (struct cell){NIL, data, {r0, r1}};
    gc_stats.allocated++;
    return young_top++;
}
