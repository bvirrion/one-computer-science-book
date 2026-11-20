/* race.c: k threads add 1 to one counter a million times each, three ways. */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <time.h>

#define N 1000000L

static atomic_long counter;
static long plain;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static void *racy(void *arg)                     /* load, add, store: three steps */
{
    (void)arg;
    for (long k = 0; k < N; k++) {
        long r = atomic_load_explicit(&counter, memory_order_relaxed);
        atomic_store_explicit(&counter, r + 1, memory_order_relaxed);
    }
    return NULL;
}

static void *locked(void *arg)                   /* the three steps under a mutex */
{
    (void)arg;
    for (long k = 0; k < N; k++) {
        pthread_mutex_lock(&m);
        plain = plain + 1;
        pthread_mutex_unlock(&m);
    }
    return NULL;
}

static void *atomic_add(void *arg)               /* one indivisible instruction */
{
    (void)arg;
    for (long k = 0; k < N; k++)
        atomic_fetch_add(&counter, 1);
    return NULL;
}

static double run(void *(*f)(void *), int k)
{
    struct timespec a, b;
    pthread_t t[8];
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (int i = 0; i < k; i++)
        pthread_create(&t[i], NULL, f, NULL);
    for (int i = 0; i < k; i++)
        pthread_join(t[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &b);
    return (b.tv_sec - a.tv_sec) * 1e3 + (b.tv_nsec - a.tv_nsec) / 1e6;
}

int main(void)
{
    printf("threads   expected     racy result   lost    racy ms  mutex ms  atomic ms\n");
    for (int k = 1; k <= 8; k *= 2) {
        atomic_store(&counter, 0);
        double tr = run(racy, k);
        long got = atomic_load(&counter);
        plain = 0;
        double tm = run(locked, k);
        atomic_store(&counter, 0);
        double ta = run(atomic_add, k);
        if (plain != k * N || atomic_load(&counter) != k * N)
            return 1;                            /* never: both are exact */
        printf("%7d %10ld %13ld %5.1f %% %9.1f %9.1f %9.1f\n", k, k * N, got,
               100.0 * (k * N - got) / (k * N), tr, tm, ta);
    }
    return 0;
}
