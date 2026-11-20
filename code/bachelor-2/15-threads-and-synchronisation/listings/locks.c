/* locks.c: Peterson's lock for two threads, Lamport's bakery for n. Every access to
   the shared variables is a sequentially consistent atomic load or store. */
#include <stdatomic.h>
#include <stdbool.h>

#include "locks.h"

static atomic_bool flag[2];                      /* flag[i]: thread i wants to enter */
static atomic_int turn;                          /* who yields if both want to */

void peterson_lock(int i)
{
    int j = 1 - i;
    atomic_store(&flag[i], true);
    atomic_store(&turn, j);                      /* after you */
    while (atomic_load(&flag[j]) && atomic_load(&turn) == j)
        ;                                        /* wait */
}

void peterson_unlock(int i)
{
    atomic_store(&flag[i], false);
}

static int nthreads;
static atomic_bool choosing[MAXT];
static atomic_long number[MAXT];                 /* 0: not waiting; else the ticket */

void bakery_init(int n)
{
    nthreads = n;
}

void bakery_lock(int i)
{
    atomic_store(&choosing[i], true);
    long max = 0;
    for (int j = 0; j < nthreads; j++) {         /* take a ticket larger than all */
        long nj = atomic_load(&number[j]);
        if (nj > max)
            max = nj;
    }
    atomic_store(&number[i], max + 1);
    atomic_store(&choosing[i], false);
    for (int j = 0; j < nthreads; j++) {
        while (atomic_load(&choosing[j]))
            ;                                    /* j is taking a ticket: wait */
        long nj;
        while ((nj = atomic_load(&number[j])) != 0
               && (nj < number[i] || (nj == number[i] && j < i)))
            ;                                    /* j is served first: wait */
    }
}

void bakery_unlock(int i)
{
    atomic_store(&number[i], 0);
}
