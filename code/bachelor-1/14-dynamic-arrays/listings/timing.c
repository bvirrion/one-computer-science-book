// timing.c: nanoseconds per push for three growth policies, best of three runs.
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static double now(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static long grow(int policy, long c) {
    return policy == 0 ? c + c / 2 + 1 : policy == 1 ? 2 * c : c + 16;
}

static double run(int policy, long n) {  // seconds for n pushes
    double start = now();
    long size = 0, capacity = 1;
    int *data = malloc(sizeof *data);
    for (long i = 0; i < n; i++) {
        if (size == capacity) {  // malloc + memcpy: a copy that realloc cannot avoid
            capacity = grow(policy, capacity);
            int *bigger = malloc(capacity * sizeof *bigger);
            memcpy(bigger, data, size * sizeof *data);
            free(data);
            data = bigger;
        }
        data[size++] = (int)i;
    }
    volatile int keep = data[n / 2];
    (void)keep;
    free(data);
    return now() - start;
}

int main(void) {
    printf("%8s %10s %10s %10s   (ns per push)\n", "n", "x1.5", "x2", "+16");
    for (long n = 1 << 12; n <= 1 << 18; n <<= 2) {
        printf("%8ld", n);
        for (int policy = 0; policy < 3; policy++) {
            double best = 1e9;
            for (int r = 0; r < 3; r++) {
                double t = run(policy, n);
                best = t < best ? t : best;
            }
            printf(" %10.2f", 1e9 * best / n);
        }
        printf("\n");
    }
    return 0;
}
