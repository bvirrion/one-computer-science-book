// tree_keys.h: 400 distinct keys "k000" ... "k399" and a small random generator.
#include <stdio.h>
static char tree_keys[400][8];
static unsigned tree_state = 9;
static int rnd(int n) { return (int)((tree_state = tree_state * 1103515245u + 12345u) >> 8) % n; }
static void make_keys(void) {
    for (int i = 0; i < 400; i++) snprintf(tree_keys[i], sizeof tree_keys[i], "k%03d", i);
}
