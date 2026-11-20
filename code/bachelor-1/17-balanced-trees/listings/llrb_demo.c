// llrb_demo.c: the same ten increasing keys in a left-leaning red-black tree.
// capture: with=llrb.c
#include "llrb.h"
#include <stdio.h>

int main(void) {
    const char *keys[] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"};
    rb *t = NULL;
    for (int i = 0; i < 10; i++) t = llrb_put(t, keys[i], i);
    printf("10 keys, height %d, black height %d, valid: %s\n", llrb_height(t),
           llrb_black_height(t), llrb_check(t) ? "yes" : "no");
    llrb_show(t);
    llrb_free(t);
    return 0;
}
