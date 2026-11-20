/* treiber_test.c: one thread sees a LIFO stack; after the workers, every node is on the
   stack exactly once. */
#define main treiber_main
#include "../listings/treiber.c"
#undef main
#include <assert.h>

int main(void)
{
    atomic_store(&head, pack(0, NIL));
    push(3); push(7); push(5);
    assert(pop() == 5 && pop() == 7 && pop() == 3 && pop() == NIL);
    for (uint32_t i = 0; i < NODES; i++) push(i);
    pthread_t th[THREADS];
    for (long t = 0; t < THREADS; t++) pthread_create(&th[t], NULL, worker, (void *)t);
    for (int t = 0; t < THREADS; t++) pthread_join(th[t], NULL);
    int count[NODES] = {0}, n = 0;
    for (uint32_t i = pop(); i != NIL && n <= NODES; i = pop()) { count[i]++; n++; }
    assert(n == NODES);
    for (int i = 0; i < NODES; i++) assert(count[i] == 1);
    return 0;
}
