/* tlb.c -- a fully associative TLB with LRU replacement, fed with the page numbers that
   three ways of summing a 1024 x 1024 matrix of 4-byte ints touch (one row = one page). */
#include <stdio.h>

#define N 1024
#define MAXTLB 128

static unsigned tag[MAXTLB];
static long used[MAXTLB], clock_now, hits, misses;

static void access_page(unsigned page, int size)
{
    int victim = 0;
    clock_now++;
    for (int e = 0; e < size; e++) {
        if (used[e] && tag[e] == page) {               /* hit */
            used[e] = clock_now;
            hits++;
            return;
        }
        if (used[e] < used[victim]) victim = e;        /* least recently used */
    }
    misses++;                                          /* walk the page table, refill */
    tag[victim] = page;
    used[victim] = clock_now;
}

static double run(int order, int size)
{
    for (int e = 0; e < MAXTLB; e++) used[e] = 0;
    hits = misses = 0;
    if (order == 0)                                    /* by rows */
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++) access_page(i, size);
    else if (order == 1)                               /* by columns */
        for (int j = 0; j < N; j++)
            for (int i = 0; i < N; i++) access_page(i, size);
    else                                               /* by columns, 32 rows at a time */
        for (int s = 0; s < N; s += 32)
            for (int j = 0; j < N; j++)
                for (int i = s; i < s + 32; i++) access_page(i, size);
    return 100.0 * hits / (hits + misses);
}

int main(void)
{
    const char *name[] = {"rows", "columns", "strips of 32"};
    printf("%-14s", "TLB entries");
    for (int size = 16; size <= MAXTLB; size *= 2) printf("%9d", size);
    printf("\n%-14s", "reach (KiB)");
    for (int size = 16; size <= MAXTLB; size *= 2) printf("%9d", size * 4);
    printf("\n");
    for (int order = 0; order < 3; order++) {
        printf("%-14s", name[order]);
        for (int size = 16; size <= MAXTLB; size *= 2) printf("%8.2f%%", run(order, size));
        printf("\n");
    }
    return 0;
}
