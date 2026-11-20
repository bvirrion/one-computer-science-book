// from_sorted.c: a search tree of minimal height from n sorted keys, in O(n).
#include "bst.h"
#include <stdlib.h>

node *from_sorted(const char **keys, int lo, int hi) {  // keys[lo..hi), sorted
    if (lo >= hi) return NULL;
    int mid = lo + (hi - lo) / 2;  // the middle key is the root
    node *t = malloc(sizeof *t);
    if (t == NULL) exit(1);
    *t = (node){keys[mid], mid, from_sorted(keys, lo, mid), from_sorted(keys, mid + 1, hi)};
    return t;
}
