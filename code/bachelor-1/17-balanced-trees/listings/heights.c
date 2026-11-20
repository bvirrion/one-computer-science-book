// heights.c: the heights of trees built from the first n titles, inserted in catalogue order,
// in alphabetical order, and in random orders (average of 1000 shuffles).
// capture: with=bst.c,avl.c,llrb.c
#include "avl.h"
#include "bst.h"
#include "llrb.h"
#include "titles.h"
#include <string.h>

static int by_title(const void *a, const void *b) { return strcmp(*(char **)a, *(char **)b); }

static unsigned state = 17;
static unsigned next_random(void) { return state = state * 1103515245u + 12345u, state >> 8; }

static int bst_height_of(const char **keys, int n) {
    node *t = NULL;
    for (int i = 0; i < n; i++) t = bst_put(t, keys[i], i);
    int h = bst_height(t);
    bst_free(t);
    return h;
}

int main(void) {
    read_titles();
    const char *cat[TITLES], *alpha[TITLES], *mix[TITLES];
    printf("%3s %9s %6s %8s %5s %5s %10s\n", "n", "catalogue", "sorted", "shuffled", "AVL",
           "LLRB", "floor(lg n)");
    for (int n = 5; n <= TITLES; n += 5) {
        for (int i = 0; i < n; i++) cat[i] = alpha[i] = titles[i];
        qsort(alpha, n, sizeof alpha[0], by_title);
        double sum = 0;
        for (int r = 0; r < 1000; r++) {
            for (int i = 0; i < n; i++) mix[i] = titles[i];
            for (int i = n - 1; i > 0; i--) {  // Fisher-Yates
                int j = (int)(next_random() % (unsigned)(i + 1));
                const char *t = mix[i];
                mix[i] = mix[j], mix[j] = t;
            }
            sum += bst_height_of(mix, n);
        }
        avl *a = NULL;
        rb *b = NULL;
        for (int i = 0; i < n; i++) a = avl_put(a, cat[i], i), b = llrb_put(b, cat[i], i);
        int lg = 0;
        while (2 << lg <= n) lg++;
        printf("%3d %9d %6d %8.2f %5d %5d %10d\n", n, bst_height_of(cat, n), bst_height_of(alpha, n),
               sum / 1000, avl_height(a), llrb_height(b), lg);
        avl_free(a), llrb_free(b);
    }
    avl_single = avl_double = 0;  // the AVL tree of all 80 titles, in catalogue order
    avl *a = NULL;
    for (int i = 0; i < TITLES; i++) a = avl_put(a, titles[i], i);
    printf("AVL, 80 titles in catalogue order: %ld single and %ld double rotations, height %d\n",
           avl_single, avl_double, avl_height(a));
    avl_single = avl_double = 0;
    avl *s = NULL;
    for (int i = 0; i < TITLES; i++) s = avl_put(s, alpha[i], i);
    printf("AVL, 80 titles in alphabetical order: %ld single and %ld double rotations, height %d\n",
           avl_single, avl_double, avl_height(s));
    rb *b = NULL;
    for (int i = 0; i < TITLES; i++) b = llrb_put(b, titles[i], i);
    printf("LLRB, catalogue order: height %d, black height %d\n", llrb_height(b),
           llrb_black_height(b));
    avl_free(a), avl_free(s), llrb_free(b);
    return 0;
}
