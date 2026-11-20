/* arena_test.c: the boundary tags stay consistent, freeing coalesces, and exercises 1 and 9. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "../listings/arena.c"

static void check(void)  /* blocks tile the arena, tags agree, no two free blocks touch */
{
    size_t total = 0, i = 1;
    int prev_free = 0;
    for (; size(i) > 0; i = next(i)) {
        assert(size(i) % 16 == 0 && size(i) >= MIN_BLOCK);
        assert(heap[i] == heap[i + size(i) / W - 1]);
        assert(!(prev_free && !used(i)));
        prev_free = !used(i);
        total += size(i);
    }
    assert(i == N - 1 && total == (N - 2) * W);
}

static size_t offset(void *p) { return ((size_t)((size_t *)p - heap) - 2) * W; }  /* of its block */

static void four_holes(arena_fit fit)  /* free blocks of 96, 48, 160 and 64 bytes, in order */
{
    size_t pay[] = {80, 16, 32, 16, 144, 16, 48, 16};
    void *p[8];
    arena_init(fit);
    for (int k = 0; k < 8; k++) p[k] = arena_alloc(pay[k]);
    for (int k = 0; k < 8; k += 2) arena_free(p[k]);
    check();
}

static uint32_t seed = 7;
static uint32_t rnd(uint32_t n) { seed = seed * 1103515245u + 12345u; return (seed >> 8) % n; }

int main(void)
{
    arena_fit fits[] = {first_fit, best_fit};
    for (int f = 0; f < 2; f++) {  /* random workload, checked after every operation */
        void *live[300] = {0};
        arena_init(fits[f]);
        for (int step = 0; step < 20000; step++) {
            int k = (int)rnd(300);
            if (live[k]) arena_free(live[k]), live[k] = NULL;
            else live[k] = arena_alloc(1 + rnd(rnd(4) ? 100 : 3000));
            check();
        }
        for (int k = 0; k < 300; k++)
            if (live[k]) arena_free(live[k]);
        struct arena_stats s = arena_stats();  /* everything freed: one block again */
        assert(s.free_blocks == 1 && s.used_blocks == 0 && s.free_bytes == (N - 2) * W);
    }
    arena_init(first_fit);  /* coalescing on both sides */
    void *a = arena_alloc(40), *b = arena_alloc(40), *c = arena_alloc(40);
    arena_free(b);
    assert(arena_stats().free_blocks == 2);
    arena_free(a);
    assert(arena_stats().free_blocks == 2 && size(1) == 128);
    arena_free(c);
    assert(arena_stats().free_blocks == 1);

    four_holes(first_fit);  /* exercise 1 */
    assert(offset(arena_alloc(40)) == 0 && offset(arena_alloc(24)) == 128);
    assert(offset(arena_alloc(130)) == 208 && offset(arena_alloc(80)) == 496);
    four_holes(best_fit);
    assert(offset(arena_alloc(40)) == 400 && offset(arena_alloc(24)) == 128);
    assert(offset(arena_alloc(130)) == 208 && offset(arena_alloc(80)) == 0);

    for (int f = 0; f < 2; f++) {  /* exercise 9: holes of 2000 then 1504 bytes */
        arena_init(fits[f]);
        void *h1 = arena_alloc(2000 - 16), *u1 = arena_alloc(16);
        void *h2 = arena_alloc(1504 - 16), *u2 = arena_alloc(16);
        void *rest = arena_alloc(ARENA_BYTES - 2000 - 1504 - 64 - 16 - 16);
        assert(rest && arena_stats().free_blocks == 0);
        arena_free(h1);
        arena_free(h2);
        void *x = arena_alloc(1408 - 16), *y = arena_alloc(1504 - 16), *z = arena_alloc(592 - 16);
        assert(x && y && u1 && u2);
        if (f == 0) assert(z != NULL);  /* first fit: 1408 from the 2000 leaves 592 */
        else assert(z == NULL);         /* best fit: 1408 from the 1504 leaves a useless 96 */
        check();
    }
    printf("arena: all checks passed\n");
    return 0;
}
