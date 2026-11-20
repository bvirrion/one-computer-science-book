/* sigint_self.c: SIGINT kills by default; with a handler, the program decides. */
#define _POSIX_C_SOURCE 200809L
#include <signal.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

static volatile sig_atomic_t interrupted = 0;

static void on_sigint(int sig)
{
    (void)sig;
    interrupted = 1;                             /* only set a flag: see the text */
}

int main(void)
{
    pid_t r = fork();
    if (r == 0) {                                /* default action: the child dies */
        kill(getpid(), SIGINT);
        _exit(0);                                /* never reached */
    }
    int status;
    waitpid(r, &status, 0);
    int sig = WIFSIGNALED(status) ? WTERMSIG(status) : 0;
    printf("default: child killed by signal %d\n", sig);

    struct sigaction sa = {0};
    sa.sa_handler = on_sigint;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGINT, &sa, NULL);                /* from now on, SIGINT calls on_sigint */
    kill(getpid(), SIGINT);                      /* as if Ctrl-C were typed */
    printf("handled: interrupted = %d, and the program goes on\n", (int)interrupted);
    return 0;
}
