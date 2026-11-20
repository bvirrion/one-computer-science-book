// kmerge.c: the returned loans of k branch libraries, each list sorted by day of return,
// merged into one list: by scanning the k heads, and with a heap of the k heads.
// capture: with=heap.c
#include "heap.h"
#include "loans.h"

static int list[32][LOANS], len[32], merged[LOANS];

static int by_day(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(void) {
    read_loans();
    printf("%3s %5s %9s %9s %7s\n", "k", "n", "scanning", "heap", "sorted");
    for (int k = 2; k <= 32; k *= 2) {
        int n = 0;
        for (int b = 0; b < k; b++) len[b] = 0;
        for (int i = 0; i < LOANS; i++)  // branch: the book number modulo k
            if (loans[i].returned >= 0) {
                int b = loans[i].book % k;
                list[b][len[b]++] = loans[i].returned, n++;
            }
        for (int b = 0; b < k; b++) qsort(list[b], (size_t)len[b], sizeof(int), by_day);
        long scan = 0;  // scanning: compare the heads of all non-empty lists
        int at[32] = {0};
        for (int out = 0; out < n; out++) {
            int best = -1;
            for (int b = 0; b < k; b++)
                if (at[b] < len[b] && (best < 0 || (scan++, list[b][at[b]] < list[best][at[best]])))
                    best = b;
            merged[out] = list[best][at[best]++];
        }
        heap h;  // the heap holds day * 64 + branch: the smallest day, ties by branch
        heap_init(&h);
        heap_compares = 0;
        for (int b = 0; b < k; b++) at[b] = 0;
        for (int b = 0; b < k; b++)
            if (len[b] > 0) heap_push(&h, list[b][at[b]++] * 64 + b);
        int ok = 1;
        for (int out = 0; out < n; out++) {
            int top = heap_min(&h), b = top % 64;
            ok &= top / 64 == merged[out] && (out == 0 || merged[out - 1] <= merged[out]);
            if (at[b] < len[b]) h.a[0] = list[b][at[b]++] * 64 + b, sift_down(h.a, h.n, 0);
            else heap_pop(&h);
        }
        printf("%3d %5d %9ld %9ld %7s\n", k, n, scan, heap_compares, ok ? "yes" : "no");
        heap_free(&h);
    }
    return 0;
}
