/* transpose.c: B = transpose of A, n x n ints, plain and in tiles (exercise 9). */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 8192

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

static void plain(const int *a, int *b)          /* reads by rows, writes by columns */
{
    for (long i = 0; i < N; i++)
        for (long j = 0; j < N; j++)
            b[j * N + i] = a[i * N + j];
}

static void tiled(const int *a, int *b, int t)    /* t x t tiles: both sides stay in cache */
{
    for (long ii = 0; ii < N; ii += t)
        for (long jj = 0; jj < N; jj += t)
            for (long i = ii; i < ii + t; i++)
                for (long j = jj; j < jj + t; j++)
                    b[j * N + i] = a[i * N + j];
}

int main(void)
{
    int *a = malloc(sizeof(int) * N * N), *b = malloc(sizeof(int) * N * N);
    for (long k = 0; k < (long)N * N; k++)
        a[k] = (int)k;
    double t0 = now_ms();
    plain(a, b);
    printf("plain       %7.1f ms   b[1][0] = %d\n", now_ms() - t0, b[N]);
    for (int t = 8; t <= 64; t *= 2) {
        t0 = now_ms();
        tiled(a, b, t);
        printf("tiles of %2d %7.1f ms   b[1][0] = %d\n", t, now_ms() - t0, b[N]);
    }
    return 0;
}
