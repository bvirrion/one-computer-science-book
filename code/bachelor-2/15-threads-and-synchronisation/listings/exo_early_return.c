/* exo_early_return.c: a withdrawal that refuses, and then (exercise 2). */
// capture: timeout=3 exit
#include <pthread.h>
#include <stdio.h>

static long balance = 100;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static int withdraw(long amount)
{
    pthread_mutex_lock(&m);
    if (amount > balance)
        return 0;                                /* refused */
    balance -= amount;
    pthread_mutex_unlock(&m);
    return 1;
}

int main(void)
{
    printf("withdraw 30: %d\n", withdraw(30));
    printf("withdraw 500: %d\n", withdraw(500));
    fflush(stdout);
    printf("withdraw 20: %d\n", withdraw(20));
    return 0;
}
