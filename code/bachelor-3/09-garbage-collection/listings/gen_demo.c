/* gen_demo.c -- the server of the weekend problem under the generational collector:
   12000 cells in all, with a nursery of 250 to 2000 of them. */
// capture: with=gen.c
#include <stdio.h>
#include "server.h"

void gc_init_gen(int nursery_cells, int cells);
extern long minors, majors, promoted, copied_major;

int main(void)
{
    printf("%8s %7s %7s %9s %13s %13s\n", "nursery", "minor", "major", "promoted", "copied major",
           "copied/alloc");
    int sizes[] = {250, 500, 1000, 2000};
    for (int i = 0; i < 4; i++) {
        gc_init_gen(sizes[i], 12000);
        serve_init(500);
        for (int r = 0; r < 20000; r++)
            if (!serve(r, 500, 4, 12, 0)) return printf("heap full\n"), 1;
        printf("%8d %7ld %7ld %9ld %13ld %13.3f\n", sizes[i], minors, majors, promoted,
               copied_major, (double)(promoted + copied_major) / (double)gc_stats.allocated);
    }
    return 0;
}
