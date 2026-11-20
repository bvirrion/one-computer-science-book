// bst.h: an ordered dictionary from strings to ints, by a binary search tree.
// The tree keeps the key pointers it is given: the caller keeps the strings alive.
#ifndef BST_H
#define BST_H
#include <stdbool.h>

typedef struct node {
    const char *key;
    int value;
    struct node *left, *right;
} node;

node *bst_put(node *t, const char *key, int value);  // returns the new root
bool bst_get(const node *t, const char *key, int *value);
const node *bst_min(const node *t);
const char *bst_floor(const node *t, const char *key);  // largest key <= key, or NULL
const char *bst_next(const node *t, const char *key);   // smallest key > key, or NULL
node *bst_delete(node *t, const char *key);             // returns the new root
int bst_height(const node *t);                          // -1 for the empty tree
int bst_size(const node *t);
void bst_inorder(const node *t, void (*visit)(const node *));
void bst_show(const node *t);  // sideways: the root on the left, the right subtree above
void bst_free(node *t);
#endif
