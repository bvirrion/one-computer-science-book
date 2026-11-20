/* server.h -- the town's server as the program whose heap is collected. It keeps the
   sessions of its last `keep` requests in roots 0 .. keep-1. Each request first builds a
   list of `temp` cells of short-lived work, then a session of `sess` cells, which replaces
   the oldest session. Root `keep` holds the list being built. */
#include "heap.h"

static int build(int slot, int n, int data, int cyclic)
{
    roots[slot] = NIL;
    for (int i = 0; i < n; i++) {
        int c = gc_alloc(data, roots[slot], NIL);
        if (c == NIL) return 0;
        roots[slot] = c;
    }
    if (cyclic) {  /* the last cell points back to the first: a cycle */
        int last = roots[slot];
        while (gc_cell(last)->ref[0] != NIL) last = gc_cell(last)->ref[0];
        gc_cell(last)->ref[1] = roots[slot];
    }
    return 1;
}

static void serve_init(int keep)
{
    nroots = keep + 1;
    for (int r = 0; r <= keep; r++) roots[r] = NIL;
}

static int serve(int r, int keep, int sess, int temp, int cyclic)  /* request number r */
{
    if (!build(keep, temp, r, 0) || !build(keep, sess, r, cyclic)) return 0;
    roots[r % keep] = roots[keep];
    roots[keep] = NIL;
    return 1;
}
