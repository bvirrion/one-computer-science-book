/* sb_litmus.c -- the store-buffering test: each thread writes its own variable, then reads
   the other's. Under sequential consistency r1 = r2 = 0 is impossible. Is it here? */
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>

#define TRIALS 100000

static atomic_int x[TRIALS], y[TRIALS];          /* a fresh pair of zeros for each trial */
static int r1[TRIALS], r2[TRIALS];
static atomic_int arrived;                       /* the two threads meet before each trial */
static unsigned char delay1[TRIALS], delay2[TRIALS];  /* a random wait, to line them up */

static void meet(int i, int delay) {
    atomic_fetch_add(&arrived, 1);
    while (atomic_load(&arrived) < 2 * (i + 1)) { /* spin until the other one is here */ }
    for (volatile int k = 0; k < delay; k++) { }
}

/* The order must be a constant: given a variable, the compiler takes the strongest. */
#define THREAD(name, mine, other, r, delay, order)                    \
    static void *name(void *arg) {                                     \
        (void)arg;                                                     \
        for (int i = 0; i < TRIALS; i++) {                             \
            meet(i, delay[i]);                                         \
            atomic_store_explicit(&mine[i], 1, order);                 \
            r[i] = atomic_load_explicit(&other[i], order);             \
        }                                                              \
        return NULL;                                                   \
    }
THREAD(relaxed1, x, y, r1, delay1, memory_order_relaxed)
THREAD(relaxed2, y, x, r2, delay2, memory_order_relaxed)
THREAD(seqcst1, x, y, r1, delay1, memory_order_seq_cst)
THREAD(seqcst2, y, x, r2, delay2, memory_order_seq_cst)

static void run(void *(*t1)(void *), void *(*t2)(void *), const char *name) {
    atomic_store(&arrived, 0);
    for (int i = 0; i < TRIALS; i++) { atomic_store(&x[i], 0); atomic_store(&y[i], 0); }
    pthread_t a, b;
    pthread_create(&a, NULL, t1, NULL);
    pthread_create(&b, NULL, t2, NULL);
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    long seen[2][2] = {{0}};
    for (int i = 0; i < TRIALS; i++) seen[r1[i]][r2[i]]++;
    printf("%-8s r1=0 r2=0: %6ld   r1=0 r2=1: %6ld   r1=1 r2=0: %6ld   r1=1 r2=1: %6ld\n",
           name, seen[0][0], seen[0][1], seen[1][0], seen[1][1]);
}

int main(void) {
    unsigned seed = 12345;
    for (int i = 0; i < TRIALS; i++) {
        seed = seed * 1103515245 + 12345;
        delay1[i] = seed >> 24 & 15;
        delay2[i] = seed >> 16 & 15;
    }
    printf("%d trials each\n", TRIALS);
    run(relaxed1, relaxed2, "relaxed");
    run(seqcst1, seqcst2, "seq_cst");
    return 0;
}
