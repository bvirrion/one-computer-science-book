/* semaphores.c: the same ring with two counting semaphores and a mutex. */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>

#define SLOTS 8
#define ITEMS 100000L

static long ring[SLOTS];
static int in, out;                              /* next slot to fill, to empty */
static sem_t empty, full;                        /* free slots; filled slots */
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static void put(long x)
{
    sem_wait(&empty);                            /* P: wait for a free slot */
    pthread_mutex_lock(&m);
    ring[in] = x;
    in = (in + 1) % SLOTS;
    pthread_mutex_unlock(&m);
    sem_post(&full);                             /* V: one more filled slot */
}

static long take(void)
{
    sem_wait(&full);
    pthread_mutex_lock(&m);
    long x = ring[out];
    out = (out + 1) % SLOTS;
    pthread_mutex_unlock(&m);
    sem_post(&empty);
    return x;
}

static void *producer(void *arg)
{
    (void)arg;
    for (long k = 1; k <= ITEMS; k++)
        put(k);
    return NULL;
}

static void *consumer(void *arg)
{
    long *sum = arg;
    for (long k = 0; k < ITEMS; k++)
        *sum += take();
    return NULL;
}

int main(void)
{
    sem_init(&empty, 0, SLOTS);                  /* all slots free */
    sem_init(&full, 0, 0);
    pthread_t p[2], c[2];
    long sums[2] = {0, 0};
    for (int i = 0; i < 2; i++) {
        pthread_create(&p[i], NULL, producer, NULL);
        pthread_create(&c[i], NULL, consumer, &sums[i]);
    }
    for (int i = 0; i < 2; i++) {
        pthread_join(p[i], NULL);
        pthread_join(c[i], NULL);
    }
    int e, f;
    sem_getvalue(&empty, &e);
    sem_getvalue(&full, &f);
    printf("sum taken: %ld, sum put: %ld\n", sums[0] + sums[1], ITEMS * (ITEMS + 1));
    printf("at the end: empty = %d, full = %d\n", e, f);
    return 0;
}
