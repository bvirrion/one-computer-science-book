/* cheney_test.c: copying keeps every session intact, and exercise 8's graph. */
#include <assert.h>
#include <stdio.h>
#include "../listings/cheney.c"
#include "../listings/server.h"

int main(void)
{
    gc_init(3000);
    serve_init(150);
    for (int r = 0; r < 2000; r++) assert(serve(r, 150, 8, 24, 0));
    for (int r = 2000 - 150; r < 2000; r++) {
        int n = 0;
        for (int c = roots[r % 150]; c != NIL; c = gc_cell(c)->ref[0], n++)
            assert(gc_cell(c)->data == r);
        assert(n == 8);
    }
    /* exercise 8: E -> A, A -> B C, B -> D A, C -> D; only A is a root */
    gc_init(20);
    nroots = 1;
    roots[0] = NIL;
    int d = gc_alloc('D', NIL, NIL), c = gc_alloc('C', d, NIL);
    int b = gc_alloc('B', d, NIL), a = gc_alloc('A', b, c);
    gc_cell(b)->ref[1] = a;
    gc_alloc('E', a, NIL);
    roots[0] = a;
    collect();
    assert(gc_stats.visited == 4 && top == 4);
    assert(from[0].data == 'A' && from[1].data == 'B' && from[2].data == 'C' && from[3].data == 'D');
    assert(from[0].ref[0] == 1 && from[0].ref[1] == 2 && from[1].ref[0] == 3 && from[1].ref[1] == 0);
    assert(from[2].ref[0] == 3);
    printf("copying: sessions intact; exercise 8 copies A B C D in that order\n");
    return 0;
}
