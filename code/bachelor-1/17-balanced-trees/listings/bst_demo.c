// bst_demo.c: a search tree of names; in-order traversal, floor and next, a deletion.
// capture: with=bst.c
#include "bst.h"
#include <stdio.h>

static void print_key(const node *n) { printf(" %s", n->key); }

int main(void) {
    const char *names[] = {"Mia", "Eli", "Tom", "Bea", "Ivy", "Pia", "Zoe", "Gus", "Kai"};
    node *t = NULL;
    for (int i = 0; i < 9; i++) t = bst_put(t, names[i], i);
    bst_show(t);
    printf("in order:");
    bst_inorder(t, print_key);
    printf("\nheight %d, size %d\n", bst_height(t), bst_size(t));
    printf("floor(\"Jo\") = %s, next(\"Jo\") = %s, next(\"Zoe\") = %s\n", bst_floor(t, "Jo"),
           bst_next(t, "Jo"), bst_next(t, "Zoe") ? bst_next(t, "Zoe") : "(none)");
    t = bst_delete(t, "Eli");  // two children: Gus, its successor, takes its place
    printf("after deleting Eli:\n");
    bst_show(t);
    bst_free(t);
    return 0;
}
