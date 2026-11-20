/* barrier.c: four threads sum a table in rounds; nobody starts round r + 1 early. */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

#define T 4
#define ROUNDS 3

static long part[T];                             /* each thread's share of a round */
static pthread_barrier_t bar;

static void *work(void *arg)
{
    int i = *(int *)arg;
    for (int r = 1; r <= ROUNDS; r++) {
        part[i] = (long)r * (i + 1);             /* this round's work */
        int last = pthread_barrier_wait(&bar);   /* all four parts are written */
        if (last == PTHREAD_BARRIER_SERIAL_THREAD) {
            long total = 0;                      /* exactly one thread reports */
            for (int j = 0; j < T; j++)
                total += part[j];
            printf("round %d: total %ld\n", r, total);
        }
        pthread_barrier_wait(&bar);              /* nobody overwrites before the report */
    }
    return NULL;
}

int main(void)
{
    pthread_t t[T];
    int id[T];
    pthread_barrier_init(&bar, NULL, T);
    for (int i = 0; i < T; i++) {
        id[i] = i;
        pthread_create(&t[i], NULL, work, &id[i]);
    }
    for (int i = 0; i < T; i++)
        pthread_join(t[i], NULL);
    return 0;
}
