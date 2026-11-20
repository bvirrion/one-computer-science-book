// range_count.c: the number of keys k with lo <= k <= hi, visiting only the nodes that
// can hold such keys: O(h + the answer).
#include "bst.h"
#include <string.h>

int range_count(const node *t, const char *lo, const char *hi) {
    if (t == NULL) return 0;
    if (strcmp(t->key, lo) < 0) return range_count(t->right, lo, hi);  // all left keys too small
    if (strcmp(t->key, hi) > 0) return range_count(t->left, lo, hi);   // all right keys too large
    return 1 + range_count(t->left, lo, hi) + range_count(t->right, lo, hi);
}
