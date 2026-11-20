/* monitor_buffer_test.c: every item sent is taken exactly once, and the buffer ends empty
   (8 threads: 4 producers, 4 consumers). */
#define main buffer_main
#include "../listings/monitor_buffer.c"
#undef main
#include <assert.h>

static int taken[4 * 1000 + 1];

static void *prod(void *arg) {
    for (long i = 1; i <= 1000; i++) put((long)arg * 1000 + i);
    return NULL;
}

static void *cons(void *arg) {
    (void)arg;
    for (int i = 0; i < 1000; i++) {
        long x = take();
        __atomic_add_fetch(&taken[x], 1, __ATOMIC_RELAXED);
    }
    return NULL;
}

int main(void)
{
    pthread_t th[8];
    for (long t = 0; t < 4; t++) pthread_create(&th[t], NULL, prod, (void *)t);
    for (long t = 4; t < 8; t++) pthread_create(&th[t], NULL, cons, NULL);
    for (int t = 0; t < 8; t++) pthread_join(th[t], NULL);
    for (int x = 1; x <= 4000; x++) assert(taken[x] == 1);
    assert(buf.count == 0);
    return 0;
}
