/* ms_demo.c -- the server on a mark-and-sweep heap of 3000 cells: 150 sessions of 8 cells,
   each a cycle, and 24 cells of short-lived work per request. */
// capture: with=marksweep.c
#include <stdio.h>
#include "server.h"

int main(void)
{
    gc_init(3000);
    serve_init(150);
    long seen = 0;
    for (int r = 0; r < 2000; r++) {
        long before = gc_stats.swept, marked = gc_stats.visited;
        if (!serve(r, 150, 8, 24, 1)) return printf("heap full\n"), 1;
        if (gc_stats.collections > seen && seen < 6) {
            seen = gc_stats.collections;
            printf("collection %ld during request %4d: marked %4ld, swept %4ld\n", seen, r,
                   gc_stats.visited - marked, gc_stats.swept - before);
        }
    }
    printf("2000 requests: %ld cells allocated, %ld collections, %ld marked, %ld swept\n",
           gc_stats.allocated, gc_stats.collections, gc_stats.visited, gc_stats.swept);
    return 0;
}
