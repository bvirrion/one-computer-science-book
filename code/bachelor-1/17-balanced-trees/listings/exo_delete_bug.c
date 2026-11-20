// exo_delete_bug.c: exercise 5, a deletion with a shortcut for the two-child case.
// capture: with=bst.c
#include "bst.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

node *delete(node *t, const char *key) {
    if (t == NULL) return NULL;
    int c = strcmp(key, t->key);
    if (c < 0) t->left = delete(t->left, key);
    else if (c > 0) t->right = delete(t->right, key);
    else {
        node *child = t->left != NULL ? t->left : t->right;  // the child takes the node's place
        free(t);
        return child;
    }
    return t;
}

int main(void) {
    const char *names[] = {"Mia", "Eli", "Tom", "Bea", "Ivy", "Pia", "Zoe"};
    node *t = NULL;
    for (int i = 0; i < 7; i++) t = bst_put(t, names[i], i);
    printf("size %d", bst_size(t));
    t = delete(t, "Mia");
    printf(", after deleting Mia: size %d\n", bst_size(t));
    bst_show(t);
    bst_free(t);
    return 0;
}
