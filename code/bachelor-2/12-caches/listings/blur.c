/* blur.c: a 3 x 3 box blur of a 4096 x 4096 grey image, in three traversal orders. */
#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 4096                                    /* 4-byte pixels: 64 MiB per image */

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

static inline void blur_pixel(const int32_t *in, int32_t *out, int y, int x)
{
    int32_t s = 0;
    for (int dy = -1; dy <= 1; dy++)
        for (int dx = -1; dx <= 1; dx++)
            s += in[(y + dy) * N + x + dx];
    out[y * N + x] = s / 9;
}

static void rows(const int32_t *in, int32_t *out)
{
    for (int y = 1; y < N - 1; y++)
        for (int x = 1; x < N - 1; x++)
            blur_pixel(in, out, y, x);
}

static void columns(const int32_t *in, int32_t *out)
{
    for (int x = 1; x < N - 1; x++)
        for (int y = 1; y < N - 1; y++)
            blur_pixel(in, out, y, x);
}

static void strips(const int32_t *in, int32_t *out, int w)   /* columns, w at a time */
{
    for (int x0 = 0; x0 < N; x0 += w)
        for (int y = 1; y < N - 1; y++)
            for (int x = x0 > 0 ? x0 : 1; x < x0 + w && x < N - 1; x++)
                blur_pixel(in, out, y, x);
}

int main(void)
{
    int32_t *in = malloc(sizeof(int32_t) * N * N);
    int32_t *out = calloc((size_t)N * N, sizeof(int32_t));
    uint32_t r = 2025;
    for (long k = 0; k < (long)N * N; k++) {     /* a generated image: grey levels 0..255 */
        r = r * 1664525u + 1013904223u;
        in[k] = (int32_t)(r >> 24);
    }
    const char *names[] = {"rows", "columns", "strips of 16", "strips of 64"};
    for (int run = 0; run < 4; run++) {
        double t0 = now_ms();
        if (run == 0) rows(in, out);
        else if (run == 1) columns(in, out);
        else strips(in, out, run == 2 ? 16 : 64);
        double t = now_ms() - t0;
        long check = 0;
        for (long k = 0; k < (long)N * N; k += 4097)
            check += out[k];
        printf("%-13s %8.1f ms   check %ld\n", names[run], t, check);
    }
    free(in), free(out);
    return 0;
}
