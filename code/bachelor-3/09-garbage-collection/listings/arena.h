/* arena.h -- a heap allocator over one static arena of ARENA_BYTES bytes. */
#ifndef ARENA_H
#define ARENA_H
#include <stddef.h>

#define ARENA_BYTES (64 * 1024)

/* A placement policy: the word index of a free block of at least `bytes` bytes, or 0. */
typedef size_t (*arena_fit)(size_t bytes);
size_t first_fit(size_t bytes);
size_t best_fit(size_t bytes);

void arena_init(arena_fit fit);
void *arena_alloc(size_t n);  /* NULL when no free block is large enough */
void arena_free(void *p);

struct arena_stats {
    size_t used_blocks, used_bytes, free_blocks, free_bytes, largest_free;
};
struct arena_stats arena_stats(void);
size_t arena_block_bytes(size_t n);  /* the block size a request of n bytes takes */
size_t arena_free_sizes(size_t *sizes, size_t max);  /* free block sizes, in address order */
#endif
