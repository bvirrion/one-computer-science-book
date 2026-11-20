// test-with: ../listings/bst.c ../exercises/range_count.c ../exercises/is_bst.c ../exercises/from_sorted.c
// Random puts and deletes against a boolean array (keys k000..k399 sort like their numbers).
#include "bst.h"
#include "tree_keys.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>

int range_count(const node *t, const char *lo, const char *hi);
bool is_bst(const node *t);
bool is_bst_local(const node *t);
node *from_sorted(const char **keys, int lo, int hi);

static int seen, last;
static void ascending(const node *n) {
    int k = atoi(n->key + 1);
    assert(k > last);
    last = k, seen++;
}

int main(void) {
    make_keys();
    bool in[400] = {false};
    node *t = NULL;
    for (int r = 0; r < 20000; r++) {
        int k = rnd(400), v;
        if (rnd(3) > 0) t = bst_put(t, tree_keys[k], k), in[k] = true;
        else t = bst_delete(t, tree_keys[k]), in[k] = false;
        int q = rnd(400), size = 0, fl = -1, nx = -1, cnt = 0, lo = rnd(400), hi = rnd(400);
        for (int i = 0; i < 400; i++) {
            size += in[i];
            if (in[i] && i <= q) fl = i;
            if (in[i] && i > q && nx < 0) nx = i;
            cnt += in[i] && lo <= i && i <= hi;
        }
        assert(bst_size(t) == size && bst_get(t, tree_keys[q], &v) == in[q]);
        const char *f = bst_floor(t, tree_keys[q]), *n = bst_next(t, tree_keys[q]);
        assert(fl < 0 ? f == NULL : strcmp(f, tree_keys[fl]) == 0);
        assert(nx < 0 ? n == NULL : strcmp(n, tree_keys[nx]) == 0);
        assert(range_count(t, tree_keys[lo], tree_keys[hi]) == cnt && is_bst(t));
    }
    seen = 0, last = -1;
    bst_inorder(t, ascending);
    assert(seen == bst_size(t));
    bst_free(t);
    // the local check accepts a tree that is not a search tree: k005 below k010's left child
    node c = {tree_keys[20], 0, NULL, NULL}, b = {tree_keys[5], 0, NULL, &c};
    node a = {tree_keys[10], 0, &b, NULL};
    assert(is_bst_local(&a) && !is_bst(&a));
    const char *sorted[400];
    for (int n = 1; n <= 400; n++) {
        for (int i = 0; i < n; i++) sorted[i] = tree_keys[i];
        node *p = from_sorted(sorted, 0, n);
        int lg = 0;
        while (2 << lg <= n) lg++;
        assert(bst_height(p) == lg && bst_size(p) == n && is_bst(p));
        bst_free(p);
    }
    puts("bst: ok");
    return 0;
}
