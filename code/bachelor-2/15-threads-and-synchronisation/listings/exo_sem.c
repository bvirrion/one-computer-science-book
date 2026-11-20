/* exo_sem.c: two threads, two semaphores (exercise 5). */
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>

static sem_t s, t;                               /* both start at 0 */

static void *one(void *arg)
{
    (void)arg;
    printf("A");
    sem_post(&s);
    printf("C");
    sem_wait(&t);
    printf("E\n");
    return NULL;
}

static void *two(void *arg)
{
    (void)arg;
    printf("B");
    sem_wait(&s);
    printf("D");
    sem_post(&t);
    return NULL;
}

int main(void)
{
    sem_init(&s, 0, 0);
    sem_init(&t, 0, 0);
    pthread_t a, b;
    pthread_create(&a, NULL, one, NULL);
    pthread_create(&b, NULL, two, NULL);
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    return 0;
}
