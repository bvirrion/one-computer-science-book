/* frag.c -- the same seeded workload under first fit and best fit: failed requests,
   internal and external fragmentation, and the free blocks left at the end. */
// capture: with=arena.c
#include <stdint.h>
#include <stdio.h>
#include "arena.h"

#define STEPS 20000
#define LIVE 280
static uint32_t seed;
static uint32_t rnd(uint32_t n) { seed = seed * 1103515245u + 12345u; return (seed >> 8) % n; }

static size_t request(void)  /* mostly small objects, now and then a large buffer */
{
    return rnd(10) < 8 ? 8 + rnd(120) : 400 + rnd(1600);
}

static void run(const char *name, arena_fit fit)
{
    void *live[LIVE] = {0};
    size_t asked[LIVE] = {0}, failed = 0, payload = 0, blocks = 0, free_min = ARENA_BYTES;
    arena_init(fit);
    seed = 2026;
    for (int step = 0; step < STEPS; step++) {
        int k = (int)rnd(LIVE);
        if (live[k]) {
            arena_free(live[k]);
            live[k] = NULL;
        } else if ((live[k] = arena_alloc(asked[k] = request())) == NULL) {
            failed++;  /* refused: how much was free all the same? */
            size_t f = arena_stats().free_bytes;
            if (f < free_min) free_min = f;
        }
    }
    for (int k = 0; k < LIVE; k++)
        if (live[k]) payload += asked[k], blocks += arena_block_bytes(asked[k]);
    struct arena_stats s = arena_stats();
    double internal = 100.0 * (double)(blocks - payload) / (double)blocks;
    double external = 100.0 * (1.0 - (double)s.largest_free / (double)s.free_bytes);
    printf("%-9s failed %4zu, with at least %5zu B free each time\n", name, failed, free_min);
    printf("%-9s used %5zu B in %3zu blocks (internal %4.1f %%)\n", "", s.used_bytes,
           s.used_blocks, internal);
    printf("%-9s free %5zu B in %3zu blocks, largest %5zu B (external %4.1f %%)\n", "",
           s.free_bytes, s.free_blocks, s.largest_free, external);
    size_t sizes[512], n = arena_free_sizes(sizes, 512), hist[8] = {0};
    for (size_t i = 0; i < n; i++) {
        int b = 0;
        while (b < 7 && sizes[i] >= (size_t)64 << b) b++;
        hist[b]++;
    }
    printf("%-9s free blocks by size:", "");
    const char *label[] = {"<64", "<128", "<256", "<512", "<1K", "<2K", "<4K", "more"};
    for (int b = 0; b < 8; b++) printf(" %s %zu%s", label[b], hist[b], b < 7 ? "," : "\n");
}

int main(void)
{
    run("first fit", first_fit);
    run("best fit", best_fit);
    return 0;
}
