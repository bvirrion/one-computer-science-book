// avl.h: a search tree that keeps every balance factor in {-1, 0, 1}.
#ifndef AVL_H
#define AVL_H
#include <stdbool.h>

typedef struct avl {
    const char *key;
    int value, height;  // height: 0 for a leaf
    struct avl *left, *right;
} avl;

extern long avl_single, avl_double;  // rotations performed by avl_put so far

avl *avl_put(avl *t, const char *key, int value);  // returns the new root
bool avl_get(const avl *t, const char *key, int *value);
int avl_height(const avl *t);  // -1 for the empty tree
bool avl_check(const avl *t);  // search order, stored heights and balance factors
void avl_show(const avl *t);
void avl_free(avl *t);
#endif
