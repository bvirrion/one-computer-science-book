// test-with: ../listings/bst.c
// Round trips of random trees: the tree read back is written out identically.
#define main serialise_main
#include "serialise.c"
#undef main
#include "tree_keys.h"
#include <assert.h>

int main(void) {
    make_keys();
    for (int trial = 0; trial < 50; trial++) {
        node *t = NULL;
        int n = rnd(60);
        for (int i = 0; i < n; i++) t = bst_put(t, tree_keys[rnd(400)], i);
        FILE *f = tmpfile(), *g = tmpfile();
        assert(f != NULL && g != NULL);
        write_tree(t, f);
        rewind(f);
        stored = 0;
        node *copy = read_tree(f);
        write_tree(copy, g);
        fseek(f, 0, SEEK_END), fseek(g, 0, SEEK_END);
        long a = ftell(f), b = ftell(g);
        assert(a == b && bst_size(copy) == bst_size(t) && bst_height(copy) == bst_height(t));
        char x[4096], y[4096];
        rewind(f), rewind(g);
        assert(fread(x, 1, (size_t)a, f) == (size_t)a && fread(y, 1, (size_t)b, g) == (size_t)b);
        assert(memcmp(x, y, (size_t)a) == 0);
        fclose(f), fclose(g), bst_free(t), bst_free(copy);
    }
    puts("serialise: ok");
    return 0;
}
