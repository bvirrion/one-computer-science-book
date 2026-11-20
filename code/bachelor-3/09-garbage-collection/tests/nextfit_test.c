/* nextfit_test.c: exercise 6, next fit keeps the arena consistent and its rover on a block. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "../exercises/ex6_next_fit.c"

static int is_block(size_t r)
{
    for (size_t i = 1; size(i) > 0; i = next(i))
        if (i == r) return 1;
    return 0;
}

static uint32_t seed = 11;
static uint32_t rnd(uint32_t n) { seed = seed * 1103515245u + 12345u; return (seed >> 8) % n; }

int main(void)
{
    void *live[300] = {0};
    long failed = 0;
    next_fit_init();
    for (int step = 0; step < 20000; step++) {
        int k = (int)rnd(300);
        if (live[k]) next_fit_free(live[k]), live[k] = NULL;
        else failed += (live[k] = arena_alloc(1 + rnd(rnd(4) ? 100 : 3000))) == NULL;
        assert(is_block(rover));
    }
    for (int k = 0; k < 300; k++)
        if (live[k]) next_fit_free(live[k]);
    assert(arena_stats().free_blocks == 1);
    next_fit_init();  /* the search goes on from the last block it used */
    void *a = arena_alloc(40), *b = arena_alloc(40), *c = arena_alloc(40);
    (void)c;
    next_fit_free(a);
    void *d = arena_alloc(40);  /* first fit would reuse a's block; next fit goes on past c */
    assert(d != a && d > b);
    printf("next fit: consistent (%ld requests failed)\n", failed);
    return 0;
}
