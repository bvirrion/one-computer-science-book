/* sweep_bug_test.c: exercise 5, with the marks never cleared the heap fills up. */
#include <assert.h>
#include <stdio.h>
#include "../exercises/ex5_sweep_bug.c"
#include "../listings/server.h"

int main(void)
{
    gc_init(3000);
    serve_init(150);
    int r = 0;
    while (r < 2000 && serve(r, 150, 8, 24, 1)) r++;
    assert(r == 367 && gc_stats.collections == 17);  /* full during request 367 */
    printf("sweep bug: heap full during request %d, after %ld collections\n", r,
           gc_stats.collections);
    return 0;
}
