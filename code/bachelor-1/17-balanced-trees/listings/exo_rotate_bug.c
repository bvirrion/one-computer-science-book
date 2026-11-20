// exo_rotate_bug.c: exercise 6, a right rotation of the left subtree of the root.
// capture: with=bst.c
#include "bst.h"
#include <stdio.h>

static node *rotate_right(node *y) {
    node *x = y->left;
    y->left = x->right;
    x->right = y;
    return x;
}

static void print_key(const node *n) { printf(" %s", n->key); }

int main(void) {
    const char *names[] = {"Mia", "Eli", "Tom", "Bea", "Ivy", "Abe"};
    node *t = NULL;
    for (int i = 0; i < 6; i++) t = bst_put(t, names[i], i);
    rotate_right(t->left);  // rotate the subtree rooted at Eli
    printf("in order after the rotation:");
    bst_inorder(t, print_key);
    printf("\n");
    return 0;  // (the tree is not freed: its links are broken)
}
