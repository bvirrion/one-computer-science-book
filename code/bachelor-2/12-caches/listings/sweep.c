/* sweep.c: the time of one memory access as the working set grows (a pointer chase). */
#define _POSIX_C_SOURCE 200809L                 /* for clock_gettime under -std=c17 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define LINE 64                                  /* one pointer per 64-byte line */
#define STEPS (1L << 23)                         /* accesses timed per size */

static uint64_t state = 2025;
static uint64_t next_random(void)                /* xorshift: the same cycle on every run */
{
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return state;
}

int main(void)
{
    printf("%10s %10s\n", "size KiB", "ns/access");
    for (long size = 4096; size <= 256L << 20; size *= 2) {
        long n = size / LINE;
        char *buf = aligned_alloc(LINE, size);
        long *order = malloc(sizeof(long) * n);
        for (long k = 0; k < n; k++)
            order[k] = k;
        for (long k = n - 1; k > 0; k--) {       /* Sattolo: a single random cycle */
            long r = (long)(next_random() % (uint64_t)k);
            long t = order[k]; order[k] = order[r]; order[r] = t;
        }
        for (long k = 0; k < n; k++)             /* line order[k] points to line order[k+1] */
            *(char **)(buf + order[k] * LINE) = buf + order[(k + 1) % n] * LINE;
        char *p = buf;
        for (long k = 0; k < n; k++)             /* one pass to warm the caches */
            p = *(char **)p;
        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        for (long k = 0; k < STEPS; k++)
            p = *(char **)p;                     /* each load needs the one before */
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double ns = ((t1.tv_sec - t0.tv_sec) * 1e9 + (t1.tv_nsec - t0.tv_nsec)) / STEPS;
        printf("%10ld %10.2f%s\n", size >> 10, ns, p == NULL ? "!" : "");
        free(order);
        free(buf);
    }
    return 0;
}
