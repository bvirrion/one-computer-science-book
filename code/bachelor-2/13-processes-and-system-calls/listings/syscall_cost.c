/* syscall_cost.c: the time of a function call and of a system call that does almost nothing. */
#define _GNU_SOURCE
#include <stdio.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>

#define CALLS 2000000

__attribute__((noinline)) static long parent_of(long x)    /* an ordinary function */
{
    __asm__ volatile("" : : : "memory");                  /* the compiler must not remove it */
    return x + 1;
}

static double now_ns(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e9 + t.tv_nsec;
}

int main(void)
{
    long sum = 0;
    double t0 = now_ns();
    for (long k = 0; k < CALLS; k++)
        sum += parent_of(k);
    double t1 = now_ns();
    for (long k = 0; k < CALLS; k++)
        sum += syscall(SYS_getppid);                      /* into the kernel and back */
    double t2 = now_ns();
    printf("function call: %6.1f ns\n", (t1 - t0) / CALLS);
    printf("system call:   %6.1f ns, %.0f times longer%s\n", (t2 - t1) / CALLS,
           (t2 - t1) / (t1 - t0), sum == 0 ? "!" : "");
    return 0;
}
