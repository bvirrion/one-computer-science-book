/* cheney_demo.c -- the server on a copying heap of 3000 cells (two halves of
   1500): 150 sessions of 8 cells, each a cycle, and 24 cells of short-lived work per request. */
// capture: with=cheney.c
#include <stdio.h>
#include "server.h"

int main(void)
{
    gc_init(3000);
    serve_init(150);
    long seen = 0;
    for (int r = 0; r < 2000; r++) {
        long marked = gc_stats.visited;
        if (!serve(r, 150, 8, 24, 1)) return printf("heap full\n"), 1;
        if (gc_stats.collections > seen && seen < 6) {
            seen = gc_stats.collections;
            printf("collection %ld during request %4d: copied %4ld\n", seen, r,
                   gc_stats.visited - marked);
        }
    }
    printf("2000 requests: %ld cells allocated, %ld collections, %ld copied\n",
           gc_stats.allocated, gc_stats.collections, gc_stats.visited);
    return 0;
}
