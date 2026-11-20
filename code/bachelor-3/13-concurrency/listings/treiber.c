/* treiber.c -- Treiber's lock-free stack. Nodes live in an array and are named by index; the
   head packs a node index with a tag that every change increments, against the ABA problem. */
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>

#define NODES 64
#define THREADS 4
#define ROUNDS 200000
#define NIL 0xFFFFFFFFu                          /* the index of no node */
#ifndef TAG_STEP
#define TAG_STEP 1                               /* 0: no tag, and ABA can strike */
#endif

static _Atomic uint32_t next[NODES];             /* node i's successor on the stack */
static _Atomic uint64_t head;                    /* tag << 32 | index of the top node */

static uint64_t pack(uint32_t tag, uint32_t index) { return (uint64_t)tag << 32 | index; }

void push(uint32_t n) {
    uint64_t old = atomic_load(&head), new;
    do {
        atomic_store_explicit(&next[n], (uint32_t)old, memory_order_relaxed);
        new = pack((uint32_t)(old >> 32) + TAG_STEP, n);
    } while (!atomic_compare_exchange_weak(&head, &old, new)); /* failed: old is reloaded */
}

uint32_t pop(void) {
    uint64_t old = atomic_load(&head), new;
    do {
        if ((uint32_t)old == NIL) return NIL;    /* empty */
        uint32_t second = atomic_load_explicit(&next[(uint32_t)old], memory_order_relaxed);
        new = pack((uint32_t)(old >> 32) + TAG_STEP, second);
    } while (!atomic_compare_exchange_weak(&head, &old, new));
    return (uint32_t)old;
}

static long pops[THREADS];

static void *worker(void *arg) {                 /* take a node, put it back, many times */
    long t = (long)arg;
    for (int r = 0; r < ROUNDS; r++) {
        uint32_t n = pop();
        if (n == NIL) continue;                  /* all nodes are in other threads' hands */
        pops[t]++;
        push(n);
    }
    return NULL;
}

int main(void) {
    atomic_store(&head, pack(0, NIL));
    for (uint32_t i = 0; i < NODES; i++) push(i);
    pthread_t th[THREADS];
    for (long t = 0; t < THREADS; t++) pthread_create(&th[t], NULL, worker, (void *)t);
    for (int t = 0; t < THREADS; t++) pthread_join(th[t], NULL);
    long total = 0;
    for (int t = 0; t < THREADS; t++) total += pops[t];
    printf("%d threads, %d rounds each, pops that found a node: %ld\n", THREADS, ROUNDS, total);
    int seen[NODES] = {0}, n = 0;                /* walk the list from the head */
    uint32_t i = (uint32_t)atomic_load(&head);
    for (; i != NIL && !seen[i]; i = next[i]) { seen[i] = 1; n++; }
    printf("nodes reachable from the head: %d of %d, then ", n, NODES);
    if (i == NIL) printf("the end of the list\n");
    else printf("node %u again: a cycle\n", i);
    return 0;
}
