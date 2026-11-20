/* sigchld_reap.c: a handler that reaps every child that ends, while main does other work. */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

static volatile sig_atomic_t reaped = 0;

static void on_sigchld(int sig)
{
    (void)sig;
    int saved = errno;                           /* waitpid may change errno */
    while (waitpid(-1, NULL, WNOHANG) > 0)       /* several children may have ended */
        reaped++;
    errno = saved;
}

int main(void)
{
    struct sigaction sa = {0};
    sa.sa_handler = on_sigchld;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;                    /* interrupted calls resume */
    sigaction(SIGCHLD, &sa, NULL);

    sigset_t block, old;
    sigemptyset(&block);
    sigaddset(&block, SIGCHLD);
    sigprocmask(SIG_BLOCK, &block, &old);        /* no signal between test and sleep */
    for (int k = 0; k < 5; k++)
        if (fork() == 0)
            _exit(k);
    while (reaped < 5)
        sigsuspend(&old);                        /* unblock, sleep until a signal */
    sigprocmask(SIG_SETMASK, &old, NULL);
    printf("5 children started, %d reaped by the handler, no zombie left\n", (int)reaped);
    return 0;
}
