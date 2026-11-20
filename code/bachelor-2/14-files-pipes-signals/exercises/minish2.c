/* minish2.c: ch. 13's shell with <, >, | and a final & (exercises 10 and 12). */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAXW 64

static volatile sig_atomic_t finished = 0;       /* background processes reaped */

static void on_sigchld(int sig)
{
    (void)sig;
    int saved = errno;
    while (waitpid(-1, NULL, WNOHANG) > 0)
        finished++;
    errno = saved;
}

static void redirect(char **w)                   /* in a child: apply and remove < f, > f */
{
    int j = 0;
    for (int i = 0; w[i]; i++) {
        int in = strcmp(w[i], "<") == 0, out = strcmp(w[i], ">") == 0;
        if ((in || out) && w[i + 1]) {
            int fd = in ? open(w[i + 1], O_RDONLY)
                        : open(w[i + 1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
            if (fd < 0) {
                perror(w[i + 1]);
                _exit(1);
            }
            dup2(fd, in ? 0 : 1);
            close(fd);
            i++;                                 /* skip the file name */
        } else {
            w[j++] = w[i];
        }
    }
    w[j] = NULL;
}

static int run_line(char **w, int n, int background)
{
    char **stage[MAXW];
    int k = 0;
    stage[k++] = w;
    for (int i = 0; i < n; i++)
        if (strcmp(w[i], "|") == 0) {            /* cut the line into stages */
            w[i] = NULL;
            stage[k++] = w + i + 1;
        }
    pid_t pids[MAXW];
    int prev = -1;
    for (int i = 0; i < k; i++) {
        int fd[2] = {-1, -1};
        if (i < k - 1 && pipe(fd) != 0)
            return 1;
        if ((pids[i] = fork()) == 0) {
            sigset_t none;                       /* the shell's mask would outlive exec */
            sigemptyset(&none);
            sigprocmask(SIG_SETMASK, &none, NULL);
            signal(SIGCHLD, SIG_DFL);
            if (prev != -1) dup2(prev, 0), close(prev);
            if (fd[1] != -1) dup2(fd[1], 1), close(fd[1]), close(fd[0]);
            redirect(stage[i]);                  /* after the pipes: > f wins over | */
            if (!stage[i][0]) _exit(0);
            execvp(stage[i][0], stage[i]);
            fprintf(stderr, "minish2: %s: command not found\n", stage[i][0]);
            _exit(127);
        }
        if (prev != -1) close(prev);
        if (fd[1] != -1) close(fd[1]);
        prev = fd[0];
    }
    if (background)
        return 0;
    int status = 0, s;
    for (int i = 0; i < k; i++)                  /* our own pids, never a background one */
        if (waitpid(pids[i], &s, 0) == pids[i] && i == k - 1)
            status = WIFEXITED(s) ? WEXITSTATUS(s) : 128 + WTERMSIG(s);
    return status;
}

int main(void)
{
    struct sigaction sa = {0};
    sa.sa_handler = on_sigchld;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    sigaction(SIGCHLD, &sa, NULL);
    sigset_t chld, old;
    sigemptyset(&chld);
    sigaddset(&chld, SIGCHLD);
    char line[1024], *w[MAXW + 1];
    int last = 0, reported = 0;
    for (;;) {
        if (finished != reported) {              /* report at the prompt, not in a handler */
            printf("[done: %d background process%s]\n", finished - reported,
                   finished - reported == 1 ? "" : "es");
            reported = finished;
        }
        printf("minish2$ ");
        fflush(stdout);
        if (!fgets(line, sizeof line, stdin))
            break;
        int n = 0;
        for (char *t = strtok(line, " \t\n"); t && n < MAXW; t = strtok(NULL, " \t\n"))
            w[n++] = t;
        w[n] = NULL;
        int background = n > 0 && strcmp(w[n - 1], "&") == 0;
        if (background)
            w[--n] = NULL;
        if (n == 0)
            continue;
        if (strcmp(w[0], "exit") == 0)
            return last;
        if (strcmp(w[0], "cd") == 0) {
            last = chdir(n > 1 ? w[1] : "/") != 0;
            continue;
        }
        sigprocmask(SIG_BLOCK, &chld, &old);     /* the handler waits until we have waited */
        last = run_line(w, n, background);
        sigprocmask(SIG_SETMASK, &old, NULL);
    }
    return last;
}
