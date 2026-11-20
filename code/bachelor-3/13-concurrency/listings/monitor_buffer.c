/* monitor_buffer.c -- a bounded buffer as a monitor: one mutex guards the state, and two
   condition variables let producers wait for room and consumers wait for an item. */
#include <pthread.h>
#include <stdio.h>

#define CAP 8
#define PER_PRODUCER 20000
#define PRODUCERS 2
#define CONSUMERS 2

static struct {
    pthread_mutex_t lock;
    pthread_cond_t not_full, not_empty;
    long items[CAP];
    int head, count;
} buf = {.lock = PTHREAD_MUTEX_INITIALIZER, .not_full = PTHREAD_COND_INITIALIZER,
         .not_empty = PTHREAD_COND_INITIALIZER};

void put(long x) {
    pthread_mutex_lock(&buf.lock);
    while (buf.count == CAP)                     /* while, not if: recheck after waking */
        pthread_cond_wait(&buf.not_full, &buf.lock);
    buf.items[(buf.head + buf.count) % CAP] = x;
    buf.count++;
    pthread_cond_signal(&buf.not_empty);
    pthread_mutex_unlock(&buf.lock);
}

long take(void) {
    pthread_mutex_lock(&buf.lock);
    while (buf.count == 0)
        pthread_cond_wait(&buf.not_empty, &buf.lock);
    long x = buf.items[buf.head];
    buf.head = (buf.head + 1) % CAP;
    buf.count--;
    pthread_cond_signal(&buf.not_full);
    pthread_mutex_unlock(&buf.lock);
    return x;
}

static void *producer(void *arg) {
    long base = (long)arg * PER_PRODUCER;
    for (long i = 1; i <= PER_PRODUCER; i++)
        put(base + i);                           /* producer p sends p*N+1 .. p*N+N */
    return NULL;
}

static long sums[CONSUMERS], counts[CONSUMERS];

static void *consumer(void *arg) {
    long c = (long)arg, n = (long)PRODUCERS * PER_PRODUCER / CONSUMERS;
    for (long i = 0; i < n; i++) {
        sums[c] += take();
        counts[c]++;
    }
    return NULL;
}

int main(void) {
    pthread_t p[PRODUCERS], c[CONSUMERS];
    for (long i = 0; i < PRODUCERS; i++) pthread_create(&p[i], NULL, producer, (void *)i);
    for (long i = 0; i < CONSUMERS; i++) pthread_create(&c[i], NULL, consumer, (void *)i);
    for (int i = 0; i < PRODUCERS; i++) pthread_join(p[i], NULL);
    for (int i = 0; i < CONSUMERS; i++) pthread_join(c[i], NULL);
    long n = 0, sum = 0, total = (long)PRODUCERS * PER_PRODUCER;
    for (int i = 0; i < CONSUMERS; i++) { n += counts[i]; sum += sums[i]; }
    printf("items taken: %ld of %ld\n", n, total);
    printf("sum taken:   %ld, expected %ld\n", sum, total * (total + 1) / 2);
    printf("left in the buffer: %d\n", buf.count);
    return 0;
}
