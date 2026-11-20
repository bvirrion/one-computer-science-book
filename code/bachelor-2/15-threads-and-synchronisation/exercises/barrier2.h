/* barrier2.h: a reusable barrier from a mutex and a condition (exercise 7). */
#ifndef BARRIER2_H
#define BARRIER2_H

#include <pthread.h>

struct barrier2 {
    pthread_mutex_t m;
    pthread_cond_t all_here;
    int n, waiting;
    unsigned long round;                         /* which use of the barrier this is */
};

void barrier2_init(struct barrier2 *b, int n);
int barrier2_wait(struct barrier2 *b);           /* 1 for the last to arrive, else 0 */

#endif
