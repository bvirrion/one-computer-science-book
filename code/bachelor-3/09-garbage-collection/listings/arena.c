/* arena.c -- every block, free or used, starts and ends with a boundary tag: its size in
   bytes, with the low bit set when the block is in use. The blocks tile the arena. */
#include "arena.h"

#define W sizeof(size_t)
#define N (ARENA_BYTES / W)
#define MIN_BLOCK 32
static size_t heap[N];
static arena_fit fit;

static size_t size(size_t i) { return heap[i] & ~(size_t)1; }
static int used(size_t i) { return heap[i] & 1; }
static size_t next(size_t i) { return i + size(i) / W; }
static void tag(size_t i, size_t bytes, size_t in_use)
{
    heap[i] = heap[i + bytes / W - 1] = bytes | in_use;  /* header and footer */
}

void arena_init(arena_fit policy)
{
    fit = policy;
    heap[0] = 1;             /* prologue: a footer in use, so nothing merges past the start */
    tag(1, (N - 2) * W, 0);  /* one free block, the whole arena */
    heap[N - 1] = 1;         /* epilogue: a header in use of size 0, where every walk stops */
}

size_t first_fit(size_t bytes)
{
    for (size_t i = 1; size(i) > 0; i = next(i))
        if (!used(i) && size(i) >= bytes) return i;
    return 0;
}

size_t best_fit(size_t bytes)
{
    size_t best = 0;
    for (size_t i = 1; size(i) > 0; i = next(i))
        if (!used(i) && size(i) >= bytes && (best == 0 || size(i) < size(best))) best = i;
    return best;
}

size_t arena_block_bytes(size_t n)
{
    size_t bytes = (n + 2 * W + 15) / 16 * 16;  /* payload and two tags, a multiple of 16 */
    return bytes < MIN_BLOCK ? MIN_BLOCK : bytes;
}

void *arena_alloc(size_t n)
{
    size_t bytes = arena_block_bytes(n), i = fit(bytes);
    if (i == 0) return NULL;
    size_t rest = size(i) - bytes;
    if (rest >= MIN_BLOCK) {  /* split: the tail stays free */
        tag(i, bytes, 1);
        tag(i + bytes / W, rest, 0);
    } else {
        tag(i, size(i), 1);   /* too small a tail: the request takes the whole block */
    }
    return &heap[i + 1];
}

void arena_free(void *p)
{
    size_t i = (size_t)((size_t *)p - heap) - 1, bytes = size(i);
    if (!used(next(i))) bytes += size(next(i));  /* coalesce with the next block */
    if (!used(i - 1)) {  /* and with the previous block, whose footer is at i - 1 */
        i -= size(i - 1) / W;
        bytes += size(i);
    }
    tag(i, bytes, 0);
}

struct arena_stats arena_stats(void)
{
    struct arena_stats s = {0};
    for (size_t i = 1; size(i) > 0; i = next(i)) {
        if (used(i)) {
            s.used_blocks++;
            s.used_bytes += size(i);
        } else {
            s.free_blocks++;
            s.free_bytes += size(i);
            if (size(i) > s.largest_free) s.largest_free = size(i);
        }
    }
    return s;
}

size_t arena_free_sizes(size_t *sizes, size_t max)
{
    size_t k = 0;
    for (size_t i = 1; size(i) > 0 && k < max; i = next(i))
        if (!used(i)) sizes[k++] = size(i);
    return k;
}
