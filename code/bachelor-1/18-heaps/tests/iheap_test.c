// test-with: ../listings/iheap.c
// Pushes, decrease-key and pops against a brute-force minimum over an array of keys.
#include "iheap.h"
#include <assert.h>
#include <stdio.h>

int main(void) {
    enum { N = 500 };
    int key[N];
    bool in[N] = {false};
    iheap h;
    ih_init(&h, N);
    unsigned s = 2;
    for (int r = 0; r < 20000; r++) {
        int x = (int)((s = s * 1103515245u + 12345u) >> 8) % N, op = (int)(s >> 20) % 3;
        int k = (int)(s >> 4) % 10000;
        if (!in[x]) ih_push(&h, x, k), key[x] = k, in[x] = true;
        else if (op < 2 && k < key[x]) ih_decrease(&h, x, k), key[x] = k;
        else if (op == 2) {
            int best = -1;
            for (int y = 0; y < N; y++)
                if (in[y] && (best < 0 || key[y] < key[best])) best = y;
            int got = ih_pop(&h);
            assert(in[got] && key[got] == key[best]);
            in[got] = false;
        }
        for (int y = 0; y < N; y += 37) assert(ih_contains(&h, y) == in[y]);
    }
    for (int i = 0; i < h.n; i++) assert(h.pos[h.item[i]] == i);
    ih_free(&h);
    puts("iheap: ok");
    return 0;
}
