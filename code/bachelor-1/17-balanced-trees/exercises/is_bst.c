// is_bst.c: checking the search-tree property; the local check is wrong.
#include "bst.h"
#include <stdbool.h>
#include <string.h>

bool is_bst_local(const node *t) {  // WRONG: compares each node only with its children
    if (t == NULL) return true;
    if (t->left != NULL && strcmp(t->left->key, t->key) >= 0) return false;
    if (t->right != NULL && strcmp(t->right->key, t->key) <= 0) return false;
    return is_bst_local(t->left) && is_bst_local(t->right);
}

static bool within(const node *t, const char *lo, const char *hi) {  // keys in (lo, hi)
    if (t == NULL) return true;
    if ((lo != NULL && strcmp(t->key, lo) <= 0) || (hi != NULL && strcmp(t->key, hi) >= 0))
        return false;
    return within(t->left, lo, t->key) && within(t->right, t->key, hi);
}

bool is_bst(const node *t) { return within(t, NULL, NULL); }
