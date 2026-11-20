/* philosophers_ordered.c: each takes the lower-numbered of its two forks first. */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>
#include <time.h>

#define P 5
#define MEALS 100000

static pthread_mutex_t fork_[P];
static long meals[P];

static void *dine(void *arg)
{
    int i = *(int *)arg, a = i, b = (i + 1) % P;
    int first = a < b ? a : b, second = a < b ? b : a;   /* philosopher 4: 0 then 4 */
    for (int k = 0; k < MEALS; k++) {
        pthread_mutex_lock(&fork_[first]);
        pthread_mutex_lock(&fork_[second]);
        meals[i]++;                                       /* eats */
        pthread_mutex_unlock(&fork_[second]);
        pthread_mutex_unlock(&fork_[first]);
    }
    return NULL;
}

int main(void)
{
    pthread_t t[P];
    int id[P];
    for (int i = 0; i < P; i++)
        pthread_mutex_init(&fork_[i], NULL);
    for (int i = 0; i < P; i++) {
        id[i] = i;
        pthread_create(&t[i], NULL, dine, &id[i]);
    }
    for (int i = 0; i < P; i++)
        pthread_join(t[i], NULL);
    for (int i = 0; i < P; i++)
        printf("philosopher %d ate %ld times\n", i, meals[i]);
    return 0;
}
