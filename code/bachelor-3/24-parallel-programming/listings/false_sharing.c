/* false_sharing.c -- p threads each add 1 to their own counter 50 million times.
   The counters are adjacent 8-byte words, or each alone in a 64-byte block.
   No counter is shared; the cache lines are. Best of three runs. */
#define _POSIX_C_SOURCE 199309L
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <time.h>

#define STEPS 50000000L
#define MAXP 8

struct padded { _Alignas(64) atomic_long v; };
static _Alignas(64) atomic_long packed[MAXP]; /* eight counters in one 64-byte line */
static struct padded spread[MAXP];            /* one counter per line */

static void *bump(void *arg)
{
    atomic_long *c = arg;
    for (long i = 0; i < STEPS; i++)
        atomic_fetch_add_explicit(c, 1, memory_order_relaxed);
    return NULL;
}

static double run(int p, int padded)
{
    struct timespec t0, t1;
    pthread_t t[MAXP];
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int i = 0; i < p; i++)
        pthread_create(&t[i], NULL, bump, padded ? (void *)&spread[i].v : (void *)&packed[i]);
    for (int i = 0; i < p; i++) pthread_join(t[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    return (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
}

int main(void)
{
    printf(" p  adjacent ms  padded ms  ratio\n");
    for (int p = 1; p <= MAXP; p *= 2) {
        double a = 1e300, b = 1e300;
        for (int r = 0; r < 3; r++) {
            double x = run(p, 0), y = run(p, 1);
            a = x < a ? x : a;
            b = y < b ? y : b;
        }
        printf("%2d %12.1f %10.1f %6.1f\n", p, a, b, a / b);
    }
    long total = 0;
    for (int i = 0; i < MAXP; i++) total += packed[i] + spread[i].v;
    printf("all counts correct: %s\n", total == 2L * 3 * (1 + 2 + 4 + 8) * STEPS ? "yes" : "no");
    return 0;
}
