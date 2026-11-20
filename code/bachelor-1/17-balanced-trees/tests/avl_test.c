// test-with: ../listings/avl.c
// Invariants after every insertion; at most one rotation event per insertion; the height bound.
#include "avl.h"
#include "tree_keys.h"
#include <assert.h>
#include <math.h>

int main(void) {
    make_keys();
    for (int trial = 0; trial < 30; trial++) {
        avl *t = NULL;
        int n = 0;
        bool in[400] = {false};
        for (int r = 0; r < 400; r++) {
            int k = trial == 0 ? r : rnd(400);  // trial 0: increasing keys
            long before = avl_single + avl_double;
            t = avl_put(t, tree_keys[k], k);
            assert(avl_single + avl_double - before <= 1 && avl_check(t));
            n += !in[k], in[k] = true;
            assert(avl_height(t) < 1.4405 * log2(n + 2) - 0.3277);
        }
        for (int k = 0; k < 400; k++) {
            int v;
            assert(avl_get(t, tree_keys[k], &v) == in[k] && (!in[k] || v == k));
        }
        avl_free(t);
    }
    puts("avl: ok");
    return 0;
}
