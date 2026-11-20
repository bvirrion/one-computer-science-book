// anagrams.c: all orders of the letters of a word, under the additive and the
// polynomial hash, in m = 127 buckets.
// capture: with=hashes.c
#include "hashes.h"
#include <stdio.h>
#include <string.h>

static int count[2][127], keys;

static void each_order(char *w, int k, int n) {  // all permutations of w[k..n)
    if (k == n) {
        count[0][hash_additive(w) % 127]++;
        count[1][hash_poly(w) % 127]++;
        keys++;
        return;
    }
    for (int i = k; i < n; i++) {
        char t = w[k]; w[k] = w[i]; w[i] = t;
        each_order(w, k + 1, n);
        t = w[k]; w[k] = w[i]; w[i] = t;
    }
}

int main(void) {
    char word[] = "dorset";  // six distinct letters: 6! = 720 keys
    each_order(word, 0, (int)strlen(word));
    for (int h = 0; h < 2; h++) {
        int used = 0, largest = 0;
        for (int b = 0; b < 127; b++) {
            used += count[h][b] > 0;
            largest = count[h][b] > largest ? count[h][b] : largest;
        }
        printf("%-10s %d keys in %3d buckets, largest bucket %3d\n",
               h == 0 ? "additive" : "polynomial", keys, used, largest);
    }
    return 0;
}
