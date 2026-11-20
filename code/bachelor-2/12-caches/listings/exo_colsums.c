/* exo_colsums.c: the sum of each column of a grid of loans per day (exercise 6). */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ROWS 8192
#define COLS 4096

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

static void col_sums_slow(const int *g, long *col)
{
    for (int j = 0; j < COLS; j++) {
        col[j] = 0;
        for (int i = 0; i < ROWS; i++)
            col[j] += g[(long)i * COLS + j];
    }
}

static void col_sums_fast(const int *g, long *col)   /* the loops interchanged */
{
    for (int j = 0; j < COLS; j++)
        col[j] = 0;
    for (int i = 0; i < ROWS; i++)
        for (int j = 0; j < COLS; j++)
            col[j] += g[(long)i * COLS + j];
}

int main(void)
{
    int *g = malloc(sizeof(int) * ROWS * COLS);
    long *a = malloc(sizeof(long) * COLS), *b = malloc(sizeof(long) * COLS);
    for (long k = 0; k < (long)ROWS * COLS; k++)
        g[k] = (int)(k % 13);
    double t0 = now_ms();
    col_sums_slow(g, a);
    double t1 = now_ms();
    col_sums_fast(g, b);
    double t2 = now_ms();
    int same = 1;
    for (int j = 0; j < COLS; j++)
        same &= a[j] == b[j];
    printf("column by column: %7.1f ms\n", t1 - t0);
    printf("row by row:       %7.1f ms, %.1f times faster, same sums: %s\n",
           t2 - t1, (t1 - t0) / (t2 - t1), same ? "yes" : "no");
    return 0;
}
