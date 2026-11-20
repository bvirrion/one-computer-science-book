/* gen_test.c: the generational collector keeps sessions intact; the write barrier of
   exercise 11 keeps an old-to-young reference alive across a minor collection. */
#include <assert.h>
#include <stdio.h>
#include "../exercises/ex11_barrier.c"
#include "../listings/server.h"

static int old_points_young(int barrier)
{
    gc_init_gen(10, 1000);
    nroots = 1;
    roots[0] = gc_alloc(1, NIL, NIL);
    for (int i = 0; i < 10; i++) gc_alloc(0, NIL, NIL);  /* a minor collection promotes it */
    assert(!young(roots[0]) && minors == 1);
    int y = gc_alloc(42, NIL, NIL);
    if (barrier) gc_write(roots[0], 0, y);
    else mem[roots[0]].ref[0] = y;
    for (int i = 0; i < 20; i++) gc_alloc(-1, NIL, NIL);  /* garbage over the nursery */
    int c = mem[roots[0]].ref[0];
    return !young(c) && mem[c].data == 42;
}

int main(void)
{
    gc_init_gen(500, 12000);
    serve_init(500);
    for (int r = 0; r < 20000; r++) assert(serve(r, 500, 4, 12, 0));
    for (int r = 20000 - 500; r < 20000; r++) {
        int n = 0;
        for (int c = roots[r % 500]; c != NIL; c = gc_cell(c)->ref[0], n++)
            assert(gc_cell(c)->data == r);
        assert(n == 4);
    }
    assert(minors == 616 && majors == 23);
    assert(!old_points_young(0));  /* without the barrier the young cell is lost */
    assert(old_points_young(1));
    printf("generational: sessions intact; the barrier keeps the young cell\n");
    return 0;
}
