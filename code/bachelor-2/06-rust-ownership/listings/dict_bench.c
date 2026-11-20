/* dict_bench.c: 4 million words drawn from 100 000, counted with dict.h. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <time.h>
#include "dict.h"

int main(void)
{
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    struct dict d;
    dict_init(&d, 8);
    uint64_t x = 2025;
    char word[16];
    for (int i = 0; i < 4000000; i++) {
        x = x * 6364136223846793005u + 1442695040888963407u;   /* the same generator in both */
        snprintf(word, sizeof word, "w%llu", (unsigned long long)((x >> 33) % 100000));
        (*dict_count(&d, word))++;
    }
    int w7 = *dict_count(&d, "w7");
    dict_free(&d);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double ms = (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
    printf("C:    %zu different, w7 %d times, %.0f ms\n", d.len, w7, ms);
    return 0;
}
