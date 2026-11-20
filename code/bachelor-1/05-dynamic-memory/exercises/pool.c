// pool.c: the free blocks are chained through their own first bytes.
#include <stdlib.h>
#include "pool.h"

int pool_init(struct pool *p, size_t size, size_t count)
{
    if (size < sizeof(void *))
        size = sizeof(void *);                              // room for the link
    size = (size + sizeof(void *) - 1) / sizeof(void *) * sizeof(void *);   // aligned
    p->memory = malloc(size * count);
    if (p->memory == NULL)
        return -1;
    p->size = size;
    p->count = count;
    p->in_use = 0;
    p->free_list = NULL;
    for (size_t i = count; i > 0; i--) {                    // chain them, block 0 first
        void *block = p->memory + (i - 1) * size;
        *(void **)block = p->free_list;
        p->free_list = block;
    }
    return 0;
}

void *pool_get(struct pool *p)
{
    void *block = p->free_list;
    if (block == NULL)
        return NULL;
    p->free_list = *(void **)block;                         // unlink the first free block
    p->in_use++;
    return block;
}

void pool_put(struct pool *p, void *block)
{
    *(void **)block = p->free_list;                         // it becomes the first free block
    p->free_list = block;
    p->in_use--;
}

void pool_destroy(struct pool *p)
{
    free(p->memory);
    p->memory = NULL;
    p->free_list = NULL;
}
