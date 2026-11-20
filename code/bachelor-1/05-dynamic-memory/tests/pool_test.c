// test-with: ../exercises/pool.c
#include <assert.h>
#include <stdio.h>
#include "../exercises/pool.h"

int main(void)
{
    struct pool p;
    assert(pool_init(&p, 12, 5) == 0);
    void *b[5];
    for (int i = 0; i < 5; i++) {
        b[i] = pool_get(&p);
        assert(b[i] != NULL);
        for (int j = 0; j < i; j++)
            assert(b[i] != b[j]);
    }
    assert(pool_get(&p) == NULL && p.in_use == 5);       // all taken
    pool_put(&p, b[2]);
    pool_put(&p, b[4]);
    assert(pool_get(&p) == b[4]);                        // last given back, first reused
    assert(pool_get(&p) == b[2]);
    assert(pool_get(&p) == NULL);
    for (int i = 0; i < 5; i++)
        pool_put(&p, b[i]);
    assert(p.in_use == 0);
    pool_destroy(&p);
    puts("pool_test: ok");
    return 0;
}
