/* bounded_buffer.c: producers and consumers share a ring of 8 slots (mutex + conditions). */
#include <pthread.h>
#include <stdio.h>

#define SLOTS 8
#define ITEMS 100000L                            /* per producer */

static long ring[SLOTS];
static int head, count, most;                    /* next to take; items held; max seen */
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;
static pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;

static void put(long x)
{
    pthread_mutex_lock(&m);
    while (count == SLOTS)                       /* while, not if: see exercise 6 */
        pthread_cond_wait(&not_full, &m);        /* unlocks m, sleeps, relocks m */
    ring[(head + count) % SLOTS] = x;
    count++;
    if (count > most)
        most = count;
    pthread_cond_signal(&not_empty);
    pthread_mutex_unlock(&m);
}

static long take(void)
{
    pthread_mutex_lock(&m);
    while (count == 0)
        pthread_cond_wait(&not_empty, &m);
    long x = ring[head];
    head = (head + 1) % SLOTS;
    count--;
    pthread_cond_signal(&not_full);
    pthread_mutex_unlock(&m);
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
    long expected = 2 * (ITEMS * (ITEMS + 1) / 2);
    printf("sum taken: %ld, sum put: %ld\n", sums[0] + sums[1], expected);
    printf("never more than %d items held: %s\n", SLOTS, most <= SLOTS ? "yes" : "no");
    return 0;
}
