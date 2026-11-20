/* philosophers.c: five philosophers take the left fork, then the right. */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <time.h>

#define P 5

static pthread_mutex_t fork_[P];
static int stuck[P];                             /* fork philosopher i waited for, or -1 */
static pthread_barrier_t done;                   /* to report before anyone lets go */

static void pause_ms(long ms)
{
    struct timespec t = {ms / 1000, (ms % 1000) * 1000000L};
    nanosleep(&t, NULL);
}

static void *dine(void *arg)
{
    int i = *(int *)arg, left = i, right = (i + 1) % P;
    pthread_mutex_lock(&fork_[left]);
    pause_ms(100);                               /* everyone is now holding a fork */
    struct timespec limit;
    clock_gettime(CLOCK_REALTIME, &limit);
    limit.tv_sec += 1;                           /* wait at most one second */
    if (pthread_mutex_timedlock(&fork_[right], &limit) == ETIMEDOUT) {
        stuck[i] = right;
    } else {
        stuck[i] = -1;                           /* eats */
        pthread_mutex_unlock(&fork_[right]);
    }
    pthread_barrier_wait(&done);                 /* all five have tried */
    pthread_mutex_unlock(&fork_[left]);
    return NULL;
}

int main(void)
{
    pthread_t t[P];
    int id[P];
    for (int i = 0; i < P; i++)
        pthread_mutex_init(&fork_[i], NULL);
    pthread_barrier_init(&done, NULL, P);
    for (int i = 0; i < P; i++) {
        id[i] = i;
        pthread_create(&t[i], NULL, dine, &id[i]);
    }
    for (int i = 0; i < P; i++)
        pthread_join(t[i], NULL);
    for (int i = 0; i < P; i++)
        if (stuck[i] >= 0)
            printf("philosopher %d held fork %d, waited 1 s for fork %d\n", i, i, stuck[i]);
        else
            printf("philosopher %d ate\n", i);
    return 0;
}
