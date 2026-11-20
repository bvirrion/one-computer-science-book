/* rows_cols.c: the same N * N additions over a matrix of ints, by rows and by columns. */
#define _POSIX_C_SOURCE 200809L                 /* for clock_gettime under -std=c17 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 4096                       /* 64 MiB of ints: far larger than any cache */

static double ms_since(struct timespec t0)
{
    struct timespec t1;
    clock_gettime(CLOCK_MONOTONIC, &t1);
    return (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
}

int main(void)
{
    int *a = malloc(sizeof(int) * N * N);
    for (long k = 0; k < (long)N * N; k++)
        a[k] = (int)(k % 7);
    struct timespec t0;

    clock_gettime(CLOCK_MONOTONIC, &t0);
    long rows = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            rows += a[(long)i * N + j];           /* consecutive addresses */
    double t_rows = ms_since(t0);

    clock_gettime(CLOCK_MONOTONIC, &t0);
    long cols = 0;
    for (int j = 0; j < N; j++)
        for (int i = 0; i < N; i++)
            cols += a[(long)i * N + j];           /* addresses 16 KiB apart */
    double t_cols = ms_since(t0);

    printf("row order:    sum %ld in %7.1f ms\n", rows, t_rows);
    printf("column order: sum %ld in %7.1f ms, %.1f times slower\n", cols, t_cols,
           t_cols / t_rows);
    free(a);
    return 0;
}
