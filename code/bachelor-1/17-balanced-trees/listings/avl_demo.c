// avl_demo.c: ten keys inserted in increasing order, then two that need a double rotation.
// capture: with=avl.c
#include "avl.h"
#include <stdio.h>

int main(void) {
    const char *keys[] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "Fa", "Fb"};
    avl *t = NULL;
    for (int i = 0; i < 12; i++) {
        long s = avl_single, d = avl_double;
        t = avl_put(t, keys[i], i);
        if (avl_single > s || avl_double > d)
            printf("insert %-2s: %s rotation\n", keys[i], avl_double > d ? "double" : "single");
    }
    printf("12 keys, height %d, valid AVL tree: %s\n", avl_height(t), avl_check(t) ? "yes" : "no");
    avl_show(t);
    avl_free(t);
    return 0;
}
