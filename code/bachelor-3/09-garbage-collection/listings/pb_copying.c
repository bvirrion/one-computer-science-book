/* pb_copying.c -- the weekend problem: the server under the copying collector, for heaps of
   H cells given as multiples of the live data L, against the model L / (H/2 - L). */
// capture: with=cheney.c args=2.5 3 4 6 8 12 16
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
    printf("L = %d live cells, %d requests of %d cells\n", live, REQUESTS, SESS + TEMP);
    printf("%5s %6s %11s %9s %13s %8s\n", "H/L", "H", "collections", "copied", "copied/alloc",
           "model");
    for (int a = 1; a < argc; a++) {
        double ratio = atof(argv[a]);
        int h = (int)(ratio * live);
        gc_init(h);
        serve_init(KEEP);
        for (int r = 0; r < REQUESTS; r++)
            if (!serve(r, KEEP, SESS, TEMP, 0)) return printf("heap full at H = %d\n", h), 1;
        double per = (double)gc_stats.visited / (double)gc_stats.allocated;
        double l = (double)gc_stats.visited / (double)gc_stats.collections;  /* live, mean */
        printf("%5.1f %6d %11ld %9ld %13.3f %8.3f\n", ratio, h, gc_stats.collections,
               gc_stats.visited, per, l / (h / 2.0 - l));
    }
    return 0;
}
