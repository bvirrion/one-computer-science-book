// test-with: ../listings/locks.c ../exercises/barrier2.c
/* counter_test.c: Peterson and the bakery keep a plain counter exact; the reusable barrier. */
#include <assert.h>
#include <pthread.h>
#include <stdio.h>

#include "../exercises/barrier2.h"
#include "locks.h"

#define N 50000L

static long counter;
static int nthreads;

static void *pet(void *arg)
{
    int i = *(int *)arg;
    for (long k = 0; k < N; k++) {
        peterson_lock(i);
        counter++;
        peterson_unlock(i);
    }
    return NULL;
}

static void *bak(void *arg)
{
    int i = *(int *)arg;
    for (long k = 0; k < N / nthreads; k++) {
        bakery_lock(i);
        counter++;
        bakery_unlock(i);
    }
    return NULL;
}

static struct barrier2 bar;
static int phase_of[8];
static int lasts;

static void *rounds(void *arg)
{
    int i = *(int *)arg;
    for (int r = 0; r < 2000; r++) {
        phase_of[i] = r;
        if (barrier2_wait(&bar))
            lasts++;                             /* only the last: no race */
        for (int j = 0; j < nthreads; j++)
            assert(phase_of[j] >= r);            /* nobody is behind */
        barrier2_wait(&bar);
    }
    return NULL;
}

static void run(void *(*f)(void *), int n)
{
    pthread_t t[8];
    int id[8];
    nthreads = n;
    for (int i = 0; i < n; i++) {
        id[i] = i;
        pthread_create(&t[i], NULL, f, &id[i]);
    }
    for (int i = 0; i < n; i++)
        pthread_join(t[i], NULL);
}

int main(void)
{
    counter = 0;
    run(pet, 2);
    assert(counter == 2 * N);
    for (int n = 2; n <= 8; n *= 2) {
        counter = 0;
        bakery_init(n);
        run(bak, n);
        assert(counter == n * (N / n));
    }
    for (int n = 1; n <= 8; n *= 2) {
        barrier2_init(&bar, n);
        lasts = 0;
        run(rounds, n);
        assert(lasts == 2000);                   /* one last arrival per round */
    }
    printf("counter_test: all passed\n");
    return 0;
}
