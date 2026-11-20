/* pb_marksweep.c -- the same server under mark and sweep: marking costs the live cells,
   sweeping the whole heap, against the model (L + H) / (H - L). */
// capture: with=marksweep.c args=1.25 1.5 2 3 4 6 8 16
#include <stdio.h>
#include <stdlib.h>
#include "server.h"

#define KEEP 500
#define SESS 4
#define TEMP 12
#define REQUESTS 20000

int main(int argc, char **argv)
{
    int live = KEEP * SESS;
    printf("%5s %6s %11s %9s %9s %11s %8s\n", "H/L", "H", "collections", "marked", "swept",
           "work/alloc", "model");
    for (int a = 1; a < argc; a++) {
        double ratio = atof(argv[a]);
        int h = (int)(ratio * live);
        gc_init(h);
        serve_init(KEEP);
        for (int r = 0; r < REQUESTS; r++)
            if (!serve(r, KEEP, SESS, TEMP, 0)) return printf("heap full at H = %d\n", h), 1;
        long work = gc_stats.visited + gc_stats.collections * (long)h;  /* mark + sweep */
        double l = (double)gc_stats.visited / (double)gc_stats.collections;
        printf("%5.2f %6d %11ld %9ld %9ld %11.3f %8.3f\n", ratio, h, gc_stats.collections,
               gc_stats.visited, gc_stats.swept, (double)work / (double)gc_stats.allocated,
               (l + h) / (h - l));
    }
    return 0;
}
