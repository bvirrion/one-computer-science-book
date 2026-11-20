/* ex12_counter.c -- a counter incremented by compare-and-swap: lock-free, and how many
   retries does it take? */
#include <pthread.h>
#include <stdatomic.h>

static atomic_long counter, retries;

void increment(void) {
    long old = atomic_load(&counter);
    while (!atomic_compare_exchange_weak(&counter, &old, old + 1))
        atomic_fetch_add_explicit(&retries, 1, memory_order_relaxed);  /* old reloaded */
}

void *count_up(void *arg) {
    for (long i = 0; i < (long)arg; i++) increment();
    return NULL;
}
