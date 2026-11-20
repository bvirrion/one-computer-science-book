// pool.h: a pool of fixed-size blocks with a free list (exercise 11).
#ifndef POOL_H
#define POOL_H
#include <stddef.h>

struct pool {
    unsigned char *memory;      // count blocks of size bytes, in one heap block
    size_t size, count;
    void *free_list;            // the first free block; each free block holds the next
    size_t in_use;
};

int pool_init(struct pool *p, size_t size, size_t count);   // 0, or -1
void *pool_get(struct pool *p);                             // a block, or NULL if none is free
void pool_put(struct pool *p, void *block);                 // gives a block back
void pool_destroy(struct pool *p);

#endif
