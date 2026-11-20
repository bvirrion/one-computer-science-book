/* ex11_barrier.c -- the write barrier: a write that makes an old cell point into the
   nursery puts the old cell in the remembered set. It includes gen.c for its helpers. */
#include "../listings/gen.c"

static int in_set(int c)
{
    for (int i = 0; i < nremembered; i++)
        if (remembered[i] == c) return 1;
    return 0;
}

void gc_write(int c, int k, int v)  /* mem[c].ref[k] = v, with the barrier */
{
    if (!young(c) && v != NIL && young(v) && !in_set(c)) remembered[nremembered++] = c;
    mem[c].ref[k] = v;
}
