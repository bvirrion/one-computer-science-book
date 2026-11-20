/* matmul.c: C = A B for n x n doubles, three loop orders over the same arithmetic. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define T 64                                      /* tile: three 64 x 64 tiles = 96 KiB */

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

static void ijk(int n, const double *A, const double *B, double *C)
{
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            double s = 0;
            for (int k = 0; k < n; k++)
                s += A[i * n + k] * B[k * n + j];   /* B walked down a column */
            C[i * n + j] = s;
        }
}

static void ikj(int n, const double *A, const double *B, double *C)
{
    for (int i = 0; i < n; i++)                   /* loop interchange: rows only */
        for (int k = 0; k < n; k++) {
            double a = A[i * n + k];
            for (int j = 0; j < n; j++)
                C[i * n + j] += a * B[k * n + j];
        }
}

static void blocked(int n, const double *A, const double *B, double *C)
{
    for (int ii = 0; ii < n; ii += T)             /* ikj on T x T tiles that stay in cache */
        for (int kk = 0; kk < n; kk += T)
            for (int jj = 0; jj < n; jj += T)
                for (int i = ii; i < ii + T; i++)
                    for (int k = kk; k < kk + T; k++) {
                        double a = A[i * n + k];
                        for (int j = jj; j < jj + T; j++)
                            C[i * n + j] += a * B[k * n + j];
                    }
}

int main(void)
{
    typedef void product(int, const double *, const double *, double *);
    struct { const char *name; product *f; } runs[] =
        {{"ijk", ijk}, {"ikj", ikj}, {"blocked", blocked}};
    for (int n = 1024; n <= 2048; n *= 2) {
        size_t bytes = sizeof(double) * n * n;
        double *A = malloc(bytes), *B = malloc(bytes), *C = malloc(bytes);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++) {
                A[i * n + j] = (i + 2 * j) % 7 - 3;
                B[i * n + j] = (3 * i + j) % 5 - 2;
            }
        for (int r = n == 1024 ? 0 : 1; r < 3; r++) {   /* ijk at 2048 would take minutes */
            memset(C, 0, bytes);
            double t0 = now_ms();
            runs[r].f(n, A, B, C);
            double t = now_ms() - t0, check = 0;
            for (int i = 0; i < n; i++)
                check += C[i * n + (i * 7) % n];
            printf("n = %4d  %-8s %8.1f ms   check %.0f\n", n, runs[r].name, t, check);
        }
        free(A), free(B), free(C);
    }
    return 0;
}
