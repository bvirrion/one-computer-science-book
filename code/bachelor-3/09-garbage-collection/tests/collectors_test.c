/* collectors_test.c: mark and sweep keeps every session intact, cycles included,
   and fails cleanly when the live data do not fit. */
#include <assert.h>
#include <stdio.h>
#include "../listings/marksweep.c"
#include "../listings/server.h"

static void sessions_intact(int done, int keep, int sess, int cyclic)
{
    for (int r = done - keep; r < done; r++) {
        int c = roots[r % keep], n = 0, head = c;
        for (; c != NIL; c = gc_cell(c)->ref[0], n++) {
            assert(gc_cell(c)->data == r);
            if (gc_cell(c)->ref[0] == NIL && cyclic) assert(gc_cell(c)->ref[1] == head);
        }
        assert(n == sess);
    }
}

int main(void)
{
    gc_init(3000);
    serve_init(150);
    for (int r = 0; r < 2000; r++) assert(serve(r, 150, 8, 24, 1));
    sessions_intact(2000, 150, 8, 1);
    assert(gc_stats.collections == 34 && gc_stats.allocated == 64000);
    gc_init(1220);  /* 1200 live cells and a request in progress do not fit: a clean failure */
    serve_init(150);
    int ok = 1;
    for (int r = 0; r < 2000 && ok; r++) ok = serve(r, 150, 8, 24, 1);
    assert(!ok);
    printf("mark and sweep: sessions intact after 34 collections\n");
    return 0;
}
