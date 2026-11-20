// test-with: ../listings/llrb.c
// Invariants after every insertion and the height bound h <= 2 lg(n + 1).
#include "llrb.h"
#include "tree_keys.h"
#include <assert.h>
#include <math.h>

int main(void) {
    make_keys();
    for (int trial = 0; trial < 30; trial++) {
        rb *t = NULL;
        int n = 0;
        bool in[400] = {false};
        for (int r = 0; r < 400; r++) {
            int k = trial == 0 ? r : trial == 1 ? 399 - r : rnd(400);
            t = llrb_put(t, tree_keys[k], k);
            n += !in[k], in[k] = true;
            assert(llrb_check(t) && llrb_height(t) + 1 <= 2 * log2(n + 1) + 1e-9);
        }
        for (int k = 0; k < 400; k++) {
            int v;
            assert(llrb_get(t, tree_keys[k], &v) == in[k] && (!in[k] || v == k));
        }
        llrb_free(t);
    }
    puts("llrb: ok");
    return 0;
}
