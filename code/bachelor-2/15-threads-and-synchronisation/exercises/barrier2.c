/* barrier2.c: the last thread to arrive starts a new round and wakes the others. */
#include "barrier2.h"

void barrier2_init(struct barrier2 *b, int n)
{
    pthread_mutex_init(&b->m, NULL);
    pthread_cond_init(&b->all_here, NULL);
    b->n = n;
    b->waiting = 0;
    b->round = 0;
}

int barrier2_wait(struct barrier2 *b)
{
    pthread_mutex_lock(&b->m);
    unsigned long my_round = b->round;
    int last = ++b->waiting == b->n;
    if (last) {
        b->waiting = 0;                          /* ready for the next use at once */
        b->round++;
        pthread_cond_broadcast(&b->all_here);
    } else {
        while (b->round == my_round)             /* not "waiting < n": that is reset */
            pthread_cond_wait(&b->all_here, &b->m);
    }
    pthread_mutex_unlock(&b->m);
    return last;
}
