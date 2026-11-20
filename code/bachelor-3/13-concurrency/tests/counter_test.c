/* counter_test.c: exercise 12. Four threads, 100,000 increments each: no update lost. */
#include "../exercises/ex12_counter.c"
#include <assert.h>
#include <stdio.h>

int main(void)
{
    pthread_t th[4];
    for (int t = 0; t < 4; t++) pthread_create(&th[t], NULL, count_up, (void *)100000L);
    for (int t = 0; t < 4; t++) pthread_join(th[t], NULL);
    assert(atomic_load(&counter) == 400000);
    return 0;
}
