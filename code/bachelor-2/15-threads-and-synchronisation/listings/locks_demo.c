/* locks_demo.c: a plain counter protected by each lock. */
// capture: with=locks.c
#include <pthread.h>
#include <stdio.h>

#include "locks.h"

#define N 200000L

static long counter;                             /* plain: only the lock protects it */

static void *with_peterson(void *arg)
{
    int i = *(int *)arg;
    for (long k = 0; k < N; k++) {
        peterson_lock(i);
        counter++;                               /* critical section */
        peterson_unlock(i);
    }
    return NULL;
}

static void *with_bakery(void *arg)
{
    int i = *(int *)arg;
    for (long k = 0; k < N; k++) {
        bakery_lock(i);
        counter++;
        bakery_unlock(i);
    }
    return NULL;
}

static long run(void *(*f)(void *), int n)
{
    pthread_t t[MAXT];
    int id[MAXT];
    counter = 0;
    for (int i = 0; i < n; i++) {
        id[i] = i;
        pthread_create(&t[i], NULL, f, &id[i]);
    }
    for (int i = 0; i < n; i++)
        pthread_join(t[i], NULL);
    return counter;
}

int main(void)
{
    printf("Peterson, 2 threads: %ld (expected %ld)\n", run(with_peterson, 2), 2 * N);
    bakery_init(4);
    printf("bakery, 4 threads:   %ld (expected %ld)\n", run(with_bakery, 4), 4 * N);
    return 0;
}
